# RelayDesk — Official 3-Minute Hackathon Demo Video Script

> **Target Track:** Best Business Workflow ($2,000)  
> **Presenter:** Ketan Kumar Chokkara — AI Engineer & Data Scientist from India ([@CodeUltr0n](https://github.com/CodeUltr0n))  
> **Project:** RelayDesk (Evidence-Gated Multi-Agent Support Triage)  
> **Target Duration:** Exactly 3 Minutes (180 seconds)  
> **Surface:** Discord (`#support-triage` via Switch Bridge) + Terminal (`make test` / `make eval-heldout`)

---

## 1. Quick Screen Setup (Before You Hit Record)

- **Left Half of Screen:** Discord channel (`#support-triage`), showing your 4 live executed test runs with `@relaydesk-triager` and `@relaydesk-investigator`.
- **Right Half of Screen:** Clean Terminal window in `/Users/chokkaraketankumar/Downloads/relaydesk_kit/relaydesk-workspace` with large, readable font.
- **Audio:** Clear microphone, steady and confident delivery.

---

## 2. Word-for-Word Spoken Narration & Action Guide

```
TIMECODE: 0:00 – 0:07 | PAPER ANIMATION INTRO
```

### 🎬 Action on Screen:
Play your 7-second custom paper animation (`assets/ketan_paper_animation.mp4`) full screen. Your name and title animate on screen: **Ketan Chokkara — AI Engineer & Data Scientist**.

### 🎙️ Spoken Narration:
> *"Hi everyone! I'm **Ketan Chokkara**, an AI Engineer and Data Scientist from India..."*

---

```
TIMECODE: 0:07 – 0:30 | THE PROBLEM & RELAYDESK OVERVIEW
```

### 🎬 Action on Screen:
Cut/fade smoothly from the animation into your Discord `#support-triage` channel, showing `@relaydesk-triager` and `@relaydesk-investigator` active in the room.

### 🎙️ Spoken Narration:
> *"...and today, I'm excited to present **RelayDesk** — an evidence-gated customer support triage and engineering escalation system built for the **Flip the Switch Hackathon** on **Switch AI**.*
>
> *Every tech company faces a painful trade-off: either support teams over-escalate routine issues and drown engineers in duplicate tickets, or ungrounded AI chatbots hallucinate false answers to customers.*
>
> *RelayDesk solves this by coordinating human leads and autonomous Switch agents in a shared room where **every single triage decision is strictly evidence-gated, and zero customer-facing action is taken without human approval**."*

---

```
TIMECODE: 0:30 – 1:15 | SCENARIO 1: AUTOMATED DUPLICATE TRIAGE
```

### 🎬 Action on Screen:
Point your mouse to the first executed query in Discord:
`@relaydesk-triager Customer reports payment total mismatch (HTTP 500) on checkout-service v2.14.0 since this morning's release.`

Highlight `@relaydesk-triager`'s response cards on screen:
- Parsed report (checkout-service v2.14.0)
- `[EVIDENCE]` Card with `INC-1042` (score 0.86)
- `[DECISION] DUPLICATE` card pausing for human operator approval.

### 🎙️ Spoken Narration:
> *"Let's look at Scenario 1: A customer reports a checkout 500 error after this morning's release.*
>
> *Watch how `@relaydesk-triager` handles this in real-time:*
> 1. *It normalizes the unstructured text, extracting the component, version, and exact error signature.*
> 2. *It queries our knowledge index and renders this **`[EVIDENCE]` Card**.*
> 3. *It computes a multi-feature score of **0.86** driven by symptom and version alignment against open incident **INC-1042**.*
>
> *Because 0.86 exceeds our duplicate threshold of 0.75, it issues a **`[DECISION] DUPLICATE`** card.*
>
> *Notice the critical safety gate: It halts with 'Awaiting human operator approval'. No customer reply is sent, and no ticket is closed until the human support lead signs off. Zero engineering noise."*

---

```
TIMECODE: 1:15 – 2:05 | SCENARIO 2: NOVEL BUG ESCALATION & SANDBOX REPRODUCTION
```

### 🎬 Action on Screen:
Scroll down in Discord to the second executed incident:
`@relaydesk-triager Customer reports discount calculation failure in price_calculator on 10% discount orders. checkout-service v2.14.0. No matching past incident. Please escalate to @relaydesk-investigator to run reproduction tests in the sandbox.`

Highlight:
- `@relaydesk-triager` issuing `[DECISION] ESCALATE` (score 0.70 < 0.75 threshold) and delegating to `@relaydesk-investigator`.
- `@relaydesk-investigator` posting `[REPRODUCTION RESULT] Bug Confirmed` with the exact stack trace (`AssertionError: Got 134.98, expected 134.97`) and root cause (`ROUND_DOWN` vs `ROUND_HALF_UP`).

### 🎙️ Spoken Narration:
> *"Now let's see what happens with a brand-new, novel defect in Scenario 2.*
>
> *Here, a customer reports a discount calculation failure on 10% discount orders. `@relaydesk-triager` evaluates it against our knowledge base. The top candidate score is only 0.70 — below our duplicate threshold. Recognizing this is an unhandled code defect, it selects **`[DECISION] ESCALATE`** and tags our second agent, `@relaydesk-investigator`.*
>
> *This is where Switch's multi-agent power shines:*
> *`@relaydesk-investigator` wakes up via agent-to-agent delegation. Rather than guessing the cause, it copies the service into an **isolated, disposable temporary sandbox** and runs our pytest reproduction suite.*
>
> *Look at the output card:*
> *`[REPRODUCTION RESULT] Bug Confirmed`! It captures the exact assertion failure — **134.98 vs expected 134.97** — and identifies the exact root cause: the discount quantizer was using `ROUND_DOWN` instead of `ROUND_HALF_UP`! It packages a ready-to-fix engineering ticket with full reproduction proof."*

---

```
TIMECODE: 2:05 – 2:30 | SCENARIOS 3 & 4: RUNBOOK ANSWERS & TARGETED CLARIFICATION
```

### 🎬 Action on Screen:
Scroll down to show Scenarios 3 and 4 in Discord:
- **Scenario 3:** Stale search results report -> `@relaydesk-triager` returns `[DECISION] ANSWER (grounded in runbook RB-501)` with exact diagnosis and resolution steps (POST /_aliases and invalidate cache).
- **Scenario 4:** Vague CSV export complaint -> `@relaydesk-triager` returns `[DECISION] CLARIFY (confidence 0.21)` with a single targeted question requesting app version, browser, and console errors.

### 🎙️ Spoken Narration:
> *"RelayDesk completes the full workflow with two more tracks:*
> - *In **Scenario 3**, for stale search results, it grounds a verified answer from **Runbook RB-501**, drafting resolution steps for human approval.*
> - *In **Scenario 4**, when given a vague report with zero technical context, it refuses to hallucinate, issuing a **`[DECISION] CLARIFY`** card with a single targeted diagnostic question.*
>
> *Every outcome is accounted for: Duplicate, Escalate, Answer, and Clarify."*

---

```
TIMECODE: 2:30 – 3:00 | TERMINAL VERIFICATION & WRAP-UP
```

### 🎬 Action on Screen:
Click over to the Terminal and run:
`pytest tests/ -q`
Then run:
`python scripts/run_eval.py --cases fixtures/cases --pipeline relaydesk --split heldout`

### 🎙️ Spoken Narration:
> *"Finally, let's look at the engineering rigor in the terminal:*
> - *All **27 unit, integration, and hardened sandbox tests pass in just 0.2 seconds**.*
> - *Evaluated on our strict held-out benchmark split, RelayDesk delivers **100% decision accuracy, 100% escalation precision, 100% recall**, and zero unsupported assertions with a median latency of **under 0.5 milliseconds**!*
>
> *By combining Switch's multi-agent room collaboration with deterministic safety, RelayDesk eliminates developer alert fatigue while ensuring no real bug ever slips through. The code is open source on GitHub. Thank you to WeMakeDevs and Switch AI!"*

---

## 3. Post-Recording Checklist

- [ ] Video length is between **2:30 and 3:00 minutes** (under the 3-minute limit).
- [ ] Voice audio is clear and audible.
- [ ] Discord text and terminal text are sharp and readable.
- [ ] Upload video to **YouTube (Unlisted or Public)** or **Loom**.
- [ ] Copy the video link into the submission form at [wemakedevs.org/hackathons/switch](https://www.wemakedevs.org/hackathons/switch).
