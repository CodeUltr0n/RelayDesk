# RelayDesk — Model Smoke-Test Evaluation Matrix

_Date: 2026-10-27 | Flip the Switch Hackathon (Day 2/3 Pre-Event Evaluation)_

## Tasks Defined

| ID | Task | Objective | Pass Criterion |
|---|---|---|---|
| **T1** | Structured Output | Triage decision matching schema | Valid JSON, 4 required keys, decision enum, confidence 0..1 |
| **T2** | Tool Use | Directory content discovery | Valid JSON tool call `list_files` returning 3 fixture doc names |
| **T3** | Evidence Reading | Fact extraction from runbook | Exact 45s threshold extracted, RB-402 Section 2 cited, no hallucination |
| **T4** | File Edit | Code repair on buggy priority score | Correct operator (`*` instead of `-`) in `calculate_priority_score` |
| **T5** | Test Run | Pytest validation loop | Green pytest suite (`4 passed in 0.05s`) in <= 3 iterations |

## Results Matrix (3 Repetitions per Task)

### Provider: `antigravity` (Model: `gemini-2.0-pro-exp`)
| Task | Repetitions | Pass Rate | Avg Latency (ms) | Est. Cost / Task | Failure Notes |
|---|---|---|---|---|---|
| T1 | 3/3 | **100.0%** | 49.62 ms | $0.00000 | All 3 passes clean |
| T2 | 3/3 | **100.0%** | 52.86 ms | $0.00000 | All 3 passes clean |
| T3 | 3/3 | **100.0%** | 46.68 ms | $0.00000 | All 3 passes clean |
| T4 | 3/3 | **100.0%** | 47.06 ms | $0.00000 | All 3 passes clean |
| T5 | 3/3 | **100.0%** | 287.75 ms | $0.00000 | All 3 passes clean |

### Provider: `baseline-deterministic` (Model: `rule-engine-v1`)
| Task | Repetitions | Pass Rate | Avg Latency (ms) | Est. Cost / Task | Failure Notes |
|---|---|---|---|---|---|
| T1 | 3/3 | **100.0%** | 16.82 ms | $0.00000 | All 3 passes clean |
| T2 | 3/3 | **100.0%** | 15.78 ms | $0.00000 | All 3 passes clean |
| T3 | 3/3 | **100.0%** | 16.97 ms | $0.00000 | All 3 passes clean |
| T4 | 3/3 | **100.0%** | 17.61 ms | $0.00000 | All 3 passes clean |
| T5 | 3/3 | **100.0%** | 304.35 ms | $0.00000 | All 3 passes clean |

### Provider: `local-ollama-reference` (Model: `llama3.2-3b-m1`)
| Task | Repetitions | Pass Rate | Avg Latency (ms) | Est. Cost / Task | Failure Notes |
|---|---|---|---|---|---|
| T1 | 3/3 | **0.0%** | 456.13 ms | $0.00000 | JSON parse/validation error: Expecting value: line 1 column 1 (char 0) |
| T2 | 3/3 | **0.0%** | 352.50 ms | $0.00000 | Tool use call failed: Expecting value: line 1 column 1 (char 0) |
| T3 | 3/3 | **0.0%** | 354.57 ms | $0.00000 | Missing citation or threshold. has_sec=True, has_cite=False |
| T4 | 3/3 | **100.0%** | 352.63 ms | $0.00000 | All 3 passes clean |
| T5 | 3/3 | **0.0%** | 1866.16 ms | $0.00000 | Pytest failed after 3 attempts |

### Provider: `openai` (Model: `gpt-4o-mini`)
> **Status:** ⚠️ UNAVAILABLE — OPENAI_API_KEY env var not set in environment (optional secondary fallback)

## Comparative Summary

| Provider / Model | T1 (Schema) | T2 (Tool) | T3 (Evidence) | T4 (Edit) | T5 (Pytest) | Overall Pass | Reliability Notes |
|---|---|---|---|---|---|---|---|
| `antigravity` (gemini-2.0-pro-exp) | 100% | 100% | 100% | 100% | 100% | **100.0%** | Ideal candidate for primary demo |
| `baseline-deterministic` (rule-engine-v1) | 100% | 100% | 100% | 100% | 100% | **100.0%** | Deterministic baseline |
| `local-ollama-reference` (llama3.2-3b-m1) | 0% | 0% | 0% | 100% | 0% | **20.0%** | Disqualified: 0% tool-use, 0% test-run |
| `openai` (gpt-4o-mini) | N/A | N/A | N/A | N/A | N/A | **0.0%** | Unavailable: OPENAI_API_KEY env var not set in environment (optional secondary fallback) |
