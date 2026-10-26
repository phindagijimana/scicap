"""Public import, agent tool, optional MCP. No model API."""

from __future__ import annotations

import os
from pathlib import Path

from scicap import invoke
from scicap.agent import TOOLS, call_tool
from scicap.mcp import handle_message

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "packages/scicap-neuro/capabilities/neuro.t1.hippocampal_volumes.yaml"
INSTANCE = ROOT / "examples/instances/complete_t1w.json"


def test_public_invoke_allow() -> None:
    os.environ.pop("OPENAI_API_KEY", None)
    result = invoke(CAP, INSTANCE)
    assert result["decision"] == "ALLOW"


def test_agent_tool_matches_invoke() -> None:
    direct = invoke(CAP, INSTANCE)
    via = call_tool("invoke", {"capability": str(CAP), "instance": str(INSTANCE)})
    assert via["decision"] == direct["decision"] == "ALLOW"
    assert {tool["name"] for tool in TOOLS} == {"invoke"}


def test_mcp_tools_call_invoke() -> None:
    listed = handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    names = [tool["name"] for tool in listed["result"]["tools"]]
    assert names == ["invoke"]
    called = handle_message(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "invoke",
                "arguments": {"capability": str(CAP), "instance": str(INSTANCE)},
            },
        }
    )
    assert called["result"]["isError"] is False
    assert "ALLOW" in called["result"]["content"][0]["text"]
