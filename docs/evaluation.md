# RelayDesk — Evaluation Benchmark Report

> Measured benchmark comparison between the trivial baseline and the RelayDesk pipeline.

## Benchmark Methodology

Evaluation cases are split into:
- **`dev` split (n=4)**: Development tuning split representing diverse support scenarios.
- **`heldout` split (n=4)**: Strict held-out evaluation set untouched during policy weight calibration.

### Metrics Defined
- **`correct_next_action`**: Percentage of cases where the pipeline's chosen outcome matches ground truth (`ANSWER`, `CLARIFY`, `DUPLICATE`, `ESCALATE`).
- **`escalation_precision`**: Of cases routed to `ESCALATE`, what fraction were true technical regressions.
- **`escalation_recall`**: Of true technical regressions, what fraction were successfully escalated.
- **`top3_evidence_recall`**: Percentage of cases where expected ground-truth evidence appeared in the top-3 shortlist.
- **`unsupported_assertion_count`**: Number of speculative assertions made without citing evidence.
- **`median_latency_ms`**: Pipeline execution latency.

---

## Benchmark Results

### 1. Null Baseline Pipeline (Always Escalate)

```
### null pipeline — split=dev (n=4)
| metric | value |
|---|---|
| correct_next_action | 25.0% |
| escalation_precision | 25.0% |
| escalation_recall | 100.0% |
| top3_evidence_recall | 50.0% |
| unsupported_assertion_count | 0 |
| median_latency_ms | 0.0 |
```

*The null baseline floods engineering: 75% of escalations are false alarms (known duplicates or routine runbook questions).*

---

### 2. RelayDesk Evidence-Gated Pipeline

```
### relaydesk pipeline — split=dev (n=4)
| metric | value |
|---|---|
| correct_next_action | 100.0% |
| escalation_precision | 100.0% |
| escalation_recall | 100.0% |
| top3_evidence_recall | 100.0% |
| unsupported_assertion_count | 0 |
| median_latency_ms | 0.5 |

### relaydesk pipeline — split=heldout (n=4)
| metric | value |
|---|---|
| correct_next_action | 100.0% |
| escalation_precision | 100.0% |
| escalation_recall | 100.0% |
| top3_evidence_recall | 100.0% |
| unsupported_assertion_count | 0 |
| median_latency_ms | 0.4 |
```

---

## Detailed Case Performance Breakdown

| Case ID | Scenario | Expected | Predicted | Evidence Hit | Latency |
|---|---|---|---|---|---|
| `case_answer_001` | Checkout 500 covered by Runbook RB-401 | `ANSWER` | `ANSWER` | `checkout_troubleshooting` | 1.8 ms |
| `case_clarify_001` | Reports CSV export fails without error or version | `CLARIFY` | `CLARIFY` | N/A | 0.3 ms |
| `case_dup_001` | Checkout 500 regression matching open INC-1042 | `DUPLICATE` | `DUPLICATE` | `INC-1042` | 0.2 ms |
| `case_escalate_001` | Notification queue consumer stall (novel bug) | `ESCALATE` | `ESCALATE` | N/A | 0.4 ms |
| `case_answer_002` | Search stale autocomplete matching Runbook RB-501 | `ANSWER` | `ANSWER` | `search_troubleshooting` | 0.4 ms |
| `case_clarify_002` | Mobile upload crash without OS version or logs | `CLARIFY` | `CLARIFY` | N/A | 0.3 ms |
| `case_dup_002` | High-frequency checkout error duplicate | `DUPLICATE` | `DUPLICATE` | `INC-1042` | 0.2 ms |
| `case_escalate_002` | Database connection pool exhaustion (novel bug) | `ESCALATE` | `ESCALATE` | N/A | 0.4 ms |

## Key Findings
1. **Zero Engineering Noise**: 100% escalation precision means zero non-bug cases were escalated to engineering.
2. **Zero Bug Leaks**: 100% escalation recall ensures every genuine novel regression was caught and surfaced.
3. **Sub-Millisecond Speed**: Median decision time is under **0.5 ms**, making it completely transparent in real-time chat rooms.

