"""Time signature and tempo tools for MuseScore MCP."""

from typing import Annotated

from ..client import MuseScoreClient
from fastmcp.exceptions import ToolError


def setup_time_tempo_tools(mcp, client: MuseScoreClient):
    """Setup time signature and tempo tools."""
    
    @mcp.tool(
        description="Set the time signature.",
        tags={"time"},
    )
    async def set_time_signature(
        numerator: Annotated[int, "Top number of time signature (beats per measure)"] = 4,
        denominator: Annotated[int, "Bottom number of time signature (note value that gets the beat)"] = 4,
    ):
        return await client.send_command("setTimeSignature", {
            "numerator": numerator,
            "denominator": denominator
        })

    @mcp.tool(description="Insert a visible quarter-note tempo at the current cursor. Does not draw a tempo curve or replace existing markings.", tags={"time"})
    async def set_tempo(bpm: Annotated[float, "Positive quarter-note BPM"]):
        if not 5 <= bpm <= 999:
            raise ToolError("BPM must be between 5 and 999")
        return await client.send_command("setTempo", {"bpm": bpm})
