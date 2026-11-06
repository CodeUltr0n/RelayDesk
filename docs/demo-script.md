# RelayDesk — Official 3-Minute Hackathon Demo Video Script

> **Target Track:** Best Business Workflow ($2,000)  
> **Presenter:** Ketan Kumar Chokkara — AI Engineer & Data Scientist from India ([@CodeUltr0n](https://github.com/CodeUltr0n))  
> **Project:** RelayDesk (Evidence-Gated Multi-Agent Support Triage)  
> **Target Duration:** Exactly 3 Minutes (180 seconds)  
> **Surface:** Discord (`#support-triage` via Switch Bridge) + Terminal (`make test` / `make eval-heldout`)

---

## 1. Quick Screen Setup (Before You Hit Record)

- **Left Half of Screen:** Discord channel (`#support-triage`), showing your live conversation with `@relaydesk-triager` and `@relaydesk-investigator`.
- **Right Half of Screen:** Clean Terminal window in `/Users/chokkaraketankumar/Downloads/relaydesk_kit/relaydesk-workspace` with large, readable font.
- **Audio:** Clear microphone, speak at a confident, steady, natural pace.

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
TIMECODE: 0:07 – 0:35 | THE PROBLEM & RELAYDESK OVERVIEW
```

### 🎬 Action on Screen:
Cut/fade smoothly from the animation into your Discord `#support-triage` channel, showing `@relaydesk-triager` and `@relaydesk-investigator` ready in the room.

### 🎙️ Spoken Narration:
> *"...and today, I'm excited to present **RelayDesk** — an evidence-gated customer support triage and engineering escalation system built for the **Flip the Switch Hackathon** on **Switch AI**.*
>
> *Every tech company faces a painful trade-off: either support teams over-escalate routine issues and drown engineers in duplicate tickets, or ungrounded AI chatbots hallucinate false answers to customers.*
>
> *RelayDesk solves this by coordinating human leads and autonomous Switch agents in a shared room where **every single triage decision is strictly evidence-gated, and zero customer-facing action is taken without human approval**."*

---

```
TIMECODE: 0:30 – 1:20 | SCENARIO 1: AUTOMATED DUPLICATE TRIAGE
```

### 🎬 Action on Screen:
Scroll to the first message in Discord from Ketan to `@relaydesk-triager`:
`@relaydesk-triager Customer reports payment total mismatch (HTTP 500) on checkout-service v2.14.0 since this morning's release.`

### 🎙️ Spoken Narration:
> *"Let's look at Scenario 1: A customer reports a checkout 500 error after this morning's release.*
>
> *Watch how our first agent, `@relaydesk-triager`, handles this in real-time:*
> 1. *It normalizes the unstructured text, extracting the component, version, and exact error signature.*
> 2. *It queries our deterministic knowledge index and renders this formatted **`[EVIDENCE]` Card**.*
> 3. *It computes a multi-feature score of **0.86** driven by symptom and version alignment against open incident **INC-1042**.*
>
> *Because 0.86 exceeds our duplicate threshold of 0.75, it issues a **`[DECISION] DUPLICATE`** card.*
>
> *Notice the critical safety gate: It halts with 'Awaiting human operator approval'. No customer reply is sent, and no ticket is closed until the human support lead signs off. Zero engineering noise."*

---

```
TIMECODE: 1:20 – 2:25 | SCENARIO 2: NOVEL BUG ESCALATION & SANDBOX REPRODUCTION
```

### 🎬 Action on Screen:
Scroll down in Discord to the second incident message:
`@relaydesk-triager Customer reports discount calculation failure in price_calculator on 10% discount orders. checkout-service v2.14.0. No matching past incident. Please escalate to @relaydesk-investigator to run reproduction tests in the sandbox.`

### 🎙️ Spoken Narration:
> *"Now let's see what happens with a brand new, novel defect in Scenario 2.*
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
TIMECODE: 2:25 – 2:45 | WHY SWITCH AI IS ESSENTIAL (RUBRIC FOCUS)
```

### 🎬 Action on Screen:
Show the multi-agent thread in Discord, highlighting both bots and human collaborating together in one room.

### 🎙️ Spoken Narration:
> *"Switch is the essential collaboration layer of RelayDesk. If you remove Switch, this workflow collapses:*
> - *It gives us specialized agent addressing policies: `@relaydesk-triager` is public to the team, while `@relaydesk-investigator` is protected and only invoked for technical reproduction.*
> - *It bridges Discord into an immutable audit room where human leads and AI agents collaborate seamlessly in threads.*
> - *It enforces the human-in-the-loop approval boundary that enterprise software demands."*

---

```
TIMECODE: 2:45 – 3:00 | TERMINAL BENCHMARK PROOF & WRAP-UP
```

### 🎬 Action on Screen:
Click over to the Terminal and run:
`make test`
Then run:
`make eval-heldout`

### 🎙️ Spoken Narration:
> *"Finally, let's look at the engineering rigor in the terminal:*
> - *`make test` — all **25 unit, integration, and sandbox tests pass in just 0.2 seconds**.*
> - *`make eval-heldout` — evaluated on our strict held-out benchmark split, RelayDesk delivers **100% decision accuracy, 100% escalation precision, and 100% recall** with a median latency of **under 0.5 milliseconds**!*
>
> *RelayDesk eliminates engineering alert fatigue while ensuring no real bug ever slips through. The code is open source on GitHub. Thank you to WeMakeDevs and Switch AI!"*

---

## 3. Post-Recording Checklist

- [ ] Video length is between **2:30 and 3:00 minutes** (under the 3-minute limit).
- [ ] Voice audio is clear and audible.
- [ ] Discord text and terminal text are sharp and readable.
- [ ] Upload video to **YouTube (Unlisted or Public)** or **Loom**.
- [ ] Copy the video link into the submission form at [wemakedevs.org/hackathons/switch](https://www.wemakedevs.org/hackathons/switch).
