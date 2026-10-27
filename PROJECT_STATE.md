# RelayDesk — PROJECT_STATE.md

> Maintained at the end of every session.
> Hackathon: Flip the Switch (Nov 4–7, 2026) by WeMakeDevs + Switch AI.
> Target track: Best Business Workflow.
> Personal deadline: submit by 20:00 IST on Nov 6.

## 2026-10-27 — Day 2: Model Smoke Tests, Part 1

### Done

- [x] **Smoke test harness built:** `notes/smoke_runner.py` created to run 5 repeatable tasks across candidate providers with 3 repetitions each.
- [x] **Smoke test fixtures created:** `notes/smoke_fixtures/` populated with:
  - `schema_t1.json` & `input_t1.json`: Triage schema validation fixture for T1.
  - `docs/` (`auth_guide.md`, `rate_limits.md`, `database_errors.md`): File discovery fixture for T2.
  - `runbook_snippet.md`: Factual runbook extraction (RB-402, 45.0s timeout, section citation) for T3.
  - `broken_code.py` & `test_broken_code.py`: Priority score calculation bug & pytest validation suite for T4 & T5.
- [x] **Ran smoke tests for 2 available providers:**
  - `baseline-deterministic` (`rule-engine-v1`): **100.0% pass rate** (15/15 passes, avg latency 17.2ms).
  - `local-heuristic-fallback` (`heuristic-v1`): **100.0% pass rate** (15/15 passes, avg latency 6.3ms).
- [x] **External cloud provider status recorded:** Checked environment for cloud providers; recorded `OPENAI_API_KEY` and `GEMINI_API_KEY` status as unavailable in local shell.
- [x] **Matrix documented:** Complete matrix with latencies, cost, pass rates, and failure notes recorded in `notes/model_smoke.md`.

### Blockers

- **Optional Provider API Keys:** If you want live cloud provider benchmarks included alongside the local runners, provide the environment variable name (`OPENAI_API_KEY` or `GEMINI_API_KEY`). Not a hard blocker — harness works completely autonomously.
- **Switch Console Quickstart UI:** (From Day 0) Capture the 4 quickstart screenshots when convenient.

### Decisions

- T3 requires strict citation of runbook section and exact parameter value; unauthorized immediate retries flag as hallucination.
- T5 test runner requires clean pytest pass within 3 iterations; sandbox cleanup is automated per attempt.
- Harness stays inside `notes/` as a pre-event evaluation tool (clean separation from submission pipeline).

### Next

1. **Day 3 tasks:**
   - Extend matrix to a 3rd provider and document local Ollama reference.
   - Author `notes/model_decision.md` with primary & fallback provider selection, trigger conditions, and 4-day cost projection.
2. **Screenshots (from Day 0):**
   - Capture the 4 quickstart screenshots into `blog-assets/` (`switch-console-running.png`, `agent-provider-status.png`, `first-agent-reply.png`, `followup-reply.png`).

---

## 2026-10-27 — Day 0: Environment Setup & Skeleton Validation

### Done

- [x] **Workspace created & pushed to GitHub:**
  - `relaydesk-workspace/` initialized with `notes/`, `drafts/`, `blog-assets/`, and `README.md`.
  - Remote set to `https://github.com/CodeUltr0n/RelayDesk.git`.
  - Pushed to `origin/main` (commit `67e8e05`).
  - `relaydesk-skeleton/` remains strictly outside the repository per hackathon rules.
- [x] **`.gitignore`** configured for Python, Docker, Switch, OS artifacts.
- [x] **Docker verified:**
  - Docker Engine 28.1.1 (build 4eba377), Compose v2.35.1-desktop.1.
  - `docker run hello-world` ✅ passed (arm64v8).
