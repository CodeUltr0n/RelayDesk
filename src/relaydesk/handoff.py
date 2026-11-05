"""Room handoff: render pipeline results into the standard message cards.

The Switch room transcript is your UI and your audit trail — judges read
it. Card copy lives in config/message_templates.yaml (copy is data, not
code). This module is COMPLETE: it only does string rendering.

Cards (matching templates in config/message_templates.yaml):
  Evidence Card  the shortlist + scores + rationale per candidate
  Decision Card  the chosen outcome + confidence + why + evidence ids
  Case Record    the final audit entry after human approval
"""

from __future__ import annotations

from pathlib import Path

import yaml

from relaydesk.schemas import CaseRecord, Decision, ScoredCandidate


class HandoffError(RuntimeError):
    """Raised for missing templates or empty inputs."""


def load_templates(path: str | Path = "config/message_templates.yaml") -> dict:
    """Load and validate the card templates; raise HandoffError if incomplete."""
    p = Path(path)
    if not p.exists():
        raise HandoffError(f"message templates not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    for key in ("evidence_card", "decision_card", "case_record"):
        if key not in data:
            raise HandoffError(f"missing template: {key}")
    return data


def render_evidence_card(candidates: list[ScoredCandidate], template: str) -> str:
    """Render the shortlist as one Evidence Card message.

    Raises HandoffError on an empty shortlist — never post an empty card.
    """
    if not candidates:
        raise HandoffError("refusing to render an empty shortlist")
    lines = []
    for rank, c in enumerate(candidates, start=1):
        lines.append(
            f"{rank}. {c.evidence.title} [{c.evidence.evidence_type.value}] "
            f"score={c.score:.2f} id={c.evidence.evidence_id}\n"
            f"   why: {c.rationale}"
        )
    body = "\n".join(lines)
    if "{shortlist}" not in template:
        raise HandoffError("evidence_card template is missing {shortlist}")
    return template.format(shortlist=body)


def render_decision_card(decision: Decision, template: str) -> str:
    """Render the chosen outcome as one Decision Card message."""
    fields = {
        "outcome": decision.outcome.value,
        "confidence": decision.confidence,  # numeric: template uses {confidence:.2f}
        "rationale": decision.rationale,
        "evidence": ", ".join(decision.supporting_evidence) or "none",
    }
    return template.format(**fields)


def render_case_record(record: CaseRecord, template: str) -> str:
    """Render the final audit entry as one Case Record message."""
    fields = {
        "case_id": record.case_id,
        "outcome": record.decision.outcome.value,
        "status": record.status.value,
        "human_decision_by": record.human_decision_by or "pending",
        "notes": "\n".join(f"- {n}" for n in record.notes) or "- none",
    }
    return template.format(**fields)
