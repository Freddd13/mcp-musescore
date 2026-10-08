"""Connection and utility tools for MuseScore MCP."""

from ..client import MuseScoreClient
from ..client.responses import unwrap_response
from fastmcp.exceptions import ToolError
from typing import Annotated, Optional


def setup_connection_tools(mcp, client: MuseScoreClient):
    """Setup connection and utility tools."""
    
    @mcp.tool(
        description="Connect to the MuseScore WebSocket API.",
        tags={"connection"},
    )
    async def connect_to_musescore():
        result = await client.connect()
        return {"success": result}

    @mcp.tool(
        description="Ping the MuseScore WebSocket API to check connection.",
        tags={"connection"},
    )
    async def ping_musescore():
        return await client.send_command("ping")

    @mcp.tool(
        description="Get information about the current score.",
        tags={"connection", "score"},
        annotations={"readOnlyHint": True},
    )
    async def get_score():
        res = unwrap_response(await client.send_command("getScore"))
        if res.get("success") and "analysis" in res:
            from ..utils.lilypond_converter import json_to_lilypond
            analysis = res["analysis"]
            lily_str = json_to_lilypond(analysis)
            
            meta = []
            if "numMeasures" in analysis:
                meta.append(f"Total Mesures: {analysis['numMeasures']}")
                
            num_staves = len(analysis.get("staves", []))
            if num_staves > 0:
                meta.append(f"Nombre de portées: {num_staves}")
                
            meta_str = ", ".join(meta) if meta else "Aucune métadonnée"
            
            return f"[Métadonnées] {meta_str}\n[Partition]\n{lily_str}"
        return res

    @mcp.tool(description="Read bridge version, MuseScore version, score availability and optional Evolution API support.",
              tags={"connection"}, annotations={"readOnlyHint": True})
    async def get_capabilities():
        return unwrap_response(await client.send_command("getCapabilities"))

    @mcp.tool(description="Read authoritative structured notes, voices, timing, ties, tuning and velocity properties. Measure bounds are inclusive; reading leaves selection unchanged.",
              tags={"score"}, annotations={"readOnlyHint": True})
    async def get_score_data(
        first_measure: Annotated[int, "First measure (1-based, inclusive)"] = 1,
        last_measure: Annotated[Optional[int], "Last measure (1-based, inclusive); omitted means end of score"] = None,
    ):
        if first_measure < 1 or (last_measure is not None and last_measure < first_measure):
            raise ToolError("Invalid measure range")
        result = unwrap_response(await client.send_command("getScore"))
        if not isinstance(result, dict) or not isinstance(result.get("analysis"), dict):
            raise ToolError("MuseScore returned no score data")
        analysis = result["analysis"]
        return {**analysis, "measures": [m for m in analysis.get("measures", [])
                if m["measure"] >= first_measure and (last_measure is None or m["measure"] <= last_measure)]}
