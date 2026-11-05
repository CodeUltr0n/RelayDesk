"""Contract tests for decision routing — EXPECTED RED until Nov 5.

These encode the routing rules from decision.py's docstring with the
thresholds in config/policy.yaml. If you tune thresholds, these tests
must be updated to match — they are the executable spec.
"""

import pytest

from relaydesk.decision import decide
from relaydesk.schemas import (
    DecisionOutcome,
    EvidenceFeatures,
    EvidenceItem,
    EvidenceType,
    IssueReport,
    ScoredCandidate,
)

POLICY = {
    "weights": {
        "error_symptom_match": 0.35,
        "component_version_match": 0.25,
        "release_timing_match": 0.20,
        "reproduction_evidence": 0.20,
    },
    "thresholds": {
        "duplicate_min": 0.75,
        "answer_min": 0.65,
        "clarify_floor": 0.45,
        "top_k_shortlist": 3,
    },
}


def _candidate(score, etype=EvidenceType.TICKET, eid="E1"):
    return ScoredCandidate(
        evidence=EvidenceItem(
            evidence_id=eid, evidence_type=etype, title="t", path="p"
        ),
        features=EvidenceFeatures(),
        score=score,
        rationale="test rationale",
    )


def _report():
    return IssueReport(report_id="R1", author="lead", text="checkout returns 500")


def test_decision_is_always_a_valid_outcome():
    d = decide(_report(), [_candidate(0.8)], POLICY)
    assert isinstance(d.outcome, DecisionOutcome)


def test_high_score_ticket_becomes_duplicate():
    d = decide(_report(), [_candidate(0.90)], POLICY)
    assert d.outcome == DecisionOutcome.DUPLICATE
    assert d.duplicate_of == "E1"
    assert "E1" in d.supporting_evidence


def test_grounded_runbook_above_answer_min_becomes_answer():
    d = decide(_report(), [_candidate(0.70, EvidenceType.RUNBOOK, "E2")], POLICY)
    assert d.outcome == DecisionOutcome.ANSWER
    assert d.supporting_evidence == ["E2"]
    assert d.draft_response  # a draft exists for the human to approve
    assert d.requires_human_approval is True


def test_mid_score_clarifies_with_targeted_question():
    d = decide(_report(), [_candidate(0.50)], POLICY)
    assert d.outcome == DecisionOutcome.CLARIFY
    assert d.clarifying_question  # exactly the thing CLARIFY exists for


def test_low_score_escalates_with_reason():
    d = decide(_report(), [_candidate(0.20)], POLICY)
    assert d.outcome == DecisionOutcome.ESCALATE
    assert d.escalation_reason


def test_never_answer_without_candidates():
    d = decide(_report(), [], POLICY)
    assert d.outcome != DecisionOutcome.ANSWER
