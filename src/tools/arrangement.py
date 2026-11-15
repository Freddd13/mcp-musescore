"""Codex-facing tools for the common score-context service."""
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from mcp.types import ImageContent, TextContent
from typing import Annotated
from uuid import uuid4
from ..context.service import ContextError, ContextService


def setup_arrangement_tools(mcp, service: ContextService):
    async def call(operation):
        try:
            return await operation
        except ContextError as error:
            raise ToolError(str(error)) from error

    @mcp.tool(description="Read the current in-memory score selection in bounded host pages. Includes exact quarter-unit timing, voices, spelling, ties, hands, velocity, repeat occurrences, available harmonic interpretation and supplied materials. request: scope {start,end,firstTrack,endTrack}, whole, firstMeasure/lastMeasure, purpose analysis/performance/engraving; fields ['geometry','performance'], taskBrief. Read first before submitting options.",
              tags={"arrangement", "score"}, annotations={"readOnlyHint": True})
    async def read_arrangement_context(request: Annotated[dict | None, "范围、可选字段和本次编配要求"] = None):
        return await call(service.capture(request))

    @mcp.tool(description="Start a cancellable score-context read. Poll arrangement_task until ready, then get_arrangement_context with its contextId.",
              tags={"arrangement", "score"}, annotations={"readOnlyHint": True})
    async def start_arrangement_read(request: Annotated[dict | None, "范围、可选字段和本次编配要求"] = None):
        try:
            return service.start_capture(request)
        except ContextError as error:
            raise ToolError(str(error)) from error

    @mcp.tool(description="Read progress or cancel an active context task.", tags={"arrangement"})
    async def arrangement_task(task_id: Annotated[str, "读取任务的taskId"], cancel: Annotated[bool, "结束这个读取任务"] = False):
        try:
            return service.task_state(task_id, cancel)
        except ContextError as error:
            raise ToolError(str(error)) from error

    @mcp.tool(description="Retrieve a completed immutable task context by contextId.", tags={"arrangement"}, annotations={"readOnlyHint": True})
    async def get_arrangement_context(context_id: Annotated[str, "读取结果中的contextId"]):
        try:
            return service.context_result(context_id)
        except ContextError as error:
            raise ToolError(str(error)) from error

    @mcp.tool(description="Refresh a retained task after score edits. Keeps its original score, range, purpose and requirements while reading current notes, material sources and requested performance. Ordinary browsing selection stays unchanged.",
              tags={"arrangement"}, annotations={"readOnlyHint": True})
    async def refresh_arrangement_context(context_id: Annotated[str, "要继续的contextId"], task_brief: Annotated[dict | None, "补充本次编配要求"] = None):
        return await call(service.refresh(context_id, task_brief))

    @mcp.tool(description="Read one native page directly. Use arrangementState via get_arrangement_state, then pass its snapshotId and scope, fromTick and limit (1-64). Useful for large scores.",
              tags={"arrangement"}, annotations={"readOnlyHint": True})
    async def get_arrangement_page(request: Annotated[dict, "原生页的snapshotId、scope和fromTick"]):
        return await call(service.command("arrangementRange", request))

    @mcp.tool(description="Read score version, exact scope, available fields and saved musical information without changing selection.",
              tags={"arrangement"}, annotations={"readOnlyHint": True})
    async def get_arrangement_state(request: Annotated[dict | None, "范围、可选字段和本次编配要求"] = None):
        return await call(service.command("arrangementState", request))

    @mcp.tool(description="Read the actual MuseScore page layout for a retained context: visible staffs, systems and measure ranges, shared rhythmic columns, element positions and placement settings. Use get_score_image with the same context_id to inspect local and whole-system notation.",
              tags={"arrangement", "engraving"}, annotations={"readOnlyHint": True})
    async def read_engraving_layout(context_id: Annotated[str, "待检查排版的选段 contextId"]):
        try:
            context = service.context_result(context_id)
        except ContextError as error:
            raise ToolError(str(error)) from error
        return await call(service.command("readEngravingLayout", {
            "snapshotId": context["snapshotId"], "scope": context["scope"],
        }))

    @mcp.tool(description="Save user-supplied assertions, materials and alignments in the score. Preserve existing entries when extending. Each assertion/material records origin, target coverage and status. One native undo. Explicit user intent to save information is required.",
              tags={"arrangement"})
    async def save_arrangement_information(snapshot_id: Annotated[str, "已读取的snapshotId"], information: Annotated[dict, "保留来源和作用范围的资料集合"]):
        return await call(service.store_information(snapshot_id, information))

    @mcp.tool(description="Submit 1-3 local score options for in-score comparison. Each: title, summary, scope, changes [{ref:{snapshotId,id},pitch,tpc1,tpc2,velocity,finger,hand,handEnd}], voices [{track,events:[{quarterDuration:{numerator,denominator},pitches:[{pitch,tpc1,tpc2}]}]}]. Voices cover the complete scope including rests (empty pitches). For an engraving-only option use engravingChanges instead: each entry has kind and tick. symbolOffset adds track, type, x, y, optionally connectionStart, connectionEnd and systemStart copied from read_engraving_layout; timeColumnSpacing adds space; measureStretch adds stretch; staffSpacing adds staff and space; lineBreak adds boolean enabled. Offsets and spaces are in staff spaces. Use compare_engraving_option to check native before and after. Host prepares copies and shows them in View > 编配建议.",
              tags={"arrangement"})
    async def submit_arrangement_options(context_id: Annotated[str, "读取结果中的contextId"], options: Annotated[list[dict], "一至三种完整的局部写法"], task_brief: Annotated[dict | None, "本次允许修改的范围和保留条件"] = None):
        return await call(service.submit_options(context_id, options, task_brief))

    @mcp.tool(description="Generate a native velocity proposal for the editable notes in this retained scope. Choose melody (raise melody), background (reduce background), or phrase (rise towards peak_tick and settle). Mark roles by track and, for crossing voices, by exact note id. Respect explicitly locked notes. Compare actual rendered attack values in MuseScore before adopting.",
              tags={"arrangement", "performance"})
    async def propose_velocity_adjustment(
        context_id: Annotated[str, "选段读取返回的 contextId"],
        kind: Annotated[str, "melody、background 或 phrase"],
        amount: Annotated[int, "变化幅度，1–24 MIDI 力度单位"] = 3,
        roles: Annotated[dict[str, str] | None, "用 track 编号标记声部角色：melody、background、bass"] = None,
        note_roles: Annotated[dict[str, str] | None, "用选段读出的 ref.id 指定单音角色，优先于声部"] = None,
        locked_notes: Annotated[list[str] | None, "保持力度的 ref.id"] = None,
        peak_tick: Annotated[int | None, "句峰在选段中的原生 tick"] = None,
        preserve_manual: Annotated[bool, "保留已有手调力度和自定义发音"] = True,
    ):
        try:
            context = service.context_result(context_id)
        except ContextError as error:
            raise ToolError(str(error)) from error
        request = {
            "snapshotId": context["snapshotId"], "scope": context["scope"],
            "kind": kind, "amount": amount, "roles": roles or {},
            "noteRoles": note_roles or {}, "lockedNotes": locked_notes or [],
            "preserveManual": preserve_manual,
            "operationId": str(uuid4()),
        }
        if peak_tick is not None:
            request["peakTick"] = peak_tick
        return await call(service.write("proposeVelocityAdjustment", request))

    @mcp.tool(description="Operate a submitted option: preview (score difference overlay), performance (original and proposed rendered MIDI attacks), original/audition (same-range playback), apply (one undo), variant (save as regional writing), stop. Apply within the user's requested scope; stale options require a fresh read. operation_id may be reused to query/recover one logical operation.",
              tags={"arrangement"})
    async def arrangement_option(
        option_id: Annotated[str, "原生面板返回的写法id"],
        action: Annotated[str, "preview、performance、original、audition、apply、variant或stop"],
        operation_id: Annotated[str | None, "这一次操作的唯一id"] = None,
        note_ids: Annotated[list[str] | None, "纯力度建议中要采用的 ref.id"] = None,
        occurrence: Annotated[int | None, "从谱段的第几遍试听"] = None,
    ):
        extra = {}
        if note_ids is not None:
            if action != "apply" or not note_ids:
                raise ToolError("请为“采用”提供要使用的音符编号。")
            extra["noteIds"] = note_ids
        if occurrence is not None:
            if action not in {"original", "audition"} or occurrence < 1:
                raise ToolError("试听的遍次从 1 开始。")
            extra["occurrence"] = occurrence
        if extra:
            return await call(service.write("arrangementOption", {
                "optionId": option_id, "action": action,
                "operationId": operation_id or str(uuid4()), **extra,
            }))
        return await call(service.option_action(option_id, action, operation_id))

    @mcp.tool(description="Compare a prepared engraving option with two native page-layout images. Both share the same measure anchor; whole_system can show an entire line.",
              tags={"arrangement", "engraving"}, annotations={"readOnlyHint": True})
    async def compare_engraving_option(
        option_id: Annotated[str, "净书建议的 optionId"],
        at_tick: Annotated[int | None, "原生 tick；省略时查看第一个改动处"] = None,
        whole_system: Annotated[bool, "查看整行"] = True,
    ) -> ToolResult:
        request = {"optionId": option_id, "action": "compare", "wholeSystem": whole_system}
        if at_tick is not None:
            request["atTick"] = at_tick
        result = await call(service.command("arrangementOption", request))
        differences = result.get("engravingDifferences", [])
        content = []
        metadata = {"engravingDifferences": differences}
        for key, label in (("before", "原排版"), ("after", "建议排版")):
            image = result.get(key, {})
            if not image.get("pngBase64"):
                raise ToolError(f"{label}暂未生成，请在编配建议中重试。")
            content.append(TextContent(type="text", text=label))
            content.append(ImageContent(type="image", data=image["pngBase64"], mimeType="image/png"))
            metadata[key] = {name: value for name, value in image.items() if name != "pngBase64"}
        return ToolResult(content=content, structured_content=metadata)

    @mcp.tool(description="Save a prepared engraving option as a separate MSCZ file after the user confirms the output path. The original remains open.",
              tags={"arrangement", "engraving"})
    async def save_engraving_copy(
        option_id: Annotated[str, "净书建议的 optionId"],
        destination: Annotated[str, "用户选择的 MSCZ 副本绝对路径"],
        overwrite: Annotated[bool, "用户已同意覆盖现有副本"] = False,
    ):
        return await call(service.write("arrangementOption", {
            "optionId": option_id, "action": "copy", "destination": destination,
            "overwrite": overwrite, "operationId": str(uuid4()),
        }))

    @mcp.tool(description="Query a native operation result by operationId after a lost connection. A known operation is returned without executing it again.",
              tags={"arrangement"}, annotations={"readOnlyHint": True})
    async def arrangement_operation_result(operation_id: Annotated[str, "要查询的operationId"]):
        return await call(service.operation_status(operation_id))
