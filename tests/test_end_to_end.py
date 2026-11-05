"""End-to-end integration tests for RelayDesk.

Tests the full lifecycle:
Raw message -> normalize -> retrieve -> score -> decide -> handoff card rendering.
"""

from pathlib import Path
import yaml

from relaydesk.decision import decide
from relaydesk.handoff import (
    load_templates,
    render_case_record,
    render_decision_card,
    render_evidence_card,
)
from relaydesk.normalize import normalize_report
from relaydesk.retrieval import build_index, shortlist
from relaydesk.schemas import (
    CaseRecord,
    CaseStatus,
    DecisionOutcome,
    new_id,
)
from relaydesk.scoring import load_weights, rank_candidates

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_full_pipeline_duplicate():
    policy_path = REPO_ROOT / "config" / "policy.yaml"
    with policy_path.open("r", encoding="utf-8") as fh:
        policy = yaml.safe_load(fh)

    weights = load_weights(policy)
    index = build_index(str(REPO_ROOT / "fixtures"))
    templates = load_templates(REPO_ROOT / "config" / "message_templates.yaml")

    raw_message = (
        "Customer reports checkout failing with HTTP 500 'payment total mismatch' "
        "since this morning. Started right after this week's release. checkout-service v2.14.0"
    )

    report = normalize_report(raw_message, author="support-lead")
    assert report.component == "checkout-service"
    assert report.version == "v2.14.0"

    candidates = shortlist(report, index, k=3)
    assert len(candidates) > 0

    scored = rank_candidates(report, candidates, weights, top_k=3)
    assert len(scored) > 0

    decision = decide(report, scored, policy)
    assert decision.outcome == DecisionOutcome.DUPLICATE
    assert decision.duplicate_of == "INC-1042"

    evidence_card = render_evidence_card(scored, templates["evidence_card"])
    assert "[EVIDENCE]" in evidence_card
    assert "INC-1042" in evidence_card

    decision_card = render_decision_card(decision, templates["decision_card"])
    assert "[DECISION]" in decision_card
    assert "DUPLICATE" in decision_card

    record = CaseRecord(
        case_id=new_id("case"),
        report=report,
        decision=decision,
        status=CaseStatus.CLOSED,
        human_decision_by="chokkaraketankumar",
        notes=["Confirmed duplicate of INC-1042 hotfix"],
    )
    case_record = render_case_record(record, templates["case_record"])
    assert "[CASE]" in case_record
    assert record.case_id in case_record


def test_full_pipeline_answer():
    policy_path = REPO_ROOT / "config" / "policy.yaml"
    with policy_path.open("r", encoding="utf-8") as fh:
        policy = yaml.safe_load(fh)

    weights = load_weights(policy)
    index = build_index(str(REPO_ROOT / "fixtures"))
    templates = load_templates(REPO_ROOT / "config" / "message_templates.yaml")

    raw_message = (
        "Customer hitting HTTP 500 on checkout with error payment processing failed. "
        "They're on v2.14.0 of checkout-service."
    )

    report = normalize_report(raw_message, author="support-lead")
    candidates = shortlist(report, index, k=3)
    scored = rank_candidates(report, candidates, weights, top_k=3)
    decision = decide(report, scored, policy)

    assert decision.outcome == DecisionOutcome.ANSWER
    assert decision.draft_response is not None
    assert decision.requires_human_approval is True

    decision_card = render_decision_card(decision, templates["decision_card"])
    assert "[DECISION]" in decision_card
    assert "ANSWER" in decision_card


def test_full_pipeline_clarify():
    policy_path = REPO_ROOT / "config" / "policy.yaml"
    with policy_path.open("r", encoding="utf-8") as fh:
        policy = yaml.safe_load(fh)

    weights = load_weights(policy)
    index = build_index(str(REPO_ROOT / "fixtures"))
    templates = load_templates(REPO_ROOT / "config" / "message_templates.yaml")

    raw_message = (
        "Customer says the CSV export button in Reports does nothing when clicked. "
        "No error message shown. No app version or browser provided."
    )

    report = normalize_report(raw_message, author="support-lead")
    candidates = shortlist(report, index, k=3)
    scored = rank_candidates(report, candidates, weights, top_k=3)
    decision = decide(report, scored, policy)

    assert decision.outcome == DecisionOutcome.CLARIFY
    assert decision.clarifying_question is not None

    decision_card = render_decision_card(decision, templates["decision_card"])
    assert "[DECISION]" in decision_card
    assert "CLARIFY" in decision_card


def test_full_pipeline_escalate():
    policy_path = REPO_ROOT / "config" / "policy.yaml"
    with policy_path.open("r", encoding="utf-8") as fh:
        policy = yaml.safe_load(fh)

    weights = load_weights(policy)
    index = build_index(str(REPO_ROOT / "fixtures"))
    templates = load_templates(REPO_ROOT / "config" / "message_templates.yaml")

    raw_message = (
        "Fatal exception in notification-service v4.1.0: queue consumer stalled. "
        "New failure after infra deploy."
    )

    report = normalize_report(raw_message, author="support-lead")
    candidates = shortlist(report, index, k=3)
    scored = rank_candidates(report, candidates, weights, top_k=3)
    decision = decide(report, scored, policy)

    assert decision.outcome == DecisionOutcome.ESCALATE
    assert decision.escalation_reason is not None

    decision_card = render_decision_card(decision, templates["decision_card"])
    assert "[DECISION]" in decision_card
    assert "ESCALATE" in decision_card
