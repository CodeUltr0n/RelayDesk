"""Tests for the optional MCP server."""

from relaydesk.mcp_server import MCPServer


def test_mcp_initialize():
    server = MCPServer()
    resp = server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert resp["result"]["serverInfo"]["name"] == "relaydesk-mcp"


def test_mcp_tools_list():
    server = MCPServer()
    resp = server.handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = resp["result"]["tools"]
    assert any(t["name"] == "triage_issue" for t in tools)


def test_mcp_tools_call():
    server = MCPServer()
    raw = (
        "Customer reports checkout failing with HTTP 500 'payment total mismatch' "
        "since this morning. Started right after this week's release. checkout-service v2.14.0"
    )
    resp = server.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "triage_issue", "arguments": {"raw_message": raw}},
        }
    )
    assert "result" in resp
    assert "DUPLICATE" in resp["result"]["content"][0]["text"]
