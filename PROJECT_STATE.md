# RelayDesk — PROJECT_STATE.md

> Maintained at the end of every session.
> Hackathon: Flip the Switch (Nov 4–7, 2026) by WeMakeDevs + Switch AI.
> Target track: Best Business Workflow.
> Personal deadline: submit by 20:00 IST on Nov 6.

---

## 2026-10-27 — Day 0: Environment Setup & Skeleton Validation

### Done

- [x] **Workspace created:** `relaydesk-workspace/` with `notes/`, `drafts/`, `blog-assets/` (empty). Git initialized (`git init`).
- [x] **`.gitignore`** configured for Python, Docker, Switch, OS artifacts.
- [x] **Docker verified:**
  - Docker Engine 28.1.1 (build 4eba377), Compose v2.35.1-desktop.1.
  - `docker run hello-world` ✅ passed (arm64v8).
- [x] **Switch Console downloaded:**
  - Version: **0.40.0** (2026-10-20), bundled server **0.31.0**.
  - Downloaded `switch-console-arm64.dmg` from GitHub releases.
  - Install: drag to `/Applications`, signed & notarized.
- [x] **Quickstart documented:** Full 10-minute quickstart steps from official docs written in `notes/environment.md`. Steps are ready for you to follow.
- [x] **Skeleton validated:**
  - `pip install -e ".[dev]"` ✅ (Python 3.11.5 venv)
  - `make test` → **5 passed, 10 failed** (TDD stubs — matches README expectation exactly).
  - `make eval` → null-baseline metric table generated, `results/eval_run.json` written.
- [x] **Environment notes:** `notes/environment.md` has all versions, tool outputs, and quickstart procedure.
- [x] **Reminder:** ⭐ Star the Switch repo ([github.com/sandbox-quantum/switch](https://github.com/sandbox-quantum/switch)) with your GitHub account for the Keychron raffle!

### Blockers

- **Switch Console quickstart not yet run interactively.** The DMG is downloaded but you need to install and run through the quickstart yourself to confirm the agent replies. Steps are documented in `notes/environment.md` under "Quickstart: 10-Minute Test Setup". This is a hands-on task (GUI app + agent reply).

### Decisions

- Skeleton stays **outside** `relaydesk-workspace/` (rules compliance) — will copy pieces in on Nov 4.
- Using Python 3.11.5 for the skeleton venv (matches `requires-python = ">=3.11"`).
- Quickstart will use "Run a server on this computer" (local Docker) + Mattermost (bundled) for the throwaway test — no external messaging app needed.

### Next

#### Manual actions for you:

1. **Install Switch Console:**
   - Open `/tmp/switch-console-arm64.dmg` (or re-download if needed).
   - Drag "Switch Console" to Applications.
   - Launch it.

2. **Run the 10-minute quickstart** (full steps in `notes/environment.md`):
   - Check agent provider status (Settings → Agent providers). You need Claude Code, Codex, or OpenCode installed + signed in.
   - Add server → "Run a server on this computer" → wait for Docker → Start.
   - Sign in to Mattermost (via Home page link).
   - Create Switch expert from template → Start in a room.
   - Wait for agent reply in the "Ask switch-expert" room.
   - Ask one follow-up question.

3. **Star the Switch repo:** Go to [github.com/sandbox-quantum/switch](https://github.com/sandbox-quantum/switch) and click ⭐ Star (Keychron raffle entry).

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
