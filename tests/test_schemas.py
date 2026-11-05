"""Schema contract tests — GREEN now (schemas.py is fully implemented)."""

from relaydesk.schemas import (
    CaseStatus,
    DecisionOutcome,
    EvidenceType,
    IssueReport,
    new_id,
)


def test_outcomes_are_exactly_the_four_tracks():
    assert {o.value for o in DecisionOutcome} == {
        "ANSWER",
        "CLARIFY",
        "DUPLICATE",
        "ESCALATE",
    }


def test_evidence_types_match_fixture_dirs():
    assert {t.value for t in EvidenceType} == {
        "ticket",
        "runbook",
        "release_note",
        "log",
        "test_result",
    }


def test_case_status_values():
    assert CaseStatus.AWAITING_HUMAN_APPROVAL.value == "awaiting_human_approval"
    assert CaseStatus.CLOSED.value == "closed"


def test_new_id_has_prefix():
    assert new_id("case").startswith("case_")


def test_report_defaults_are_safe():
    r = IssueReport(report_id="R1", author="lead", text="checkout 500s")
    assert r.component is None
    assert r.version is None
    assert r.raw_channel_message == ""
