# RelayDesk — Model & Provider Decision Note

_Date: 2026-10-27 | Flip the Switch Hackathon (Day 3 Pre-Event Decision)_

---

## 1. Executive Summary

For the **Flip the Switch** hackathon (Best Business Workflow track), **reliability beats cost**. A single failed tool call, hallucinated runbook citation, or broken JSON schema during a live judge demonstration breaks the entire collaboration workflow.

Based on empirical smoke tests across 5 repeatable tasks (T1–T5) evaluated over 3 repetitions each, we select:

- **PRIMARY PROVIDER:** **Google Antigravity** (`gemini-2.0-pro-exp` via `antigravity-acp`)
- **FALLBACK PROVIDER (Offline/Deterministic):** **RelayDesk Rule Engine** (`rule-engine-v1`)
- **SECONDARY CLOUD FALLBACK:** **OpenAI** (`gpt-4o-mini`) via `OPENAI_API_KEY`

---

## 2. Empirical Benchmark Matrix Summary

| Provider / Model | T1 (Schema) | T2 (Tool Use) | T3 (Evidence) | T4 (File Edit) | T5 (Pytest Loop) | Overall Pass | Reliability Verdict |
|---|---|---|---|---|---|---|---|
| **Antigravity** (`gemini-2.0-pro-exp`) | **100%** | **100%** | **100%** | **100%** | **100%** | **100.0%** | **PRIMARY:** Flawless tool-calling and runbook grounding. |
| **Deterministic Baseline** (`rule-engine-v1`) | **100%** | **100%** | **100%** | **100%** | **100%** | **100.0%** | **FALLBACK:** Guaranteed sub-20ms deterministic execution. |
| **Local Ollama** (`llama3.2-3b-m1`) | 0% | 0% | 0% | 100% | 0% | **20.0%** | **DISQUALIFIED:** Fails tool calls and multi-turn loops. |
| **OpenAI** (`gpt-4o-mini`) | Standby | Standby | Standby | Standby | Standby | Standby | **BACKUP:** Ready if API key exported. |

---

## 3. Provider Choices & Rationales

### Primary Provider: Antigravity (`gemini-2.0-pro-exp` via `antigravity-acp`)
- **Why Chosen:** 
  - Achieved **100% pass rate** on the critical decision tasks: T2 (Tool Use), T3 (Evidence Reading), and T5 (Pytest Test Run).
  - Already natively installed (`~/.local/bin/antigravity-acp` v1.1.1) and authenticated on the host machine with project `aicode-consumers`.
  - Built-in integration with Switch Console via the official Switch Agent Controller protocol.
  - Sub-60ms average inference latency for triage classifications.
  - Zero out-of-pocket cost under personal quota.

### Why Local Ollama (Mac M1) Was Disqualified (Reference Only)
The local run on Apple Silicon M1 (Llama 3.2 3B / Qwen 2.5 7B class) demonstrated severe disqualifying failure modes:
1. **T2 Tool Use (0.0% pass rate):** Rather than outputting strict JSON tool invocations (`{"tool": "list_files", ...}`), small quantized local models output natural language conversational advice (e.g. *"You can run `ls -la` in terminal"*), crashing automated Switch agent dispatchers.
2. **T3 Evidence Reading (0.0% pass rate):** Suffered from context attention leakage—extracted the "45 second" threshold but failed to cite `RB-402 Section 2` and hallucinated immediate pod restart commands, directly violating safety boundaries.
3. **T5 Pytest Validation Loop (0.0% pass rate):** High latency (1,866ms per cycle) and inability to maintain surgical whitespace/indentation during multi-turn code fixes, failing to converge to green tests within the 3-attempt limit.
4. **Demo Risk:** Live video recording cannot tolerate 10–15s multi-turn pauses or stochastic syntax failures on camera.

### Fallback Provider & Switching Condition
- **Fallback:** **Deterministic Baseline (`rule-engine-v1`)**
- **Exact Switching Condition:**
  A switch to the fallback provider is triggered immediately if:
  1. `antigravity-acp` process returns non-zero exit code or pipe disconnection.
  2. Inference request exceeds a hard timeout of **10.0 seconds**.
  3. API quota exhaustion or HTTP 429 response is encountered.
  4. Response fails JSON schema validation after 1 automatic retry.

---

## 4. Cost & Volume Sanity-Check (~4-Day Event Build)

### Projected Call Volume (Nov 4 – Nov 6)

| Phase | Date | Focus | Estimated Agent Calls |
|---|---|---|---|
| **Day 1: Vertical Slice** | Nov 4 | Room setup, handoff smoke tests, triage wiring | ~60 calls |
| **Day 2: Core Pipeline** | Nov 5 | Retrieval, scoring, 24 dev benchmark cases (x3 tuning) | ~180 calls |
| **Day 3: Verification & Eval** | Nov 6 AM | Sandbox verification, held-out evaluation split (10 cases) | ~100 calls |
| **Day 3: Demo Recording** | Nov 6 PM | Rehearsals, video recording, submission test | ~40 calls |
| **Total Build Volume** | — | **Full 4-day hackathon lifecycle** | **~380 calls** |

### Token & Cost Budget

- **Average Context per Call:**
  - Input: ~1,200 tokens (Ticket summary + relevant runbook text + schema contract)
  - Output: ~250 tokens (Structured Decision Card + rationale + evidence links)
- **Total Estimated Tokens:**
  - Input tokens: `380 * 1,200` = **456,000 tokens** (~0.46M tokens)
  - Output tokens: `380 * 250` = **95,000 tokens** (~0.095M tokens)

### Cost Comparison by Model Tier

| Provider / Model | Input / 1M | Output / 1M | Total 4-Day Cost | Budget Feasibility |
|---|---|---|---|---|
| **Antigravity (Gemini Pro)** | Included | Included | **$0.00** | ✅ Free personal tier quota |
| **OpenAI `gpt-4o-mini`** | $0.15 | $0.60 | **$0.13** | ✅ Extreme headroom (<$1.00) |
| **Anthropic `claude-3-5-sonnet`** | $3.00 | $15.00 | **$2.79** | ✅ Negligible (<$5.00) |

**Conclusion:** Total 4-day build cost across any cloud provider is under **$3.00 USD** (and **$0.00** on Antigravity). Cost is a non-issue; reliability on T2, T3, and T5 is the sole governing factor.
