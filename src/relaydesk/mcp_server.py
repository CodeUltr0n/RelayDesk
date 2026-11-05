"""Optional MCP (Model Context Protocol) server for RelayDesk.

Exposes RelayDesk's deterministic pipeline as standard MCP tools over stdio
JSON-RPC (zero extra dependencies).

Tools exposed:
  - triage_issue: runs end-to-end normalization, retrieval, scoring, decision
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

from relaydesk.decision import decide
from relaydesk.handoff import (
    load_templates,
    render_decision_card,
    render_evidence_card,
)
from relaydesk.normalize import normalize_report
from relaydesk.retrieval import build_index, shortlist
from relaydesk.scoring import load_weights, rank_candidates

REPO_ROOT = Path(__file__).resolve().parents[2]


class MCPServer:
    """Stdio JSON-RPC MCP server for RelayDesk tools."""

    def __init__(self, corpus_dir: Path | None = None, policy_path: Path | None = None):
        self.corpus_dir = corpus_dir or (REPO_ROOT / "fixtures")
        self.policy_path = policy_path or (REPO_ROOT / "config" / "policy.yaml")
        self.templates_path = REPO_ROOT / "config" / "message_templates.yaml"

        with self.policy_path.open("r", encoding="utf-8") as fh:
            self.policy = yaml.safe_load(fh)
        self.weights = load_weights(self.policy)
        self.index = build_index(str(self.corpus_dir))
        self.templates = load_templates(self.templates_path)

    def triage_issue(self, raw_message: str, author: str = "support-lead") -> dict[str, Any]:
        """Run the full RelayDesk pipeline on an incoming support issue."""
        report = normalize_report(raw_message, author=author)
        candidates = shortlist(report, self.index, k=3)
        scored = rank_candidates(report, candidates, self.weights, top_k=3)
        decision = decide(report, scored, self.policy)

        evidence_card = render_evidence_card(scored, self.templates["evidence_card"])
        decision_card = render_decision_card(decision, self.templates["decision_card"])

        return {
            "report_id": report.report_id,
            "component": report.component,
            "version": report.version,
            "error_signature": report.error_signature,
            "outcome": decision.outcome.value,
            "confidence": round(decision.confidence, 2),
            "duplicate_of": decision.duplicate_of,
            "draft_response": decision.draft_response,
            "clarifying_question": decision.clarifying_question,
            "escalation_reason": decision.escalation_reason,
            "supporting_evidence": decision.supporting_evidence,
            "evidence_card": evidence_card,
            "decision_card": decision_card,
        }

    def handle_request(self, req: dict[str, Any]) -> dict[str, Any] | None:
        """Process a single JSON-RPC request."""
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "relaydesk-mcp", "version": "0.1.0"},
                    "capabilities": {"tools": {}},
                },
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "triage_issue",
                            "description": "Evidence-gated customer support triage and escalation.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "raw_message": {
                                        "type": "string",
                                        "description": "Incoming support report text",
                                    },
                                    "author": {
                                        "type": "string",
                                        "description": "Author username or identifier",
                                    },
                                },
                                "required": ["raw_message"],
                            },
                        }
                    ]
                },
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name == "triage_issue":
                res = self.triage_issue(args.get("raw_message", ""), args.get("author", "support-lead"))
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    },
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }

    def run_stdio(self) -> None:
        """Run standard I/O loop."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                if resp:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
            except Exception as exc:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": str(exc)},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    server = MCPServer()
    server.run_stdio()
