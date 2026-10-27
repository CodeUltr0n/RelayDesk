# RelayDesk — Protocol & Room Integration Study

_Date: 2026-10-27 | Flip the Switch Hackathon (Day 5 Pre-Event)_

---

## 1. How Rooms, Agents, and Addressing Work in Switch

### The Room as the Shared Coordination Surface
A Switch room is not just a messaging channel or notification feed—it is a shared stateful coordination layer where humans and AI agents collaborate with equal visibility:
- **Every event is ordered:** Human messages, agent evidence cards, triage decisions, approval requests, and sandbox test results appear in a single chronologically consistent room transcript.
- **Auditable provenance:** If a human rejects an escalation, or an agent disputes a duplicate, that debate is memorialized directly in the room history.

### The Wire Protocol: WebSocket (Inbound) + HTTP (Outbound)
- **Transport:** Switch agents connect to the Switch Server (`switch-core`) over a persistent WebSocket connection (`/agents/{agent_id}/connection/ws`) carrying an `Authorization: Bearer <agent_api_key>` header.
- **Event Dispatch:** Inbound room activity (new messages, user mentions, thread replies, button clicks) streams to the agent client over the socket.
- **Outbound Operations:** The agent makes structured HTTP REST calls for every mutation:
  - `POST /agents/{agent_id}/ops/post_message` (posting evidence cards or answers)
  - `POST /agents/{agent_id}/ops/request_approval` (triggering human-in-the-loop action cards)
  - `POST /agents/{agent_id}/ops/update_agent_detail` (setting addressing permissions)
- **Liveness & Resumption:** The client maintains a monotonic `cursor` and `generation` UUID, acknowledging periodic ping frames to confirm active liveness.

### Addressing & Permission Models
Switch enforces strict capability-based addressing rules. Newly registered agents default to `owner_only` (they answer only the registered human owner). To build a reliable multi-agent support workflow, addressing must be configured explicitly:
1. `addressing: anyone`:
   - Any team member or colleague in the room can invoke the agent with `@agent-name`.
   - **Assigned to:** `relaydesk-triager` (so any support lead can post an issue report).
2. `addressing: owner_and_owner_agents`:
   - Only the human owner or designated companion agents owned by the same account can invoke the agent.
   - External participants cannot trigger it directly.
   - **Assigned to:** `relaydesk-investigator` (protects expensive reproduction runs, sandboxed test execution, and model costs from unauthorized triggering).
3. `addressing: owner_only`:
   - Strict lockdown mode for administrative agents.

---

## 2. Anatomy of a Room Configuration File

A Switch room configuration file (YAML format, schema v2) declaratively captures:
- **`metadata`**: Room name, slug, description, and workspace ownership.
- **`messaging`**: Target bridge (`discord` or `mattermost`), channel visibility (`public` or `private`), and bridge-specific webhooks.
- **`instructions`**: The immutable system briefing every agent reads upon entering the room. Sets tone, response formatting (threads vs root), evidence expectations, and safety rules.
- **`agents`**: The registered agents participating in the room, specifying:
  - `name`: Display name and `@` mention tag.
  - `provider`: Underlying AI provider (e.g. `antigravity`, `claude-code`, `opencode`).
  - `addressing`: Permitted instructors (`anyone` vs `owner_and_owner_agents`).
  - `role` / `job`: Designated exclusive responsibility (e.g., `triage-lead`, `patch-verifier`).
- **`documents` & `references`**: Pinned runbooks, schemas, and repository pointers that agents are instructed to consult before answering.
- **`kickoff_message`**: The initial message automatically posted into the channel upon room creation to initialize team context.

---

## 3. The 3 Biggest Integration Risks for a 4-Day Solo Build

### Risk 1: Addressing & Permission Lockout (Silent Refusals)
- **The Failure:** If `relaydesk-investigator` is onboarded with default `owner_only` addressing, when `relaydesk-triager` attempts to hand off a technical regression, Switch will intercept the mention and post a refusal (*"agent-name does not accept instructions from triager"*).
- **Mitigation:** Explicitly configure `relaydesk-investigator` with `addressing: owner_and_owner_agents` during the Nov 4 setup. Verify with a throwaway cross-agent ping before building business logic.

### Risk 2: Multi-Agent Ping-Pong & Unbounded Loops
- **The Failure:** If both agents have open addressing and listen to general channel traffic, Agent A's status post can trigger Agent B, whose reply triggers Agent A again, burning API rate limits and flooding the demo channel.
- **Mitigation:**
  - `relaydesk-triager` only responds to direct `@` mentions or inbound ticket cards.
  - `relaydesk-investigator` only responds when explicitly handed off with an structured `INVESTIGATE` command payload.
  - Enforce human approval gating before any code modification or sandbox reproduction is launched.

### Risk 3: WebSocket Cursor Disconnection During Video Recording
- **The Failure:** If the host machine experiences a momentary socket drop or sleep event during screencast recording, an agent client that fails to resume with its saved `cursor` will drop events or replay previous cards.
- **Mitigation:**
  - Build connection auto-reconnect with backoff in the client adapter.
  - Keep the deterministic rule engine (`rule-engine-v1`) as a zero-socket CLI backup so the demo can proceed without live cloud network dependency if needed.

---

## 4. Switch Repository Issues Labeled `hackathon` (Context Study)

Reviewing `sandbox-quantum/switch` issues labeled `hackathon` highlights community integration patterns:

1. **Issue: Third-Party Ticketing Connectors (e.g., Zendesk / Jira / Linear)**
   - *Context:* Community requests for ingesting support tickets directly from issue trackers into Switch rooms.
   - *RelayDesk Takeaway:* Reinforces our product positioning. Rather than building fragile bi-directional Zendesk sync during a 4-day sprint, RelayDesk ingests synthetic ticket payloads via Switch message cards, focusing 100% on evidence-gated triage quality.
2. **Issue: Custom & Generic Webhook Messaging Bridges**
   - *Context:* Requests for "bring-your-own-chat" webhook endpoints for teams not using Slack/Discord/Teams.
   - *RelayDesk Takeaway:* Confirms our decision to rely on Discord as primary and bundled Mattermost as the 100% local offline fallback.
3. **Issue: Enhanced Human-in-the-Loop Action Card Callbacks**
   - *Context:* Discussions around normalizing button click payloads and status transitions across messaging apps.
   - *RelayDesk Takeaway:* Our card templates in `relaydesk-skeleton/config/message_templates.yaml` must provide both button callbacks AND plain-text numbered options (1/2/3) so the workflow functions identically across Discord and Mattermost.

---

## 5. Pre-Event Draft Room Configuration

A complete declarative room blueprint matching this architecture has been drafted at:
- [`config/room-config.draft.yaml`](file:///Users/chokkaraketankumar/Downloads/relaydesk_kit/relaydesk-workspace/config/room-config.draft.yaml)

Key specifications verified in the draft:
- **Status:** Prominently tagged `DRAFT ONLY — PRE-EVENT SKETCH (NO REAL ROOMS CREATED)` to comply with the hackathon provenance policy.
- **Agent 1:** `relaydesk-triager` configured with `addressing: anyone` so frontline support staff can trigger triage at any time.
- **Agent 2:** `relaydesk-investigator` configured with `addressing: owner-agents` (`owner_and_owner_agents`) so only the room owner or `relaydesk-triager` can delegate sandbox repro workloads.
- **Kickoff Message:** Initial room onboarding banner detailing agent roles, evidence rules, and human-in-the-loop confirmation safeguards.

