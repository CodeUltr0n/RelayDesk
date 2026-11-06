"""Isolated verification: reproduce + run tests in a disposable copy.

NOV 5/6 IMPLEMENTATION NOTE — OPTIONAL STRETCH. Build only if the
end-to-end flow is already solid (see the fallback table in the plan).
A demo that shows a verified reproduction plus a REJECTED failing patch
is a feature, not a failure. Do not chase auto-fix success rates.

Spec:
  - copy the target service into a temp dir (disposable; never run in place)
  - run ONLY fixed, allow-listed commands (e.g. ["pytest", "-x", "-q"])
  - hard timeout from policy.safety.sandbox.timeout_s; kill on expiry
  - no network: best-effort env flags + document exactly what you enforced
    in docs/safety.md (judges check honesty, not perfection)
  - never touch production credentials, deploy or rollback tooling
  - return TestRunResult; keep only the last max_log_echo_lines of output
    (log content is untrusted — never post it verbatim to the room)
"""

from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestRunResult:
    """Outcome of one sandboxed verification run."""

    passed: bool
    timed_out: bool
    duration_s: float
    log_tail: str  # untrusted content; cap at policy max_log_echo_lines


class SandboxError(RuntimeError):
    """Raised when the sandbox cannot be set up safely."""


# Characters that could be abused for shell injection or chaining.
_FORBIDDEN_SHELL_CHARS = frozenset([";", "&", "|", "`", "$", "(", ")", "<", ">", "\n", "\r"])

# Commands that are allowed to run in the sandbox.
_ALLOWED_COMMANDS = frozenset(["pytest", "python", "python3", "make"])


def _parse_and_validate_command(cmd: str) -> list[str]:
    """Parse command into argv tokens and ensure strictly allow-listed binary with NO shell chaining."""
    if not isinstance(cmd, str) or not cmd.strip():
        raise SandboxError(f"empty or invalid command: {cmd!r}")

    for char in _FORBIDDEN_SHELL_CHARS:
        if char in cmd:
            raise SandboxError(
                f"shell operator or metacharacter {char!r} is strictly forbidden: {cmd!r}"
            )

    try:
        parts = shlex.split(cmd)
    except Exception as exc:
        raise SandboxError(f"failed to parse command tokens: {exc}") from exc

    if not parts:
        raise SandboxError(f"empty command after tokenization: {cmd!r}")

    binary = parts[0]
    if binary not in _ALLOWED_COMMANDS:
        raise SandboxError(
            f"command '{binary}' is not in the allow-list: "
            f"{sorted(_ALLOWED_COMMANDS)}"
        )
    return parts


def _validate_commands(commands: list[str]) -> list[list[str]]:
    """Ensure all commands are valid argv arrays with allow-listed binaries."""
    return [_parse_and_validate_command(cmd) for cmd in commands]


def run_tests(service_dir: str, commands: list[str], policy: dict) -> TestRunResult:
    """Run allow-listed commands on a disposable copy; return the outcome.

    Creates a temporary copy of service_dir, runs each command sequentially
    inside it, enforces a timeout, and returns a TestRunResult with the
    last N lines of combined output (N from policy.safety.max_log_echo_lines).
    """
    parsed_commands = _validate_commands(commands)

    safety = policy.get("safety", {})
    sandbox_cfg = safety.get("sandbox", {})
    timeout_s = int(sandbox_cfg.get("timeout_s", 120))
    max_lines = int(safety.get("max_log_echo_lines", 20))

    # Create disposable copy.
    src_path = Path(service_dir)
    if not src_path.is_dir():
        raise SandboxError(f"service directory not found: {service_dir}")

    tmpdir = tempfile.mkdtemp(prefix="relaydesk_sandbox_")
    work_dir = Path(tmpdir) / src_path.name
    try:
        shutil.copytree(src_path, work_dir)
    except Exception as exc:
        raise SandboxError(f"failed to create disposable copy: {exc}") from exc

    venv_bin = str(Path(sys.executable).parent)
    system_path = "/usr/local/bin:/usr/bin:/bin"
    combined_path = f"{venv_bin}:{system_path}" if venv_bin else system_path

    # Build environment: best-effort network isolation.
    env = {
        "HOME": tmpdir,
        "PATH": combined_path,
        "PYTHONDONTWRITEBYTECODE": "1",
        # Best-effort network isolation flags.
        "no_proxy": "*",
        "http_proxy": "http://127.0.0.1:0",
        "https_proxy": "http://127.0.0.1:0",
    }

    all_output: list[str] = []
    passed = True
    timed_out = False
    start = time.monotonic()

    try:
        for cmd_args in parsed_commands:
            elapsed = time.monotonic() - start
            remaining = max(1, timeout_s - int(elapsed))
            try:
                result = subprocess.run(
                    cmd_args,
                    shell=False,
                    cwd=str(work_dir),
                    capture_output=True,
                    text=True,
                    timeout=remaining,
                    env=env,
                )
                all_output.append(result.stdout)
                all_output.append(result.stderr)
                if result.returncode != 0:
                    passed = False
            except subprocess.TimeoutExpired:
                timed_out = True
                passed = False
                all_output.append(
                    f"[TIMEOUT] Command '{' '.join(cmd_args)}' exceeded {remaining}s"
                )
                break
    finally:
        # Clean up the disposable copy.
        shutil.rmtree(tmpdir, ignore_errors=True)

    duration = time.monotonic() - start
    combined = "\n".join(all_output)
    # Cap output to last max_lines (untrusted content).
    lines = combined.splitlines()
    log_tail = "\n".join(lines[-max_lines:]) if lines else ""

    return TestRunResult(
        passed=passed,
        timed_out=timed_out,
        duration_s=round(duration, 2),
        log_tail=log_tail,
    )
