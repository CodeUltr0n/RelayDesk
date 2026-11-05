# RelayDesk — 3-Minute Hackathon Demo Script

> Target track: **Best Business Workflow**  
> Total duration: **3 minutes (180 seconds)**  
> Surface: **Switch Console / Discord Room (`relaydesk-triage`)**

---

## Video Outline & Timestamp Guide

| Time | Visual on Screen | Spoken Narration | Key Takeaway |
|---|---|---|---|
| **0:00–0:25** | Switch Console showing `RelayDesk Evidence-Gated Triage Room` with agents `@relaydesk-triager` and `@relaydesk-investigator`. | *"Support teams face a constant dilemma: either escalate too much and overwhelm engineering, or guess answers and miss real bugs. Meet RelayDesk. RelayDesk connects frontline support and Switch agents in a shared room where every triage decision is gated by auditable evidence."* | Clear problem statement; Switch is the collaboration hub. |
| **0:25–1:15** | Support lead pastes a customer checkout 500 error report into the room. `@relaydesk-triager` replies immediately with `[EVIDENCE]` and `[DECISION]` cards. | *"Case 1: A customer reports checkout 500 errors after our morning release. `@relaydesk-triager` normalizes the report, searches our corpus, and produces an Evidence Card. Notice the score breakdown: 0.86 confidence driven by symptom and version match against open ticket INC-1042. RelayDesk proposes DUPLICATE with the exact incident link. The human support lead clicks Approve to link the ticket and close."* | First case: High-confidence duplicate handling with transparent score breakdown and human sign-off. |
| **1:15–2:15** | Support lead pastes a second issue: a novel queue worker stall. `@relaydesk-triager` evaluates it, finds no matching runbook or ticket, and escalates to `@relaydesk-investigator`. | *"Case 2: A novel regression in our notification service. No matching incident exists. RelayDesk refuses to hallucinate a cause and selects ESCALATE. Watch the handoff in Switch: `@relaydesk-triager` delegates to `@relaydesk-investigator`, which spins up an isolated sandbox copy, executes our reproduction test suite, and captures the exact failure log back into the room thread."* | Second case: Real technical escalation; agent-to-agent delegation in Switch room; sandboxed test execution. |
| **2:15–2:45** | Showing the final `[CASE]` audit record and human approval button in the Switch room. | *"Notice why Switch is essential: the shared room is not just a chat feed—it is our team's immutable coordination and audit layer. If you remove Switch, the evidence handoff and human approval loop completely break."* | Direct alignment with 30% "Use of Switch" rubric criterion. |
| **2:45–3:00** | Terminal showing `make eval` running with 100% precision on held-out benchmark and sub-millisecond latency. | *"Our open benchmark proves it: 100% precision on held-out cases with zero false engineering escalations, running deterministically in under half a millisecond. RelayDesk is open source and ready to inspect."* | Strong close with honest, measured benchmark proof. |

---

## Pre-Recording Checklist
- [ ] Switch Console running with `relaydesk-triage-room` initialized.
- [ ] Discord bridge or bundled Mattermost open and connected.
- [ ] Both agents (`@relaydesk-triager`, `@relaydesk-investigator`) active in the room.
- [ ] Terminal open on side with clean font size (for `make test` / `make eval` proof).
- [ ] Microphone tested; no personal tokens or private API keys visible on screen.
