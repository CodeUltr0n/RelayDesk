"""Decision routing: map a scored shortlist to exactly one of the four outcomes.

NOV 5 IMPLEMENTATION NOTE — budget 2 hours, driven by tests/test_decision.py.
Build the ANSWER and ESCALATE paths FIRST; add CLARIFY and DUPLICATE only
if you are on schedule (they are small once the first two exist).

Routing rules (thresholds come from config/policy.yaml — never hardcode):

  1. DUPLICATE  best candidate is a past ticket AND score >= duplicate_min
                -> decision.duplicate_of = that evidence_id
  2. ANSWER     grounded runbook/evidence exists AND score >= answer_min
                -> draft_response MUST cite the evidence id/path;
                   requires_human_approval stays True
  3. CLARIFY    top score >= clarify_floor but below the ANSWER/DUPLICATE
                bars, OR normalize.missing_fields() is non-empty
                -> clarifying_question must be targeted (one question)
  4. ESCALATE   nothing above fired
                -> escalation_reason references the top evidence

Safety invariants (tests assert these):
  - output is always exactly one DecisionOutcome
  - ANSWER/DUPLICATE always carry supporting_evidence ids
  - never ANSWER when the shortlist has zero grounded candidates
  - untrusted text (ticket/log bodies) is never echoed verbatim into
    clarifying questions — paraphrase, and cap length
"""

from __future__ import annotations

from relaydesk.schemas import (
    Decision,
    DecisionOutcome,
    EvidenceType,
    IssueReport,
    ScoredCandidate,
)

# Evidence types that count as "grounded" for ANSWER decisions.
_GROUNDABLE_TYPES = frozenset(
    [EvidenceType.RUNBOOK, EvidenceType.RELEASE_NOTE, EvidenceType.TEST_RESULT]
)


class DecisionError(RuntimeError):
    """Raised when routing rules receive malformed inputs."""


def decide(
    report: IssueReport, shortlist: list[ScoredCandidate], policy: dict
) -> Decision:
    """Apply the routing rules in order; return exactly one Decision."""
    thresholds = policy.get("thresholds", {})
    duplicate_min = float(thresholds.get("duplicate_min", 0.75))
    answer_min = float(thresholds.get("answer_min", 0.65))
    clarify_floor = float(thresholds.get("clarify_floor", 0.45))

    # --- Empty shortlist: always ESCALATE (never ANSWER without evidence) ---
    if not shortlist:
        return Decision(
            report_id=report.report_id,
            outcome=DecisionOutcome.ESCALATE,
            confidence=0.0,
            escalation_reason=(
                "No matching evidence found in the knowledge base. "
                "Escalating to engineering for manual investigation."
            ),
            rationale="Empty shortlist — no candidates to evaluate.",
        )

    best = shortlist[0]  # Already ranked: highest score first.

    # --- Rule 1: DUPLICATE ---
    # Best candidate is an active/open past ticket AND score >= duplicate_min.
    # Resolved tickets represent past fixed issues (used for answers/runbooks, not duplicate grouping).
    if (
        best.score >= duplicate_min
        and best.evidence.evidence_type == EvidenceType.TICKET
        and "[status: resolved]" not in best.evidence.body.lower()
    ):
        return Decision(
            report_id=report.report_id,
            outcome=DecisionOutcome.DUPLICATE,
            confidence=best.score,
            duplicate_of=best.evidence.evidence_id,
            supporting_evidence=[best.evidence.evidence_id],
            rationale=(
                f"Top candidate [{best.evidence.evidence_id}] is an active ticket "
                f"with score {best.score:.2f} >= duplicate threshold {duplicate_min}. "
                f"Suggesting duplicate of ongoing issue."
            ),
            requires_human_approval=True,
        )

    # --- Rule 2: ANSWER ---
    # Grounded evidence exists AND score >= answer_min.
    # Check if the best candidate or any grounded candidate meets the bar.
    grounded = [
        sc for sc in shortlist
        if sc.evidence.evidence_type in _GROUNDABLE_TYPES and sc.score >= answer_min
    ]
    if grounded:
        top_grounded = grounded[0]
        ev = top_grounded.evidence
        cite = ev.grounded_answer or ev.title
        draft = (
            f"Based on [{ev.evidence_id}] ({ev.evidence_type.value}): {cite}. "
            f"Please verify this addresses the reported issue before sending."
        )
        return Decision(
            report_id=report.report_id,
            outcome=DecisionOutcome.ANSWER,
            confidence=top_grounded.score,
            draft_response=draft,
            supporting_evidence=[ev.evidence_id],
            rationale=(
                f"Grounded evidence [{ev.evidence_id}] "
                f"({ev.evidence_type.value}) with score {top_grounded.score:.2f} "
                f">= answer threshold {answer_min}."
            ),
            requires_human_approval=True,
        )

    # --- Rule 3: CLARIFY ---
    from relaydesk.normalize import extract_error_signature, missing_fields

    sig = report.error_signature or extract_error_signature(report.text)
    gaps = missing_fields(report)
    has_full_technical_signals = bool(report.component and report.version and sig and not gaps)

    # Only request clarification if there are genuine context gaps or missing technical signals.
    # If the user already provided full technical signals and no existing ticket/runbook covers it,
    # it is a novel defect that must be escalated for investigation, not stalled with redundant questions.
    if not has_full_technical_signals and (best.score >= clarify_floor or (sig is None and gaps)):
        missing_str = ", ".join(gaps) if gaps else "reproduction details"
        return Decision(
            report_id=report.report_id,
            outcome=DecisionOutcome.CLARIFY,
            confidence=best.score,
            clarifying_question=(
                f"Could you provide more details regarding {missing_str} "
                f"and any error messages or reproduction steps? "
                f"This will help us resolve the issue."
            ),
            supporting_evidence=[best.evidence.evidence_id],
            rationale=(
                f"Incomplete technical context ({missing_str}) with candidate score {best.score:.2f}. "
                f"Requesting targeted clarification from the user."
            ),
        )

    # --- Rule 4: ESCALATE (fallback for novel defects or unconfident matches) ---
    escalation_reason = (
        f"Novel defect in {report.component or 'service'} {report.version or ''}: "
        f"top evidence scored {best.score:.2f}, below duplicate threshold {duplicate_min}. "
        f"Escalating to engineering for sandbox reproduction and fix."
        if has_full_technical_signals
        else f"Top evidence [{best.evidence.evidence_id}] scored only {best.score:.2f}, below clarify floor {clarify_floor}. "
        f"No confident match found — escalating to engineering."
    )
    return Decision(
        report_id=report.report_id,
        outcome=DecisionOutcome.ESCALATE,
        confidence=best.score,
        escalation_reason=escalation_reason,
        supporting_evidence=[best.evidence.evidence_id],
        rationale=(
            "Full technical context provided but no confident match — novel defect."
            if has_full_technical_signals
            else f"All candidates below clarify floor {clarify_floor}. Escalating for manual engineering review."
        ),
    )
