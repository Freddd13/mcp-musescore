"""Staff and instrument tools for MuseScore MCP."""

from typing import Annotated

from ..client import MuseScoreClient


def setup_staff_instruments_tools(mcp, client: MuseScoreClient):
    """Setup staff and instrument tools."""
    
    @mcp.tool(
        description="Add a new staff/instrument to the score.",
        tags={"staff"},
    )
    async def add_instrument(
        instrument_id: Annotated[str, "ID of the instrument to add"],
    ):
        return await client.send_command("addInstrument", {
            "instrumentId": instrument_id
        })

    @mcp.tool(
        description="Legacy visibility operation, not audio mute. MuseScore 3 lacks this staff property and reports unsupported; use Mixer for audio mute.",
        tags={"staff"},
    )
    async def set_staff_mute(
        staff: Annotated[int, "Staff number (0-based)"],
        mute: Annotated[bool, "True to hide the staff, False to show it (legacy parameter name)"],
    ):
        return await client.send_command("setStaffMute", {
            "staff": staff,
            "mute": mute
        })

    @mcp.tool(
        description="Open MuseScore's instrument dialog for manual selection. Does not automatically apply the requested sound.",
        tags={"staff"},
    )
    async def set_instrument_sound(
        staff: Annotated[int, "Staff number (0-based)"],
        instrument_id: Annotated[str, "ID of the new instrument sound"],
    ):
        return await client.send_command("setInstrumentSound", {
            "staff": staff,
            "instrumentId": instrument_id
        })