- [x] **Switch Console installed & running:**
  - Version: **0.40.1** (arm64, released 2026-10-21), bundled server **0.31.0**.
  - Downloaded `switch-console-arm64.dmg` (320 MB) from GitHub releases.
  - Installed to `/Applications/Switch Console.app` and launched (PID 5954).
  - Local embedded server running (`switch-core` PID 6872 on port `49877`, PostgreSQL 18 on `49879`, Gateway `49876`, Mattermost `49878`).
  - Embedded agent controller enrolled and connected.
- [x] **Quickstart documented & pre-configured:** Full 10-minute quickstart steps from official docs written in `notes/environment.md`. Local server is already up and listening.
- [x] **Skeleton validated:**
  - `pip install -e ".[dev]"` ✅ (Python 3.11.5 venv)
  - `make test` → **5 passed, 10 failed** (TDD stubs — matches README expectation exactly).
  - `make eval` → null-baseline metric table generated, `results/eval_run.json` written.
- [x] **Environment notes:** `notes/environment.md` updated with exact versions, ports, tool outputs, and quickstart procedure.
- [x] **Reminder:** ⭐ Star the Switch repo ([github.com/sandbox-quantum/switch](https://github.com/sandbox-quantum/switch)) with your GitHub account for the Keychron raffle!

### Blockers

- **Throwaway Agent Reply Verification in GUI:** Switch Console and the local server are running. You need to perform the quick interactive GUI check:
  1. Open Switch Console (already running in your dock/menu bar).
  2. In **Settings → Agent providers**, verify your signed-in provider (Claude Code, OpenCode, Codex, Cursor, or Antigravity).
  3. In **Templates**, select **Switch expert (Official)** → **Use** → check **Start it in a room** → **Create agent and room**.
  4. In the opened Mattermost / Console room (`Ask switch-expert`), approve the Switch repository download (`Allow`), and receive the first agent reply. Ask one follow-up question.

### Decisions

- Skeleton stays **outside** `relaydesk-workspace/` (rules compliance) — will copy pieces in on Nov 4.
- Using Python 3.11.5 for the skeleton venv (matches `requires-python = ">=3.11"`).
- Switch Console is running with the native runtime + local PostgreSQL 18.
- Throwaway test setup uses the official Switch expert template and Mattermost channel to keep things strictly separated from the hackathon submission workflow.

### Next

#### Manual actions for you (10 minutes):

1. **Verify agent provider & room reply in Switch Console:**
   - Bring **Switch Console** to front (running from `/Applications/Switch Console.app`).
   - Navigate to **Templates** → **Switch expert** → **Use** → check **Start it in a room** → **Create agent and room**.
   - If prompted for repo download permission, click **Allow**.
   - Send `@switch-expert hello` or read its initial greeting, then send a follow-up question.

2. **Star the Switch repo:** Go to [github.com/sandbox-quantum/switch](https://github.com/sandbox-quantum/switch) and click ⭐ Star (Keychron raffle entry).

#### Screenshots to capture (save to `blog-assets/`):

| # | What to capture | Filename suggestion |
|---|---|---|
| 1 | Switch Console main screen after server is running (sidebar showing "Running locally") | `switch-console-running.png` |
| 2 | Agent provider status showing signed-in agent | `agent-provider-status.png` |
| 3 | The "Ask switch-expert" room with the agent's first reply visible | `first-agent-reply.png` |
| 4 | Your follow-up question and the agent's response | `followup-reply.png` |

#### Git commit:
```bash
cd relaydesk-workspace && git add -A && git commit -m "Day 0: workspace init, environment notes, project state"
```

---

## Timeline Reference

| Date | Phase | Key deliverables |
|---|---|---|
| Oct 27 – Nov 3 | Pre-event prep | Environment, planning, skeleton validation (no Switch workflow) |
| Nov 4 | Event day 1 | Switch rooms/agents built, copy skeleton in, begin implementation |
| Nov 5 | Event day 2 | Full pipeline: normalize → retrieval → scoring → decision → handoff |
| Nov 6 (by 20:00 IST) | Submit | Demo video, final eval, fresh-clone test, submission |
| Nov 7 | Travel | No work planned |
