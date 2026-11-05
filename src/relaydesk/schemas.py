"""Core data contracts for RelayDesk.

These models are the vocabulary every other module speaks. They are
intentionally dependency-free (stdlib dataclasses + enums) so the project
installs cleanly on a judge's machine. This file is COMPLETE — treat it as
the spec; do not change field names after Nov 4 without updating tests.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class DecisionOutcome(str, Enum):
    """The four supported next actions. This is the product's vocabulary."""

    ANSWER = "ANSWER"
    CLARIFY = "CLARIFY"
    DUPLICATE = "DUPLICATE"
    ESCALATE = "ESCALATE"


class EvidenceType(str, Enum):
    """Kinds of retrievable artifacts in fixtures/."""

    TICKET = "ticket"
    RUNBOOK = "runbook"
    RELEASE_NOTE = "release_note"
    LOG = "log"
    TEST_RESULT = "test_result"


class CaseStatus(str, Enum):
    """Lifecycle of one case as shown in the room's audit trail."""

    TRIAGED = "triaged"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    INVESTIGATING = "investigating"
    AWAITING_HUMAN_APPROVAL = "awaiting_human_approval"
    CLOSED = "closed"


@dataclass
class IssueReport:
    """A customer issue as posted by the support lead in the Switch room."""

    report_id: str
    author: str
    text: str
    component: str | None = None
    version: str | None = None
    first_seen: str | None = None        # ISO date the failure appeared
    error_signature: str | None = None   # error string / trace fingerprint
    raw_channel_message: str = ""        # untrusted original text


@dataclass
class EvidenceItem:
    """One retrievable artifact: ticket, runbook, release note, log, test."""

    evidence_id: str
    evidence_type: EvidenceType
    title: str
    path: str                            # repo-relative path under fixtures/
    component: str | None = None
    version: str | None = None
    date: str | None = None
    error_signature: str | None = None
    body: str = ""                       # treated as UNTRUSTED input
    grounded_answer: str | None = None   # for runbooks: the citable section


@dataclass
class EvidenceFeatures:
    """The four scoring features per (report, evidence) pair.

    Field names mirror the keys in config/policy.yaml `weights`. Keep them
    in sync — scoring.load_weights validates the mapping.
    """

    error_symptom_match: float = 0.0       # 0..1 same observable failure?
    component_version_match: float = 0.0   # 0..1 same service and/or version?
    release_timing_match: float = 0.0      # 0..1 appeared around that change?
    reproduction_evidence: float = 0.0     # 0..1 direct repro / failing test?


@dataclass
class ScoredCandidate:
    """An evidence item plus features, blended score, and a rationale.

    The rationale is what the room sees on the Evidence Card — it must name
    which features drove the score and cite the evidence id.
    """

    evidence: EvidenceItem
    features: EvidenceFeatures
    score: float
    rationale: str


@dataclass
class Decision:
    """The workflow's chosen next action for one report.

    Invariants (asserted by tests/test_decision.py):
      - outcome is always exactly one DecisionOutcome
      - ANSWER/DUPLICATE always carry supporting_evidence ids
      - ANSWER and DUPLICATE require human approval before anything is sent
      - CLARIFY carries a targeted question, never a guess
      - ESCALATE carries an escalation_reason referencing the top evidence
    """

    report_id: str
    outcome: DecisionOutcome
    confidence: float
    draft_response: str | None = None       # required for ANSWER (approved first)
    clarifying_question: str | None = None  # required for CLARIFY
    duplicate_of: str | None = None         # evidence_id, required for DUPLICATE
    escalation_reason: str | None = None    # required for ESCALATE
    supporting_evidence: list[str] = field(default_factory=list)  # evidence ids
    rationale: str = ""
    requires_human_approval: bool = True    # default True: never auto-send


@dataclass
class CaseRecord:
    """Final audit entry posted back to the room after the human decision."""

    case_id: str
    report: IssueReport
    decision: Decision
    status: CaseStatus
    human_decision_by: str = ""
    notes: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


def new_id(prefix: str) -> str:
    """Short readable id like 'case_1a2b3c4d' for room messages."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
