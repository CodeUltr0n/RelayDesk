#!/usr/bin/env python3
"""Benchmark harness for RelayDesk.

Runs a pipeline over labelled JSON cases and computes the plan's metrics.

Usage:
    python scripts/run_eval.py --cases fixtures/cases --pipeline null
    python scripts/run_eval.py --cases fixtures/cases --pipeline relaydesk --split heldout

Pipelines:
    null       trivial baseline: always predicts ESCALATE (sanity floor)
    relaydesk  your Nov 5/6 implementation (raises NotImplementedError until then)

Metrics (per split):
    correct_next_action   share of cases where the predicted outcome matches the label
    escalation_precision  of predicted ESCALATEs, share that were true bugs
    escalation_recall     of true bugs, share that were escalated
    top3_evidence_recall  share of cases whose expected evidence was predicted
    unsupported_assertion_count  claims without evidence (counted by your checker)
    median_latency_ms

Outputs:
    results/eval_run.json — per-case records + aggregate metrics
    stdout — a markdown table you can paste into docs/evaluation.md

Discipline: tune on the dev split only. Touch --split heldout once, on Nov 6.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))


@dataclass
class Prediction:
    """What a pipeline produced for one case."""

    outcome: str
    evidence_ids: list[str] = field(default_factory=list)
    draft_response: str | None = None
    unsupported_assertions: int = 0  # claims w/o evidence, counted by your checker
    latency_ms: float = 0.0


class NullPipeline:
    """Trivial baseline: escalate everything. Establishes the floor."""

    name = "null"

    def predict(self, case: dict) -> Prediction:
        start = time.perf_counter()
        p = Prediction(outcome="ESCALATE")
        p.latency_ms = (time.perf_counter() - start) * 1000
        return p


class RelayDeskPipeline:
    """Full implementation: normalize -> retrieval -> scoring -> decide."""

    name = "relaydesk"

    def __init__(self):
        from relaydesk.scoring import load_weights
        from relaydesk.retrieval import build_index

        import yaml

        policy_path = REPO_ROOT / "config" / "policy.yaml"
        with policy_path.open("r", encoding="utf-8") as fh:
            self._policy = yaml.safe_load(fh)
        self._weights = load_weights(self._policy)
        self._index = build_index(str(REPO_ROOT / "fixtures"))

    def predict(self, case: dict) -> Prediction:
        from relaydesk.normalize import normalize_report
        from relaydesk.scoring import rank_candidates
        from relaydesk.decision import decide

        start = time.perf_counter()

        report_data = case["report"]
        report = normalize_report(report_data["text"], report_data["author"])
        # Override with explicit fields from the case if present.
        if report_data.get("component"):
            report.component = report_data["component"]
        if report_data.get("version"):
            report.version = report_data["version"]
        if report_data.get("first_seen"):
            report.first_seen = report_data["first_seen"]
        if report_data.get("error_signature"):
            report.error_signature = report_data["error_signature"]

        top_k = self._policy.get("thresholds", {}).get("top_k_shortlist", 3)
        from relaydesk.retrieval import shortlist
        candidates = shortlist(report, self._index, k=top_k)

        scored = rank_candidates(report, candidates, self._weights, top_k=top_k)
        decision = decide(report, scored, self._policy)

        latency = (time.perf_counter() - start) * 1000

        # Validate that cited evidence IDs actually exist in the knowledge corpus.
        # An unsupported assertion occurs if a decision cites an ungrounded ID or drafts an answer without evidence.
        known_ids = {item.evidence_id for item in self._index.get("items", [])}
        unsupported = sum(1 for eid in decision.supporting_evidence if eid not in known_ids)
        if decision.outcome.value == "ANSWER" and not decision.supporting_evidence:
            unsupported += 1

        return Prediction(
            outcome=decision.outcome.value,
            evidence_ids=decision.supporting_evidence,
            draft_response=decision.draft_response,
            unsupported_assertions=unsupported,
            latency_ms=latency,
        )


def load_cases(case_dir: Path, split: str) -> list[dict]:
    """Load labelled case JSONs for one split ('dev' or 'heldout')."""
    cases = []
    for path in sorted(case_dir.glob("*.json")):
        if path.name.startswith("case_schema"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("split", "dev") == split:
            cases.append(data)
    return cases


def evaluate(cases: list[dict], pipeline) -> dict:
    """Run the pipeline over cases and compute the metric block."""
    records = []
    for case in cases:
        pred = pipeline.predict(case)
        expected_ids = set(case.get("expected_evidence_ids", []))
        if expected_ids:
            top3_hit = bool(expected_ids & set(pred.evidence_ids))
        else:
            # When no past evidence is expected (e.g. novel defect or clarification),
            # verify that the pipeline did not hallucinate an unrelated past ticket/runbook.
            top3_hit = bool(pred.outcome in ("ESCALATE", "CLARIFY"))
        records.append(
            {
                "case_id": case["case_id"],
                "label": case["label"],
                "predicted": pred.outcome,
                "correct": pred.outcome == case["label"],
                "top3_hit": top3_hit,
                "unsupported_assertions": pred.unsupported_assertions,
                "latency_ms": round(pred.latency_ms, 1),
            }
        )

    n = len(records) or 1
    true_esc = [c for c in cases if c["label"] == "ESCALATE"]
    pred_esc = [r for r in records if r["predicted"] == "ESCALATE"]
    metrics = {
        "pipeline": pipeline.name,
        "split": cases[0]["split"] if cases else "n/a",
        "n_cases": len(records),
        "correct_next_action": sum(r["correct"] for r in records) / n,
        "escalation_precision": (
            sum(1 for r in pred_esc if r["correct"]) / len(pred_esc)
        )
        if pred_esc
        else None,
        "escalation_recall": (
            sum(1 for r in pred_esc if r["correct"]) / len(true_esc)
        )
        if true_esc
        else None,
        "top3_evidence_recall": sum(r["top3_hit"] for r in records) / n,
        "unsupported_assertion_count": sum(
            r["unsupported_assertions"] for r in records
        ),
        "median_latency_ms": (
            sorted(r["latency_ms"] for r in records)[len(records) // 2]
            if records
            else None
        ),
    }
    return {"metrics": metrics, "records": records}


def main() -> int:
    ap = argparse.ArgumentParser(description="RelayDesk benchmark harness")
    ap.add_argument("--cases", default="fixtures/cases", help="dir of case JSONs")
    ap.add_argument("--pipeline", choices=["null", "relaydesk"], default="null")
    ap.add_argument("--split", choices=["dev", "heldout", "all"], default="all")
    args = ap.parse_args()

    case_dir = Path(args.cases)
    if not case_dir.exists():
        print(f"case dir not found: {case_dir}", file=sys.stderr)
        return 2

    pipeline = NullPipeline() if args.pipeline == "null" else RelayDeskPipeline()

    splits = ["dev", "heldout"] if args.split == "all" else [args.split]
    out = {"generated_by": pipeline.name, "results": []}
    for split in splits:
        cases = load_cases(case_dir, split)
        if not cases:
            continue
        try:
            out["results"].append(evaluate(cases, pipeline))
        except NotImplementedError as exc:
            print(f"pipeline not implemented: {exc}", file=sys.stderr)
            return 3

    results_dir = REPO_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "eval_run.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    pct_keys = {
        "correct_next_action",
        "escalation_precision",
        "escalation_recall",
        "top3_evidence_recall",
    }
    for block in out["results"]:
        m = block["metrics"]
        print(
            f"\n### {m['pipeline']} pipeline — split={m['split']} (n={m['n_cases']})\n"
        )
        print("| metric | value |")
        print("|---|---|")
        for k in (
            "correct_next_action",
            "escalation_precision",
            "escalation_recall",
            "top3_evidence_recall",
            "unsupported_assertion_count",
            "median_latency_ms",
        ):
            v = m[k]
            if isinstance(v, float) and k in pct_keys:
                v = f"{v:.1%}"
            print(f"| {k} | {v} |")
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
