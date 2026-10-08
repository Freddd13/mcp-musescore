# Architecture and connection model

```text
Codex / another MCP client
                 │ MCP stdio
                 ▼
server.py ─ FastMCP("MuseScore Assistant")
                 │ src/tools/*
                 ▼
MuseScoreClient ─ WebSocket ws://127.0.0.1:8765
                 │ JSON actions
                 ▼
musescore-mcp-websocket.qml ─ MuseScore plugin API
                 ▼
open score in MuseScore 3 Evolution
```

## Components

- `server.py` creates the FastMCP server and registers the public Python tools.
- `src/tools/` translates typed MCP calls into camelCase JSON actions.
- `src/client/websocket_client.py` serializes requests, bounds receive waits and retries only reads. Lost write responses report outcomeUnknown; inspect before replay.
- `musescore-mcp-websocket.qml` uses QtWebSockets on loopback port 8765. It requires no api.websocketserver. Windows needs the matching Qt5WebSockets.dll and QML module.
- `src/utils/lilypond_converter.py` converts score analysis/selection data into LilyPond text for supported read paths.

## Startup order

1. Start MuseScore 3 Evolution and open a score.
2. Enable the plugin once in MuseScore's plugin manager.
3. Run `Plugins > MuseScore API Server`.
4. Let the MCP client launch `server.py` over stdio, or run the skill's start script manually.
5. Call `ping_musescore` before using a score tool.

The Python backend is not the WebSocket server. The QML plugin is the process that listens on port 8765. Starting only `server.py` cannot make MuseScore reachable.

## Wire format

The Python client sends:

```json
{"action": "ping", "params": {}}
```

The QML plugin replies with a success envelope:

```json
{"status": "success", "result": "pong"}
```

Errors use:

```json
{"status": "error", "message": "..."}
```

Read wrappers unwrap status/result and surface nested errors. get_score keeps the LilyPond view; get_score_data provides JSON. Legacy mutation tools retain the wire envelope; inspect its inner result. Sequences stop on failures and report failedIndex/completedCount without rolling back completed actions.

## Files and versions

- Plugin source: `musescore-mcp-websocket.qml`.
- Python entry point: `server.py`.
- Dependency declaration: `requirements.txt`.
- The current source imports `fastmcp` (standalone FastMCP 4, declared as `fastmcp>=4,<5` in `requirements.txt`).
- This fork targets MuseScore 3 Evolution. Native checks use personal 0.10/0.11 Windows installations; upstream MuseScore 4 support claims are not guarantees for this fork.

## Failure diagnosis

- `Not connected to MuseScore`: the plugin is not running, the port is unavailable, or MuseScore closed/reloaded the plugin.
- `Unknown command`: the requested action is not in the QML dispatcher or is using the wrong camelCase spelling.
- Empty or stale score data: refresh the plugin/cursor state and call `get_score` again.
- Python import failure: inspect the venv and the installed MCP version; the unpinned upstream requirement may have selected an incompatible major version.
