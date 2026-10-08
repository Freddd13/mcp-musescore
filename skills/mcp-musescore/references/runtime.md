# Runtime and CLI helpers

## Tested dependency line

The repository currently declares:

```text
fastmcp>=4,<5
websockets
```

`server.py` imports `from fastmcp import FastMCP` (standalone FastMCP 4, built on MCP SDK v2).

Keep the Python environment isolated in the project venv. Do not put secrets in the skill or client entry.

This fork's Windows setup uses Python 3.13. The system Python 3.7 is not supported. Run the checkout's `scripts/install-codex.ps1` to create the runtime, register Codex MCP and install the skill; use -WhatIf to preview. The helper scripts discover the checkout when run in-place and recognize Windows `.venv/Scripts/python.exe` from Git Bash. An installed standalone skill requires MCP_MUSESCORE_DIR when the checkout is outside the historical Downloads default.

## Start script

The skill scripts do not install dependencies or alter client configuration. They only launch or probe an already-installed checkout:

```bash
skills/mcp-musescore/scripts/start-mcp-musescore.sh
```

```powershell
& .\skills\mcp-musescore\scripts\start-mcp-musescore.ps1
```

Set `MCP_MUSESCORE_DIR` to override the default `~/Downloads/mcp-musescore` location. Set `MCP_MUSESCORE_PYTHON` to override the Python executable.

## Repository CLI

The upstream README documents `fastmcp dev inspector server.py` and `fastmcp inspect server.py` for development/inspection. Use those only when the user asks to inspect the MCP server itself. They do not start the MuseScore QML plugin and do not replace calls to the registered score tools.

## Verification script

`check-mcp-musescore.sh`/`.ps1` compiles the Python package, imports `server.py`, and sends a real `ping` WebSocket action to port 8765. It fails when MuseScore or the plugin is not reachable.
