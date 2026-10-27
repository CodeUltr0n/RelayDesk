# RelayDesk

> **Evidence-Gated Customer Support Triage**  
> Entry for the **Flip the Switch** hackathon (Nov 4–7, 2026) by **WeMakeDevs** + **Switch AI**  
> **Target Track:** Best Business Workflow

---

## Overview

RelayDesk is an evidence-gated customer support triage system. Working inside Switch rooms with connected AI agents and human reviewers, RelayDesk evaluates inbound customer issues and decides whether an issue should be:

- **ANSWERED** — backed by verified documentation / runbooks.
- **CLARIFIED** — when critical diagnostic information is missing.
- **DUPLICATE** — identified against existing open tickets with similarity evidence.
- **ESCALATED** — routed to engineering with full context and reproduction logs.

Every decision is gated with ranked, verifiable evidence cards — no unsupported assertions.

## Timeline & Rules Compliance

- **Oct 27 – Nov 3 (Pre-Event):** Environment setup, model smoke tests, tooling verification, and architecture planning.
- **Nov 4 – Nov 6 (Hackathon Build):** Switch rooms, agent setup, pipeline implementation, and evaluation benchmarks built during the official event window.
- **Nov 6 (20:00 IST):** Submission deadline.

## Workspace Structure

```
relaydesk-workspace/
├── PROJECT_STATE.md       # Session state, blockers, decisions, and next steps
├── README.md              # Project overview and hackathon track details
├── notes/                 # Environment specs, model smoke tests, architecture notes
│   └── environment.md     # Verified host, Docker, Python, and Switch versions
├── drafts/                # Video scripts and planning documents
└── blog-assets/           # Screenshots, diagrams, and media artifacts
```

## Setup & Verification

See [notes/environment.md](notes/environment.md) for full toolchain versions and verification steps:

- **Docker:** Engine 28.1.1, Compose v2.35.1
- **Python:** >= 3.11
- **Switch Console:** 0.40.1 (arm64)
- **Switch Server:** 0.31.0
