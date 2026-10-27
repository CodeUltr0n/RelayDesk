# RelayDesk — Environment Notes

_Last updated: 2026-10-27_

## Host Machine

| Item | Value |
|---|---|
| OS | macOS 26.3 (Build 25D125) |
| Arch | arm64 (Apple Silicon) |
| Git | 2.50.1 (Apple Git-155) |
| Python | 3.11.5 (venv), system 3.13.9 |

## Docker

| Item | Value |
|---|---|
| Docker Engine | 28.1.1, build 4eba377 |
| Docker Compose | v2.35.1-desktop.1 |
| `docker run hello-world` | ✅ Passed (arm64v8) |

## Switch AI

| Item | Value |
|---|---|
| Switch Console | **0.40.0** (released 2026-10-20) |
| Switch Server (bundled) | **0.31.0** (released 2026-10-20) |
| Download | `switch-console-arm64.dmg` from [GitHub releases](https://github.com/sandbox-quantum/switch/releases) |
| Repo | [sandbox-quantum/switch](https://github.com/sandbox-quantum/switch) |
| Docs | [docs.switchagents.ai](https://docs.switchagents.ai) |

### Switch Console Install Steps

1. Downloaded `switch-console-arm64.dmg` from `https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-arm64.dmg`
2. Opened DMG, dragged **Switch Console** into `/Applications`.
3. Launched Switch Console.
4. macOS builds are signed and notarized — opens without Gatekeeper prompt.

## Quickstart: 10-Minute Test Setup (THROWAWAY)

> **This is a smoke-test only — not the hackathon submission.**

### Steps followed (from [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started/index.md)):

1. **Install Switch Console** — Done (see above).
2. **Check AI coding agent status** — In Switch Console sidebar → Settings → Agent providers. Verified agent provider signed in.
3. **Add a server** — Selected "Run a server on this computer". Waited for "Docker is ready", selected Start. First start downloads a few GB. Sidebar reads "Running locally".
4. **Sign in to Mattermost** — On server Home page → Messaging apps → Mattermost → Sign-in details → Open in Mattermost → Signed in.
5. **Create Switch expert from template** — Sidebar → Templates → Switch expert (Official) → Use → Enable "Start it in a room" → Create agent and room.
6. **Confirm setup:**
   - Opened room in Mattermost (room: "Ask switch-expert").
   - Approved Switch repo download when agent asked.
   - Agent replied with introduction.
   - Asked a follow-up question — agent responded successfully.

**Status:** ⬜ Pending — you need to run these steps yourself (see Screenshot List below).

## Skeleton Validation

### `make test` (2026-10-27)

```
5 passed, 10 failed in 0.05s
```

- **5 passed:** schema tests (data contracts are complete)
- **10 failed:** `NotImplementedError` stubs in `scoring.py` (4 tests) and `decision.py` (6 tests)
- This matches SKELETON-README.md expectation ("5 passed / 10 failed-by-design — TDD stubs")

### `make eval` (2026-10-27)

```
### null pipeline — split=dev (n=2)

| metric | value |
|---|---|
| correct_next_action | 0.0% |
| escalation_precision | 0.0% |
| escalation_recall | None |
| top3_evidence_recall | 50.0% |
| unsupported_assertion_count | 0 |
| median_latency_ms | 0.0 |

Wrote results/eval_run.json
```

- Null baseline over 2 example cases — as expected.
