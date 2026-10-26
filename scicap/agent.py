"""Agent call contract. Same function as `scicap invoke`. Not a dataset skill."""

from __future__ import annotations

from typing import Any

from scicap import invoke

TOOLS: list[dict[str, Any]] = [
    {
        "name": "invoke",
        "description": (
            "Decide whether one capability may be invoked. "
            "Returns ALLOW, REJECT, or ABSTAIN. Missing space is never filled in."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "capability": {
                    "type": "string",
                    "description": "Path to capability YAML",
                },
                "instance": {
                    "type": "string",
                    "description": "Path to instance JSON sidecar",
                },
                "approve": {
                    "type": "boolean",
                    "default": False,
                    "description": "Record approval only; no container pull",
                },
            },
            "required": ["capability", "instance"],
        },
    }
]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name != "invoke":
        raise ValueError(f"unknown tool: {name}")
    return invoke(
        arguments["capability"],
        arguments["instance"],
        approve=bool(arguments.get("approve", False)),
    )
