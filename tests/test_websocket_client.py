"""Transport invariants: concurrent responses, ambiguous writes and recovery."""

import asyncio
import json

from websockets.asyncio.server import serve
from src.client import MuseScoreClient


def test_parallel_calls_receive_their_own_response():
    async def scenario():
        async def handler(ws):
            async for message in ws:
                command = json.loads(message)
                await asyncio.sleep(0.01)
                await ws.send(json.dumps({"result": command["params"]["id"]}))
        async with serve(handler, "127.0.0.1", 0) as bridge:
            client = MuseScoreClient(port=bridge.sockets[0].getsockname()[1])
            results = await asyncio.gather(*(client.send_command("getScore", {"id": i}) for i in range(8)))
            assert [r["result"] for r in results] == list(range(8))
            await client.close()
    asyncio.run(scenario())


def test_lost_write_response_is_not_replayed_and_next_read_recovers():
    async def scenario():
        writes = []
        async def handler(ws):
            async for message in ws:
                command = json.loads(message)
                if command["action"] == "addNote":
                    writes.append(command)
                    await ws.close()
                else:
                    await ws.send(json.dumps({"status": "success", "result": "pong"}))
        async with serve(handler, "127.0.0.1", 0) as bridge:
            client = MuseScoreClient(port=bridge.sockets[0].getsockname()[1])
            result = await client.send_command("addNote", {"pitch": 60})
            assert result["outcomeUnknown"] is True
            assert len(writes) == 1
            assert (await client.send_command("ping"))["result"] == "pong"
            await client.close()
    asyncio.run(scenario())


def test_write_response_timeout_is_bounded():
    async def scenario():
        async def handler(ws):
            async for _ in ws:
                await ws.wait_closed()
        async with serve(handler, "127.0.0.1", 0) as bridge:
            client = MuseScoreClient(port=bridge.sockets[0].getsockname()[1], timeout=0.05)
            result = await asyncio.wait_for(client.send_command("addNote"), 2)
            assert result["outcomeUnknown"] is True
            await client.close()
    asyncio.run(scenario())
