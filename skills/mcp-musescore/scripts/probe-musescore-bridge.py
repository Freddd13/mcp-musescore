#!/usr/bin/env python3
"""Send one real ping through the MuseScore plugin WebSocket."""

import asyncio
import json
import os
import sys

import websockets


async def main() -> None:
    host = os.environ.get("MCP_MUSESCORE_HOST", "127.0.0.1")
    port = int(os.environ.get("MCP_MUSESCORE_PORT", "8765"))
    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri, open_timeout=5, close_timeout=2) as websocket:
        await websocket.send(json.dumps({"action": "ping", "params": {}}))
        response = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
    if response.get("status") != "success" or response.get("result") != "pong":
        raise RuntimeError(f"Unexpected MuseScore bridge response: {response!r}")
    print(f"MuseScore bridge OK: {uri}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f"MuseScore bridge check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
