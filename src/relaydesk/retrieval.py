"""Deterministic retrieval: shortlist the few evidence items worth scoring.

NOV 5 IMPLEMENTATION NOTE — budget 90 minutes. A keyword/token-overlap
baseline is enough for a 20-24 case corpus. Do NOT reach for embeddings or
a vector DB; determinism is a feature here (judges must be able to
reproduce the same shortlist from the same inputs).

Spec:
  build_index(corpus_dir) -> dict
    - walk fixtures/{tickets,runbooks,releases,logs}/
    - parse each file into an EvidenceItem (id from filename, type from dir)
  shortlist(report, index, k) -> list[EvidenceItem]
    - deterministic score: token overlap on error signature, plus component
      and version match
    - stable tie-break by evidence_id so every run is reproducible
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from relaydesk.schemas import EvidenceItem, EvidenceType, IssueReport

# Map directory names under fixtures/ to EvidenceType.
_DIR_TYPE_MAP: dict[str, EvidenceType] = {
    "tickets": EvidenceType.TICKET,
    "runbooks": EvidenceType.RUNBOOK,
    "releases": EvidenceType.RELEASE_NOTE,
    "release_notes": EvidenceType.RELEASE_NOTE,
    "logs": EvidenceType.LOG,
    "test_results": EvidenceType.TEST_RESULT,
    "tests": EvidenceType.TEST_RESULT,
}


def _tokenize(text: str | None) -> set[str]:
    """Lowercase alpha-numeric token set for deterministic matching."""
    if not text:
        return set()
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _parse_json_evidence(path: Path, etype: EvidenceType) -> EvidenceItem | None:
    """Parse a JSON fixture file into an EvidenceItem."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    status = data.get("status")
    raw_body = data.get("body", data.get("text", data.get("content", "")))
    body_with_status = f"[status: {status}] {raw_body}" if status else raw_body

    return EvidenceItem(
        evidence_id=data.get("id", path.stem),
        evidence_type=etype,
        title=data.get("title", data.get("summary", path.stem)),
        path=str(path),
        component=data.get("component"),
        version=data.get("version"),
        date=data.get("date"),
        error_signature=data.get("error_signature", data.get("error")),
        body=body_with_status,
        grounded_answer=data.get("grounded_answer", data.get("answer")),
    )


def _parse_text_evidence(path: Path, etype: EvidenceType) -> EvidenceItem:
    """Parse a markdown or plain-text fixture file into an EvidenceItem."""
    body = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem.replace("_", " ").replace("-", " ").title()

    # Try to extract a title from the first markdown heading.
    heading_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if heading_match:
        title = heading_match.group(1).strip()

    # Extract component if mentioned
    comp = None
    comp_m = re.search(r"\b([a-z0-9_-]+)[-\s]service\b", body, re.IGNORECASE)
    if comp_m:
        comp = f"{comp_m.group(1).lower()}-service"

    # Extract version if mentioned
    ver = None
    ver_m = re.search(r"\b(v\d+\.\d+(?:\.\d+)?)\b", body, re.IGNORECASE)
    if ver_m:
        ver = ver_m.group(1)

    return EvidenceItem(
        evidence_id=path.stem,
        evidence_type=etype,
        title=title,
        path=str(path),
        component=comp,
        version=ver,
        body=body,
        grounded_answer=body[:500] if etype == EvidenceType.RUNBOOK else None,
    )


def build_index(corpus_dir: str) -> dict:
    """Parse the fixtures corpus into an in-memory index of EvidenceItems.

    Returns a dict with key 'items' mapping to a list of EvidenceItem objects,
    and 'tokens' mapping evidence_id -> token set for fast retrieval.
    """
    root = Path(corpus_dir)
    items: list[EvidenceItem] = []
    tokens: dict[str, set[str]] = {}

    for subdir, etype in _DIR_TYPE_MAP.items():
        dirpath = root / subdir
        if not dirpath.is_dir():
            continue
        for fpath in sorted(dirpath.iterdir()):
            if fpath.is_dir() or fpath.name.startswith("."):
                continue

            item: EvidenceItem | None = None
            if fpath.suffix == ".json":
                item = _parse_json_evidence(fpath, etype)
            elif fpath.suffix in (".md", ".txt", ".log", ".yaml", ".yml"):
                item = _parse_text_evidence(fpath, etype)

            if item:
                items.append(item)
                # Build token set from all searchable text fields.
                combined = " ".join(
                    filter(None, [item.title, item.body, item.error_signature,
                                  item.component, item.version])
                )
                tokens[item.evidence_id] = _tokenize(combined)

    return {"items": items, "tokens": tokens}


def _relevance_score(
    report: IssueReport, item: EvidenceItem, item_tokens: set[str]
) -> float:
    """Compute a deterministic relevance score in [0, 1].

    Combines: token containment/overlap on error signature and report text (50%),
    component match (30%), and version match (20%).
    """
    report_text = " ".join(
        filter(None, [report.text, report.error_signature, report.component])
    )
    report_tokens = _tokenize(report_text)
    sig_tokens = _tokenize(report.error_signature)

    sig_score = 0.0
    if sig_tokens and item_tokens:
        sig_score = len(sig_tokens & item_tokens) / len(sig_tokens)

    text_score = 0.0
    if report_tokens and item_tokens:
        containment = len(report_tokens & item_tokens) / len(report_tokens)
        jaccard = len(report_tokens & item_tokens) / len(report_tokens | item_tokens)
        text_score = max(containment * 0.8, jaccard)

    overlap_score = max(sig_score, text_score)

    # Component match bonus.
    comp_bonus = 0.0
    if report.component:
        if item.component and report.component.lower() == item.component.lower():
            comp_bonus = 1.0
        elif report.component.lower() in item.body.lower():
            comp_bonus = 0.8

    # Version match bonus.
    ver_bonus = 0.0
    if report.version:
        if item.version and report.version.lower() == item.version.lower():
            ver_bonus = 1.0
        elif report.version.lower() in item.body.lower():
            ver_bonus = 0.8

    return overlap_score * 0.50 + comp_bonus * 0.30 + ver_bonus * 0.20


def shortlist(report: IssueReport, index: dict, k: int = 3) -> list[EvidenceItem]:
    """Return the top-k most relevant evidence items, deterministically.

    Stable tie-break by evidence_id ensures every run produces the same result.
    """
    items: list[EvidenceItem] = index.get("items", [])
    tokens: dict[str, set[str]] = index.get("tokens", {})

    scored: list[tuple[float, str, EvidenceItem]] = []
    for item in items:
        item_tokens = tokens.get(item.evidence_id, set())
        score = _relevance_score(report, item, item_tokens)
        # Tuple: (-score for descending, evidence_id for stable tie-break).
        scored.append((score, item.evidence_id, item))

    scored.sort(key=lambda t: (-t[0], t[1]))
    return [item for _, _, item in scored[:k]]
