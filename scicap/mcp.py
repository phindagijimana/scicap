"""Optional stdio MCP transport. Calls scicap.invoke only.

Not a Coala/Nipoppy product. Default path is still `scicap invoke` / `from scicap import invoke`.
No model API.
"""

from __future__ import annotations

from scicap import __version__
from scicap.agent import TOOLS, call_tool
from scicap.mcp_stdio import handle_message as _handle
from scicap.mcp_stdio import serve

SERVER = "scicap"


def handle_message(message: dict) -> dict | None:
    return _handle(
        message,
        name=SERVER,
        version=__version__,
        tools=TOOLS,
        call_tool=call_tool,
    )


def main() -> None:
    serve(name=SERVER, version=__version__, tools=TOOLS, call_tool=call_tool)


if __name__ == "__main__":
    main()
