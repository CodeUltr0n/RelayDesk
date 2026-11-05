"""Tests for the sandbox module."""

from pathlib import Path
import pytest

from relaydesk.sandbox import SandboxError, run_tests

REPO_ROOT = Path(__file__).resolve().parents[1]
BUGGY_SERVICE = REPO_ROOT / "fixtures" / "buggy_service"

POLICY = {
    "safety": {
        "max_log_echo_lines": 20,
        "sandbox": {
            "timeout_s": 30,
            "network": "disabled",
            "disposable_copy": True,
        },
    }
}


def test_sandbox_detects_failing_tests():
    """Buggy service fails test_ten_percent_discount because of ROUND_DOWN bug."""
    result = run_tests(
        str(BUGGY_SERVICE),
        ["pytest -q test_price_calculator.py"],
        POLICY,
    )
    assert result.passed is False
    assert result.timed_out is False
    assert result.duration_s >= 0.0
    assert "AssertionError" in result.log_tail or "FAILED" in result.log_tail


def test_sandbox_rejects_unauthorized_command():
    with pytest.raises(SandboxError):
        run_tests(
            str(BUGGY_SERVICE),
            ["curl https://malicious.example.com"],
            POLICY,
        )


def test_sandbox_rejects_nonexistent_directory():
    with pytest.raises(SandboxError):
        run_tests("/nonexistent/dir", ["python3 -m unittest"], POLICY)
