# RelayDesk — Security and Operational Safety Model

> Defensive design principles for AI-assisted support triage and engineering escalation.

## Core Safety Invariants

### 1. Mandatory Human Approval (No Autonomous External Actions)
- `requires_human_approval` defaults to `True` on all `Decision` and `CaseRecord` objects.
- RelayDesk **never** auto-sends messages to customers, never automatically closes Jira/GitHub tickets, and never executes production rollbacks.
- Every proposed response or escalation requires explicit sign-off from a human support lead in the Switch room (`/ops/request_approval` or button callback).

### 2. Untrusted Data Boundary (Prompt Injection Defense)
Customer tickets, error traces, runbooks, and logs are treated as strictly **untrusted external data**:
- **No Instruction Following in Data**: The pipeline treats ticket bodies and log lines purely as string literals for feature extraction. System instructions and routing rules are strictly isolated in Python logic and YAML policies.
- **Log Echo Limits**: `max_log_echo_lines` (default: 20 lines) limits the volume of raw log content presented in chat cards, preventing context window exhaustion or log-based prompt manipulation.

### 3. Disposable Execution Sandbox
When `relaydesk-investigator` runs verification tests on a reported regression:
- **Disposable Temp Copies**: Tests run strictly in an ephemeral temporary directory (`tempfile.mkdtemp`), completely isolated from the working repository.
- **Fixed Command Allow-List**: Only explicitly vetted commands are permitted (`pytest`, `python3`, `make`). Shell command injection and arbitrary binary execution are blocked by `SandboxError`.
- **Hard Timeouts**: Execution is bounded by `policy.safety.sandbox.timeout_s` (120 seconds default), killing processes on expiry.
- **Network Isolation**: Best-effort proxy blackholing (`http_proxy=http://127.0.0.1:0`) prevents outbound telemetry exfiltration or credential leaks during test runs.

### 4. Zero Secrets Exposure
- All evaluation fixtures and tickets use synthetic data.
- No real customer PII, customer credentials, or production tokens exist in the repository or git history.
- The pipeline runs completely offline without sending data to external APIs.
