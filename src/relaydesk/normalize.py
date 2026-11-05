"""Input normalization: raw room messages -> structured IssueReport.

NOV 5 IMPLEMENTATION NOTE — budget 60-90 minutes, do this FIRST.
The support lead's message is free text; everything downstream depends on
the structured fields this module extracts.

Spec:
  normalize_report(raw_message, author) -> IssueReport
    - pull component / version / error signature with regex patterns you control
    - keep the original text verbatim in raw_channel_message (it is untrusted)
  extract_error_signature(text) -> str | None
    - stable fingerprint of the failure: first error line, HTTP status code,
      exception type. Deterministic: same input -> same signature.
  missing_fields(report) -> list[str]
    - drives CLARIFY: report which required fields are absent
      (component, version, first_seen). Empty list = nothing to ask about.
"""

from __future__ import annotations

import re

from relaydesk.schemas import IssueReport, new_id

# --- Regex patterns for structured field extraction ---

# Component: look for "component: X", "service: X", "[X]" prefix, "in X service", or "X-service"
_COMPONENT_PATTERNS = [
    re.compile(r"(?:component|service)\s*[:=]\s*(\S+)", re.IGNORECASE),
    re.compile(r"^\[([a-zA-Z0-9_-]+)\]", re.MULTILINE),
    re.compile(r"\b([a-zA-Z0-9_-]+-service)\b", re.IGNORECASE),
    re.compile(r"\bin\s+([\w-]+)\s+(?:service|module|api|component)", re.IGNORECASE),
]

# Version: look for "version: X", "v1.2.3", "version 1.2.3"
_VERSION_PATTERNS = [
    re.compile(r"(?:version|ver|v)\s*[:=]?\s*(v?\d+\.\d+(?:\.\d+)?)", re.IGNORECASE),
    re.compile(r"\b(v\d+\.\d+(?:\.\d+)?)\b", re.IGNORECASE),
]

# Date: look for "first seen: YYYY-MM-DD", "since YYYY-MM-DD", ISO dates
_DATE_PATTERNS = [
    re.compile(r"(?:first[\s_]?seen|since|started|from)\s*[:=]?\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
]

# Error signature extractors: specific phrases/quotes first, then exceptions, then HTTP status codes
_ERROR_PATTERNS = [
    re.compile(r"['\"]([^'\"]{4,80})['\"]"),
    re.compile(r"\b(?:error|exception|failure)\s*[:=]?\s*([a-zA-Z0-9_\s-]{4,60})", re.IGNORECASE),
    re.compile(r"\b([A-Z][a-zA-Z]*(?:Error|Exception|Fault|Failure))\b"),
    re.compile(r"(HTTP\s*\d{3}\b)", re.IGNORECASE),
    re.compile(r"\b(\d{3})\s+(?:error|status|response)\b", re.IGNORECASE),
    re.compile(r"\breturns?\s+(\d{3})\b", re.IGNORECASE),
]


def _first_match(patterns: list[re.Pattern], text: str) -> str | None:
    """Return the first capture group from the first matching pattern."""
    for pat in patterns:
        m = pat.search(text)
        if m:
            return m.group(1).strip()
    return None


def extract_error_signature(text: str) -> str | None:
    """Return a deterministic fingerprint of the failure, or None.

    Extracts the first recognizable error indicator: HTTP status codes,
    exception type names, or explicit error messages. Same input always
    produces the same output.
    """
    if not text:
        return None

    # If the text explicitly states no error was shown or present, don't treat it as an error
    if re.search(r"\b(?:no|without)\s+(?:error|exception|crash|traceback)\b", text, re.IGNORECASE):
        # Unless a specific HTTP code or Exception class is also explicitly mentioned
        status_or_exc = _first_match([
            re.compile(r"(HTTP\s*\d{3}\b)", re.IGNORECASE),
            re.compile(r"\b([A-Z][a-zA-Z]*(?:Error|Exception))\b"),
        ], text)
        if status_or_exc:
            return status_or_exc
        return None

    sig = _first_match(_ERROR_PATTERNS, text)
    if sig:
        # Normalize: strip trailing punctuation and sentence continuations, cap at 120 chars.
        sig = sig.split(".")[0].rstrip(".,;:!").strip()[:120]
    return sig or None


def normalize_report(raw_message: str, author: str) -> IssueReport:
    """Parse a raw room message into a structured IssueReport."""
    ver = _first_match(_VERSION_PATTERNS, raw_message)
    if ver and not ver.lower().startswith("v"):
        ver = f"v{ver}"

    return IssueReport(
        report_id=new_id("report"),
        author=author,
        text=raw_message.strip(),
        component=_first_match(_COMPONENT_PATTERNS, raw_message),
        version=ver,
        first_seen=_first_match(_DATE_PATTERNS, raw_message),
        error_signature=extract_error_signature(raw_message),
        raw_channel_message=raw_message,
    )


def missing_fields(report: IssueReport) -> list[str]:
    """Return names of required fields that are absent ('component', ...).

    Drives the CLARIFY path: if the list is non-empty, the decision module
    can ask a targeted clarifying question.
    """
    missing: list[str] = []
    if not report.component:
        missing.append("component")
    if not report.version:
        missing.append("version")
    if not report.first_seen:
        missing.append("first_seen")
    return missing
