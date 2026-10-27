# RelayDesk — Messaging Bridges Walkthrough & Decision

_Date: 2026-10-27 | Flip the Switch Hackathon (Day 4 Pre-Event)_

---

## 1. Recommendation & Decision Rule

> **RECOMMENDATION LINE:**  
> **Primary bridge: Discord.**  
> **Fallback bridge: Bundled Mattermost (local).**  
> **Switching Condition (Decision Point: Nov 4, 8:00 PM IST):** If Discord bot creation, intent permissions, or webhook relay consumes more than **60–90 minutes** on Nov 4, or if Discord API experiences gateway disconnections, **immediately freeze Discord and switch to bundled Mattermost** so the core triage pipeline is never compromised.

---

## 2. Comparison Matrix

| Feature / Criteria | Discord Bridge | Mattermost Bridge (Bundled) |
|---|---|---|
| **Judge Impression** | **High** (distinct avatars, rich threads, native feel) | **Good** (clean enterprise Slack-like UI) |
| **Agent Identity** | Webhooks with per-agent avatar & display name | Dedicated bot user accounts per agent |
| **Addressing & Mentions** | `@agent-name` with auto-created Discord roles | `@agent-name` in channel; `!` prefix for commands |
| **Setup Overhead** | ~20–30 mins (Dev Portal, OAuth2, Bot Token, Intents) | **0 mins** (pre-bundled with Switch local server) |
| **External Dependency** | Requires Discord account, server, and active internet | **Zero** — 100% offline localhost connection |
| **Interactive Cards** | Thread-based replies and reaction 👀 emoji | Interactive buttons (with Callback Base URL) |
| **Reliability Risk** | Role limit (max 250), Privileged Intent omissions | Untrusted internal connection whitelist setting |

---

## 3. Discord Bridge Walkthrough

### Architecture
Switch establishes an **outbound** gateway connection to Discord. Nothing needs to be publicly reachable on your local network. Switch provisions a webhook for each bridged channel, allowing agents to post under their unique names and avatars.

### Step-by-Step Setup
1. **Create Discord Application & Bot:**
   - Navigate to [discord.com/developers/applications](https://discord.com/developers/applications).
   - Select **New Application** &rarr; name it `RelayDesk Bridge`.
   - Open the **Bot** tab &rarr; click **Reset Token** &rarr; copy the bot token (store securely in shell env/manager; never commit).
2. **Enable Privileged Gateway Intents (CRITICAL):**
   - In Developer Portal under **Bot** &rarr; **Privileged Gateway Intents**, turn ON:
     - `Server Members Intent` (required to resolve members and provision channel permissions).
     - `Message Content Intent` (required for Switch agents to read message text).
   - Click **Save Changes**.
3. **Generate OAuth2 Invite URL:**
   - Under **OAuth2** &rarr; **URL Generator**:
     - Scopes: `bot` + `applications.commands` (enables native slash commands).
     - Bot Permissions:
       - `View Channels`, `Send Messages`, `Send Messages in Threads`
       - `Manage Webhooks` (mandatory for agents to post under their own avatars)
       - `Manage Roles` (mandatory for agent `@mention` autocomplete roles)
       - `Read Message History`, `Attach Files`, `Add Reactions`
   - Copy the generated URL &rarr; open in browser &rarr; authorize the bot into your throwaway test Discord server.
4. **Retrieve Server ID (Guild ID):**
   - In Discord &rarr; User Settings &rarr; Advanced &rarr; enable **Developer Mode**.
   - Right-click server icon &rarr; **Copy Server ID**.
5. **Connect in Switch Console:**
   - Open Switch Console &rarr; Select Local Server &rarr; **Home** &rarr; **Messaging apps** &rarr; **Connect**.
   - Choose **Discord**.
   - Enter Connection Name (e.g., `RelayDesk Discord`), paste **Bot Token** and **Guild Id**.
   - Keep **Agent name autocomplete** enabled.
   - Click **Connect** &rarr; link your personal Discord account (`This is me`).
6. **Turn Channel into a Room:**
   - Create a channel (e.g. `#relaydesk-triage`).
   - Post an ordinary message in the channel (posting initializes the room in Switch Console).
   - In the channel, type `/` to verify Switch commands or invite agents with `@agent-name`.

### Gotchas & Failure Modes
- **Silent Bot (Empty messages):** Occurs if `Message Content Intent` was not toggled in the Developer Portal.
- **Missing Slash Commands:** Occurs if `applications.commands` scope was omitted from the invite URL.
- **Webhook 403 Forbidden:** Occurs if the bot role is placed below other roles or lacks `Manage Webhooks` permission.

---

## 4. Mattermost Bridge Walkthrough (Event Fallback)

### Architecture
Switch Console automatically provisions and connects a bundled Mattermost server on local setups. Each Switch agent receives a dedicated Mattermost bot account that joins channels as a real member.

### Local Server Status
- **Pre-configured Port:** `49878` (verified running under local `switch-core` server).
- **Credentials:** Switch Console &rarr; Server Home &rarr; **Messaging apps** &rarr; Mattermost &rarr; **Sign-in details…** provides instantaneous login.

### Step-by-Step Setup
1. **Access Mattermost:**
   - In Switch Console Server Home &rarr; click **Sign-in details…** on the Mattermost row.
   - Click **Open in Mattermost** and sign in.
2. **Channel to Room Mapping:**
   - Creating a room in Switch automatically creates the corresponding Mattermost channel.
   - Alternatively, add an agent's bot account to an existing channel to turn it into an active room.
3. **Agent Addressing:**
   - Address agents with `@agent-name` in public channels.
   - Open a direct message with the agent's bot user for private 1-on-1 triage drills.
4. **Interactive Action Cards:**
   - Decision and triage cards support interactive approval buttons (`[APPROVE]`, `[REJECT]`).
   - *Requirement:* In Mattermost System Console &rarr; Environment &rarr; Developer, add `localhost` / `127.0.0.1` to **Allow untrusted internal connections to**.

### Gotchas & Failure Modes
- **Slash Commands:** Mattermost does not support Discord-style slash commands for Switch; commands must use the `!` prefix (e.g., `!invite-agent @agent-name`).
- **Button Callbacks:** If `Callback Base Url` is not routable by the Mattermost server, button clicks fail with `Action failed to execute`; typing decision numbers (1/2/3) acts as the zero-config fallback.

---

## 5. Rehearsal & Decision Checklist

- [x] Read Switch official docs on Discord bridge (`deploy/messaging-apps/discord.md`).
- [x] Read Switch official docs on Mattermost bridge (`deploy/messaging-apps/mattermost.md`).
- [x] Verified local Mattermost server running on port `49878`.
- [x] Documented exact setup steps, intents, scopes, and gotchas for both chat paths.
- [x] Hard rule committed: 90-minute timebox on Discord during event build (Nov 4); instant pivot to Mattermost if blocked.
