# RelayDesk 🛎️

> **Evidence-Gated Customer Support Triage and Engineering Escalation**  
> Built for the **Flip the Switch** Hackathon (Nov 4–7, 2026) by **WeMakeDevs** + **Switch AI**  
> **Track:** Best Business Workflow · **Team:** Solo (Ketan Kumar Chokkara)

---

## The Problem

Frontline support teams face a painful trade-off:
1. **Over-escalation:** Support agents escalate routine questions or already-known bugs to engineering, burying developers in duplicate tickets and false alarms.
2. **Under-escalation / Hallucination:** Generic LLM bots try to answer every question, guessing root causes, fabricating diagnostic steps, or sending incorrect advice to frustrated customers.

## The Solution

**RelayDesk** coordinates human support leads and Switch agents in a shared room where every triage decision is strictly **evidence-gated**:

- **`ANSWER`** — Grounded solution citing an exact verified runbook section (confidence $\ge 0.65$).
- **`CLARIFY`** — Targeted clarifying question when reproduction steps, environment, or error signatures are missing.
- **`DUPLICATE`** — Links to an active open incident with symptom, component, and timing evidence (confidence $\ge 0.75$).
- **`ESCALATE`** — Packages novel code defects with sandboxed test execution reproduction evidence for engineering review.

**Zero Unsupported Assertions:** Agents never suggest an outcome without presenting a ranked **`[EVIDENCE]` Card** and obtaining **Human Sign-Off** before customer-facing action is taken.

---

## How Switch is Used (30% Rubric Priority)

Switch is the essential collaboration and audit layer of RelayDesk. If Switch is removed, the multi-agent coordination, human sign-off, and audit trail completely collapse:

1. **Shared Team Room (`relaydesk-triage`):** Support leads, triage agents, and investigation bots interact in a single shared room bridged to Discord or Mattermost.
2. **Explicit Agent Roles & Addressing Policies:**
   - `@relaydesk-triager` (`addressing: anyone`): Public frontline agent. Ingests raw messages, extracts signatures, searches the knowledge base, ranks evidence, and drafts cards.
   - `@relaydesk-investigator` (`addressing: owner_and_owner_agents`): Deep investigation agent. Protected from external triggers; invoked by `@relaydesk-triager` to execute sandboxed test reproduction.
3. **Threaded Audit Trail:** Every customer ticket creates a dedicated room thread holding the `[EVIDENCE]` Card, `[DECISION]` Card, reproduction artifacts, and final `[CASE]` Record.
4. **Mandatory Human Approval:** Triage proposals surface approval callbacks (`/ops/request_approval`), requiring support lead sign-off before customer messages are dispatched.

---

## Architecture

```mermaid
flowchart TD
    A["Support Lead / Customer Report"] -->|"Free Text"| B["normalize.py (Structured Extraction)"]
    B -->|"IssueReport"| C["retrieval.py (Deterministic Index)"]
    D[("Knowledge Corpus: Tickets, Runbooks, Releases, Logs")] --> C
    C -->|"Top-3 Candidates"| E["scoring.py (Feature Blending)"]
    E -->|"Scored Candidates"| F["decision.py (Threshold Routing)"]
    F -->|"Outcome: ANSWER/CLARIFY/DUPLICATE/ESCALATE"| G["handoff.py (Message Card Rendering)"]
    G -->|"Switch Room Feed"| H{"Human-in-the-Loop Approval"}
    H -->|"Approved Fix"| I["Customer Message Dispatched"]
    H -->|"Approved Duplicate"| J["Linked to Active Ticket"]
    H -->|"Approved Escalation"| K["sandbox.py (Isolated Repro Execution)"]
    K -->|"Reproduction Evidence"| L["Engineering Ticket Packaged"]
```

---

## Quickstart & Reproducibility (Under 2 Minutes)

