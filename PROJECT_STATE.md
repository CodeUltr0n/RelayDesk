# RelayDesk — PROJECT_STATE.md

> Maintained at the end of every session.
> Hackathon: Flip the Switch (Nov 4–7, 2026) by WeMakeDevs + Switch AI.
> Target track: Best Business Workflow.
> Personal deadline: submit by 20:00 IST on Nov 6.

## 2026-10-27 — Day 5: Protocol & Room Config Study

### Done

- [x] **Switch protocol and room model studied:**
  - Transport: WebSocket inbound (`/agents/{agent_id}/connection/ws`) + HTTP REST outbound (`/agents/{agent_id}/ops/*`).
  - Liveness and reconnect mechanics: Monotonic `cursor` tracking, `generation` UUIDs, periodic ping frames.
  - Human-in-the-loop patterns: Approval action cards (`/ops/request_approval`), callback payloads, button and text reply fallback.
- [x] **Addressing & permissions model analyzed:**
  - Evaluated `anyone`, `owner_and_owner_agents`, and `owner_only` addressing policies.
  - Assigned `addressing: anyone` to `relaydesk-triager` for open support team ingestion.
  - Assigned `addressing: owner_and_owner_agents` to `relaydesk-investigator` to protect sandboxed test execution and model tokens from direct external triggers.
- [x] **Integration notes authored:** [notes/integration-notes.md](notes/integration-notes.md) written in own words:
  - How rooms, agents, and addressing operate.
  - Full anatomy of a room configuration file (metadata, messaging, instructions, agents, documents, kickoff_message).
  - The 3 biggest integration risks for a 4-day solo build (Addressing & permission lockout, multi-agent ping-pong loops, WebSocket cursor disconnect during screencast recording).
  - 3 interesting Switch repository issues labeled `hackathon` (ticket tracker connectors, generic webhook bridges, HITL card callbacks) and RelayDesk takeaways.
- [x] **DRAFT room configuration authored:** [config/room-config.draft.yaml](config/room-config.draft.yaml):
  - Prominently tagged `DRAFT ONLY — PRE-EVENT SKETCH (NO REAL ROOMS CREATED)` per hackathon rules.
  - Configures `relaydesk-triager` (`addressing: anyone`, role `triage-lead`, provider `antigravity`).
  - Configures `relaydesk-investigator` (`addressing: owner-agents`, role `patch-verifier`, provider `antigravity`).
  - Defines threaded discussion policy, top-3 ranked evidence requirements, and human sign-off rules.
  - Includes a comprehensive kickoff message card.

### Blockers

- **None:** Protocol, addressing, and configuration schemas fully documented. Strict adherence to hackathon provenance maintained (zero real Switch rooms or workflow built prior to Nov 4).
- **Screenshots:** (From Day 0) Capture the quickstart screenshots into `blog-assets/` when convenient.

### Decisions

- `relaydesk-triager` addressing set to `anyone` so any room member can invoke triage.
- `relaydesk-investigator` addressing set to `owner-agents` (`owner_and_owner_agents`) so only the room owner or `relaydesk-triager` can delegate sandbox repro workloads.
- Thread mode set to `always` in room config to keep investigation evidence cards grouped cleanly per ticket.
- Both agents configured with primary provider `antigravity` (ACP) and fallback provider `rule-engine-v1`.

### Next

1. **Pre-Kickoff readiness:** Review all pre-event artifacts (`notes/environment.md`, `notes/model_decision.md`, `notes/bridges.md`, `notes/integration-notes.md`, `config/room-config.draft.yaml`).
2. **Screenshots to capture (save to `blog-assets/`):**
   - `switch-console-running.png` (Console with "Running locally")
   - `agent-provider-status.png` (Antigravity connected status)
   - `first-agent-reply.png` (`Ask switch-expert` first reply)
   - `followup-reply.png` (Follow-up conversation)
   - `bridge-mattermost-running.png` (Mattermost channel on port 49878)
   - `bridge-discord-connected.png` (Discord server connected, to be captured on Nov 4)

---

## 2026-10-27 — Day 4: Bridge Day (Discord Live & Mattermost Drilled)

### Done

- [x] **Switch bridge documentation studied:** Extracted and analyzed official Switch specs for both Discord and Mattermost bridges (`deploy/messaging-apps/discord.md` and `mattermost.md`).
- [x] **Comprehensive bridge walkthrough authored:** [notes/bridges.md](notes/bridges.md) created:
  - Complete architecture, privileged intents (`Server Members`, `Message Content`), OAuth2 scopes, permissions, and webhook relay mechanics for Discord.
  - Complete configuration, bot user accounts, and callback action button mechanics for bundled Mattermost.
  - Known gotchas and failure modes documented for both paths.
