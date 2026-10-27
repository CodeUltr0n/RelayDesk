# RelayDesk — Model Smoke-Test Evaluation Matrix

_Date: 2026-10-27 | Flip the Switch Hackathon (Day 2 Pre-Event)_

## Tasks Defined

| ID | Task | Objective | Pass Criterion |
|---|---|---|---|
| **T1** | Structured Output | Triage decision matching schema | Valid JSON, 4 required keys, decision enum, confidence 0..1 |
| **T2** | Tool Use | Directory content discovery | Valid JSON tool call `list_files` returning 3 fixture doc names |
| **T3** | Evidence Reading | Fact extraction from runbook | Exact 45s threshold extracted, RB-402 Section 2 cited, no hallucination |
| **T4** | File Edit | Code repair on buggy priority score | Correct operator (`*` instead of `-`) in `calculate_priority_score` |
| **T5** | Test Run | Pytest validation loop | Green pytest suite (`4 passed in 0.05s`) in <= 3 iterations |

## Results Matrix (3 Repetitions per Task)

### Provider: `baseline-deterministic` (Model: `rule-engine-v1`)
| Task | Repetitions | Pass Rate | Avg Latency (ms) | Est. Cost / Task | Failure Notes |
|---|---|---|---|---|---|
| T1 | 3/3 | **100.0%** | 17.69 ms | $0.00000 | All 3 passes clean |
| T2 | 3/3 | **100.0%** | 16.81 ms | $0.00000 | All 3 passes clean |
| T3 | 3/3 | **100.0%** | 17.47 ms | $0.00000 | All 3 passes clean |
| T4 | 3/3 | **100.0%** | 17.25 ms | $0.00000 | All 3 passes clean |
| T5 | 3/3 | **100.0%** | 333.33 ms | $0.00000 | All 3 passes clean |

### Provider: `local-heuristic-fallback` (Model: `heuristic-v1`)
| Task | Repetitions | Pass Rate | Avg Latency (ms) | Est. Cost / Task | Failure Notes |
|---|---|---|---|---|---|
| T1 | 3/3 | **100.0%** | 6.28 ms | $0.00000 | All 3 passes clean |
| T2 | 3/3 | **100.0%** | 6.57 ms | $0.00000 | All 3 passes clean |
| T3 | 3/3 | **100.0%** | 6.16 ms | $0.00000 | All 3 passes clean |
| T4 | 3/3 | **100.0%** | 6.35 ms | $0.00000 | All 3 passes clean |
| T5 | 3/3 | **100.0%** | 276.88 ms | $0.00000 | All 3 passes clean |

### Provider: `openai` (Model: `gpt-4o-mini`)
> **Status:** ⚠️ UNAVAILABLE — OPENAI_API_KEY env var not set in environment

### Provider: `google-gemini` (Model: `gemini-2.0-flash`)
> **Status:** ⚠️ UNAVAILABLE — GEMINI_API_KEY / GOOGLE_API_KEY env var not set in environment

## Comparative Summary

| Provider / Model | T1 (Schema) | T2 (Tool) | T3 (Evidence) | T4 (Edit) | T5 (Pytest) | Overall Pass | Reliability Notes |
|---|---|---|---|---|---|---|---|
| `baseline-deterministic` (rule-engine-v1) | 100% | 100% | 100% | 100% | 100% | **100.0%** | Verified deterministic harness execution |
| `local-heuristic-fallback` (heuristic-v1) | 100% | 100% | 100% | 100% | 100% | **100.0%** | Verified deterministic harness execution |
| `openai` (gpt-4o-mini) | N/A | N/A | N/A | N/A | N/A | **0.0%** | Unavailable: OPENAI_API_KEY env var not set in environment |
| `google-gemini` (gemini-2.0-flash) | N/A | N/A | N/A | N/A | N/A | **0.0%** | Unavailable: GEMINI_API_KEY / GOOGLE_API_KEY env var not set in environment |
