"""Current document identity across lightweight, paged and legacy reads."""
import asyncio
import copy

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from src.context.service import ContextService
from src.tools.connection import setup_connection_tools, score_data_projection


class Document:
    def __init__(self):
        self.calls = []
        self.states = 0
        self.identity = {"schemaVersion": "score-identity/1", "hasScore": True,
            "displayTitle": "谱面标题", "workTitle": "作品信息", "filePath": "E:/曲谱/第三稿.mscz",
            "partName": "钢琴", "scoreSessionId": "part-1", "masterSessionId": "master-1"}

    async def send_command(self, action, params=None):
        self.calls.append((action, copy.deepcopy(params)))
        if action == "getScoreIdentity":
            return {"status": "success", "result": copy.deepcopy(self.identity)}
        if action == "getScore":
            return {"status": "success", "result": {"success": True, "analysis": {
                "identity": copy.deepcopy(self.identity), "title": "谱面标题", "staves": [], "measures": []}}}
        if action == "arrangementState":
            self.states += 1
            current = copy.deepcopy(self.identity)
            if self.states > 1:
                current.update(displayTitle="修改后的标题", filePath="E:/曲谱/另存.mscz")
            return {"status": "success", "result": {"snapshotId": "part-1:1", "scoreSessionId": "part-1",
                "title": current["displayTitle"], "identity": current, "documentId": current["filePath"],
                "ticksPerQuarter": 480, "scope": {"start": 0, "end": 480, "firstTrack": 0, "endTrack": 4, "lastMeasure": 1}, "coverage": {}}}
        if action == "arrangementRange":
            return {"status": "success", "result": {"snapshotId": "part-1:1", "done": True}}
        raise AssertionError(action)


def test_identity_is_one_read_and_returns_distinct_titles():
    async def check():
        doc = Document(); mcp = FastMCP("identity-check")
        setup_connection_tools(mcp, doc)
        async with Client(mcp) as client:
            tools = await client.list_tools()
            assert next(t for t in tools if t.name == "get_score_identity").annotations.read_only_hint
            result = await client.call_tool("get_score_identity")
            assert result.data == doc.identity
        assert doc.calls == [("getScoreIdentity", None)]
    asyncio.run(check())


def test_no_open_score_keeps_application_identity():
    async def check():
        doc = Document(); doc.identity = {"hasScore": False, "application": {"instanceId": "app-1"}}
        mcp = FastMCP("empty-check"); setup_connection_tools(mcp, doc)
        async with Client(mcp) as client:
            assert (await client.call_tool("get_score_identity")).data == doc.identity
    asyncio.run(check())


def test_older_bridge_reports_update_instead_of_inventing_title():
    async def check():
        doc = Document(); doc.identity = {"error": "unknown command"}
        mcp = FastMCP("old-check"); setup_connection_tools(mcp, doc)
        async with Client(mcp) as client:
            with pytest.raises(ToolError, match="更新"):
                await client.call_tool("get_score_identity")
    asyncio.run(check())


def test_paged_read_finishes_with_latest_title_and_save_as_path():
    async def check():
        doc = Document(); context = await ContextService(doc).capture({"whole": True})
        assert context["title"] == "修改后的标题"
        assert context["identity"]["displayTitle"] == context["title"]
        assert context["documentId"] == "E:/曲谱/另存.mscz"
        assert context["snapshotId"] == "part-1:1"
        projected = score_data_projection(context)
        for key in ("title", "identity", "scoreSessionId", "documentId"):
            assert projected[key] == context[key]
    asyncio.run(check())


def test_lilypond_tool_names_current_part_and_file():
    async def check():
        doc = Document(); mcp = FastMCP("text-check"); setup_connection_tools(mcp, doc)
        async with Client(mcp) as client:
            result = await client.call_tool("get_score")
            text = result.content[0].text
            assert "谱面标题" in text and "钢琴" in text and "第三稿.mscz" in text
            assert "LilyPond" in text
        assert len(doc.calls) == 1
    asyncio.run(check())