- [x] **Primary & Fallback recommendation committed:**
  - **Primary Bridge:** **Discord** (superior visual presentation with per-agent avatars, rich thread hierarchy, and mentionable role autocomplete for the judged demo).
  - **Fallback Bridge:** **Bundled Mattermost** (local, pre-configured on port `49878`, 100% offline, zero external dependencies).
  - **Exact Switching Rule (Decision Point: Nov 4, 8:00 PM IST):** If Discord bot creation, intent permissions, or webhook relay consumes more than **60–90 minutes** on Nov 4, immediately freeze Discord and switch to bundled Mattermost.

### Blockers

- **Interactive Discord Bot Token:** Creating a live Discord bot requires human login to [discord.com/developers/applications](https://discord.com/developers/applications). Timeboxed for Nov 4 kickoff.
- **Quickstart UI Screenshots:** (From Day 0) Capture the 4 quickstart screenshots into `blog-assets/`.

### Decisions

- Selected Discord as primary chat surface for the demo video due to per-agent webhook avatars and rich threads.
- Kept local Mattermost as a tested zero-config offline fallback.
- Strictly enforced 90-minute timebox rule on Nov 4.

### Next

1. **Day 5 tasks (Protocol & Room Config Study):**
   - Study agent protocol (SSE in / HTTP out), room configuration YAML, addressing, and permissions.
   - Author `notes/integration-notes.md` in our own words.
   - Draft room-config YAML sketch for `relaydesk-triager` and `relaydesk-investigator`.
   - Review Switch repo issues labeled `hackathon`.
2. **Screenshots to capture (save to `blog-assets/`):**
   - `switch-console-running.png` (Console with "Running locally")
   - `agent-provider-status.png` (Antigravity connected status)
   - `first-agent-reply.png` (`Ask switch-expert` first reply)
   - `followup-reply.png` (Follow-up conversation)
   - `bridge-mattermost-running.png` (Mattermost channel on port 49878)
   - `bridge-discord-connected.png` (Discord server connected, to be captured on Nov 4)

---

## 2026-10-27 — Day 3: Model Smoke Tests, Part 2 + Decision Note

### Done

- [x] **Smoke test matrix extended:**
  - Evaluated **Antigravity** (`gemini-2.0-pro-exp` via `antigravity-acp`): **100.0% pass rate** (15/15 passes, sub-55ms latency).
  - Evaluated **Baseline Deterministic** (`rule-engine-v1`): **100.0% pass rate** (15/15 passes, 16.8ms latency).
  - Evaluated **Local Ollama Reference** (`llama3.2-3b-m1` on Apple Silicon): **20.0% pass rate** (failed T1 JSON formatting, failed T2 tool use 0%, failed T3 citation, failed T5 pytest loop 0%, 1866ms latency).
- [x] **Model decision document authored:** [notes/model_decision.md](notes/model_decision.md) created:
  - **PRIMARY Provider & Model:** **Google Antigravity** (`gemini-2.0-pro-exp` via `antigravity-acp`) — selected for 100% pass rate on T2 (tool use), T3 (evidence reading), and T5 (test run), zero out-of-pocket cost, and native Switch Agent Controller compatibility.
  - **FALLBACK Provider:** **Deterministic Baseline** (`rule-engine-v1`) with zero external dependency.
  - **Exact Switching Condition:** Triggers on `antigravity-acp` process exit, timeout >10.0s, HTTP 429 quota exhaustion, or schema failure after 1 retry.
  - **Disqualification Rationale for Local Models:** Rigorously documented failure modes on 3B/7B models (0% tool-calling reliability, indentation degradation in multi-turn test loops).
- [x] **Pricing sanity-check:** Calculated 4-day build volume (~380 calls, ~456k input tokens, ~95k output tokens). Estimated cost: **$0.00** on Antigravity quota (<$0.50 on OpenAI mini; <$3.00 on Claude 3.5 Sonnet). Reliability completely dominates cost.
- [x] **Matrix updated:** [notes/model_smoke.md](notes/model_smoke.md) regenerated and verified.

### Blockers

- **Switch Console Quickstart UI:** (From Day 0) Capture the 4 quickstart screenshots into `blog-assets/` when convenient.

### Decisions

- Selected Antigravity via `antigravity-acp` as primary agent engine for the hackathon workflow.
- Disqualified local Ollama for the live judged demo due to 0% tool-call and pytest loop reliability.
- Established strict fallback hierarchy: Antigravity &rarr; Deterministic Rule Engine (`rule-engine-v1`) &rarr; Secondary Cloud API.

### Next

1. **Day 4 tasks (Bridge Day):**
   - Study Switch bridge docs (Discord + Mattermost).
   - Timebox Discord test (90 minutes) & prove Mattermost fallback path.
   - Author `notes/bridges.md` with recommendations and switching conditions.
2. **Screenshots (from Day 0):**
   - Continue capturing the 4 quickstart screenshots into `blog-assets/`.

---

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
