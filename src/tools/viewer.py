"""Score viewer tool: renders the current score as sheet music inside MCP Apps hosts."""

import json
from pathlib import Path
from typing import Annotated, Optional

from fastmcp.apps import AppConfig, ResourceCSP
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult

from ..client import MuseScoreClient
from ..client.responses import unwrap_response

VIEWER_URI = "ui://musescore/score-viewer.html"
VIEWER_HTML = Path(__file__).resolve().parent.parent / "ui" / "score_viewer.html"
DEFAULT_MEASURE_TICKS = 1920


def _unwrap(response: dict) -> dict:
    """Return the plugin's result payload or raise ToolError."""
    result = unwrap_response(response)
    if not isinstance(result, dict) or "error" in result:
        message = result.get("error") if isinstance(result, dict) else "Unexpected plugin response"
        raise ToolError(message)
    return result


def setup_viewer_tools(mcp, client: MuseScoreClient, context_service=None):
    """Setup the score viewer (an MCP App: tool plus ui:// resource)."""

    @mcp.resource(
        VIEWER_URI,
        app=AppConfig(csp=ResourceCSP(resource_domains=["https://unpkg.com"])),
    )
    def score_viewer() -> str:
        """Sheet music viewer used by show_score."""
        return VIEWER_HTML.read_text(encoding="utf-8")

    @mcp.tool(
        app=AppConfig(resource_uri=VIEWER_URI),
        description=(
            "显示按音符数据绘制的简略示意图。查看MuseScore实际排版用get_score_image，"
            "先用read_arrangement_context读取指定段落。示意图适合浏览音高与时值。"
        ),
        tags={"score"},
        annotations={"readOnlyHint": True},
    )
    async def show_score(
        first_measure: Annotated[int, "First measure to show (1-based)"] = 1,
        last_measure: Annotated[
            Optional[int], "Last measure to show (1-based). Defaults to the end of the score."
        ] = None,
    ) -> ToolResult:
        analysis = _unwrap(await client.send_command("getScore")).get("analysis")
        if not isinstance(analysis, dict):
            raise ToolError("MuseScore returned no score data")

        measures = analysis.get("measures", [])
        measure_ticks = DEFAULT_MEASURE_TICKS
        if len(measures) > 1:
            measure_ticks = measures[1]["startTick"] - measures[0]["startTick"] or measure_ticks

        shown = [
            m for m in measures
            if m["measure"] >= first_measure and (last_measure is None or m["measure"] <= last_measure)
        ]
        payload = {**analysis, "measures": shown, "measureTicks": measure_ticks}

        title = analysis.get("title") or "Untitled"
        summary = (
            f'Score "{title}": showing {len(shown)} of {len(measures)} measure(s), '
            f'{len(analysis.get("staves", []))} staff/staves.'
        )
        return ToolResult(content=summary, structured_content=json.loads(json.dumps(payload)))

    @mcp.tool(description="读取已获取选段的MuseScore原生谱图，包含实际延音、连音组、字体和手动位置。返回PNG及音符在图中的位置，共用context_id对应的音符引用。较长范围分图，image_index从0开始。",
              tags={"score"}, annotations={"readOnlyHint": True})
    async def get_score_image(
        context_id: Annotated[str, "read_arrangement_context返回的contextId"],
        image_index: Annotated[int, "从0开始的图片序号；按返回的nextImage继续读取"] = 0,
    ) -> ToolResult:
        from mcp.types import ImageContent, TextContent
        from ..context.service import ContextError
        if context_service is None:
            raise ToolError("请先读取要查看的谱段。")
        try:
            context = context_service.context_result(context_id)
            result = await context_service.command("arrangementImage", {
                "snapshotId": context["snapshotId"], "scope": context["scope"], "imageIndex": image_index})
        except ContextError as error:
            raise ToolError(str(error)) from error
        if result.get("snapshotId") != context["snapshotId"] or not result.get("pngBase64"):
            raise ToolError("请更新MuseScore后重新读取这一段的谱图。")
        metadata = {key: value for key, value in result.items() if key != "pngBase64"}
        metadata["contextId"] = context_id
        measures = result["measures"]
        title = result.get("identity", {}).get("displayTitle", "当前乐谱")
        caption = f"{title} · 第{measures[0]['firstMeasure']}—{measures[-1]['lastMeasure']}小节 · 谱图{image_index + 1}/{result['imageCount']}"
        return ToolResult(content=[TextContent(text=caption),
            ImageContent(data=result["pngBase64"], mimeType="image/png")], structured_content=metadata)