### 1. Environment Requirements
- Python 3.11+
- Git

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/CodeUltr0n/RelayDesk.git
cd RelayDesk

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (zero bloat — pure stdlib + PyYAML)
pip install -e ".[dev]"
```

### 3. Run Test Suite (25 Tests)
```bash
make test
```
*Expected: 25 passed in ~0.25s.*

### 4. Run Benchmark Evaluation
```bash
make eval-relaydesk   # Evaluate on dev split
make eval-heldout     # Evaluate on strict held-out split
```

---

## Benchmark Results

Evaluated using `scripts/run_eval.py` over 8 synthetic support cases:

| Metric | Null Baseline (Always Escalate) | RelayDesk (Dev Split) | RelayDesk (Held-out Split) |
|---|---|---|---|
| **`correct_next_action`** | 25.0% | **100.0%** | **100.0%** |
| **`escalation_precision`** | 25.0% | **100.0%** | **100.0%** |
| **`escalation_recall`** | 100.0% | **100.0%** | **100.0%** |
| **`top3_evidence_recall`** | 50.0% | **100.0%** | **100.0%** |
| **`unsupported_assertion_count`** | 0 | **0** | **0** |
| **`median_latency_ms`** | 0.0 ms | **0.5 ms** | **0.4 ms** |

### Benchmark Takeaway
- **100% Escalation Precision:** Zero false alarms sent to engineering.
- **100% Escalation Recall:** Every genuine technical defect was captured.
- **Sub-Millisecond Latency:** Decisions computed in under 0.5 ms.

---

## Repository Structure

```
relaydesk/
├── config/
│   ├── policy.yaml              # Tunable scoring weights and decision thresholds
│   ├── message_templates.yaml   # UI copy for Evidence, Decision, and Case cards
│   └── room-config.draft.yaml   # Official Switch room configuration
├── src/relaydesk/
│   ├── schemas.py               # Pydantic-free core data contracts
│   ├── normalize.py             # Regex-based extraction of error signatures & components
│   ├── retrieval.py             # Deterministic token containment & metadata index
│   ├── scoring.py               # 4-feature weighted evidence scoring engine
│   ├── decision.py              # Priority decision router
│   ├── handoff.py               # Room card formatting and templating
│   ├── sandbox.py               # Disposable isolated test execution runner
│   └── mcp_server.py            # Stdio JSON-RPC Model Context Protocol server
├── fixtures/
│   ├── tickets/                 # Active (INC-1042) and resolved (INC-1038) tickets
│   ├── runbooks/                # Troubleshooting runbooks with grounded answers
│   ├── releases/                # Deployment changelogs and notes
│   ├── logs/                    # Representative failure log samples
│   ├── cases/                   # Labelled dev and heldout evaluation cases
│   └── buggy_service/           # Deliberately broken service for sandbox reproduction
├── tests/
│   ├── test_schemas.py          # Data contract tests
│   ├── test_scoring.py          # Weight validation and score bounds
│   ├── test_decision.py         # Routing threshold and safety tests
│   ├── test_sandbox.py          # Disposable container test runner verification
│   ├── test_mcp.py              # MCP tool protocol verification
│   └── test_end_to_end.py       # Full lifecycle integration tests
├── docs/
│   ├── architecture.md          # In-depth architectural design
│   ├── evaluation.md            # Detailed benchmark breakdown
│   ├── safety.md                # Security, isolation, and untrusted data model
│   └── demo-script.md           # 3-minute judged screencast walkthrough
├── scripts/
│   └── run_eval.py              # Reproducible benchmark runner
├── Makefile                     # Shortcut targets (test, eval, eval-relaydesk)
└── pyproject.toml               # Minimal packaging configuration
```

---

## Documentation & References

- [Architecture Design](docs/architecture.md)
- [Benchmark Evaluation Report](docs/evaluation.md)
- [Safety & Isolation Model](docs/safety.md)
- [3-Minute Demo Video Script](docs/demo-script.md)
- [Switch Integration Notes](notes/integration-notes.md)
- [Bridge Configuration Guide](notes/bridges.md)
- [Model Evaluation Smoke Tests](notes/model_smoke.md)

---

## License

MIT License. Designed and submitted for the Flip the Switch Hackathon 2026.
