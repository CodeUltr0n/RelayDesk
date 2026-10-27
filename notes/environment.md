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
| Switch Console | **0.40.1** (released 2026-10-21) |
| Switch Server (bundled) | **0.31.0** (PID 6872, native runtime with PostgreSQL 18) |
| Active Ports | Gateway: `49876`, API: `49877`, Mattermost: `49878`, Postgres: `49879`, Control: `49855` |
| Download | `switch-console-arm64.dmg` (319 MB) from [GitHub releases](https://github.com/sandbox-quantum/switch/releases) |
| Location | `/Applications/Switch Console.app` |
| Status | Installed, launched (PID 5954), local server running |
| Repo | [sandbox-quantum/switch](https://github.com/sandbox-quantum/switch) |
| Docs | [docs.switchagents.ai](https://docs.switchagents.ai) |

### Switch Console Install Steps

1. Downloaded `switch-console-arm64.dmg` from GitHub releases into `/tmp/switch-console-arm64.dmg`.
2. Verified checksum and mounted DMG (`/Volumes/Switch Console 0.40.1-arm64`).
3. Installed `Switch Console.app` to `/Applications/Switch Console.app`.
4. Cleared `com.apple.quarantine` attribute.
5. Ejected DMG image.
6. Launched `Switch Console.app` (`open -a "Switch Console"`).
7. Verified app process (PID 5954) and embedded local server `switch-core` (PID 6872) are active.

## Quickstart: 10-Minute Test Setup (THROWAWAY)

> **This is a smoke-test only — not the hackathon submission.**

### Steps followed (from [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started/index.md)):

1. **Install Switch Console** — ✅ Done (0.40.1 installed in `/Applications`).
2. **Launch & Start Server** — ✅ Done (local server running on ports 49876-49879, agent controller enrolled).
3. **Check AI coding agent status** — In Switch Console sidebar → Settings → Agent providers. Verify your preferred provider (Claude Code, OpenCode, Codex, Cursor, or Antigravity) is connected.
4. **Sign in to Mattermost** — On server Home page → Messaging apps → Mattermost → Sign-in details → Open in Mattermost → Sign in.
5. **Create Switch expert from template** — Sidebar → Templates → Switch expert (Official) → Use → Enable "Start it in a room" → Create agent and room.
6. **Confirm setup:**
   - Open room in Mattermost (room: `Ask switch-expert`).
   - Approve Switch repo download when prompted (`Allow`).
   - Agent replies with introduction.
   - Ask one follow-up question — verify the reply.

**Status:** Server running locally; UI interaction & screenshot capture ready for you.

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
