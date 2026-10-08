"""Read the QML envelope while accepting legacy unwrapped responses."""

from fastmcp.exceptions import ToolError


def unwrap_response(response):
    if response.get("status") == "error" or "error" in response:
        raise ToolError(response.get("message") or response.get("error") or "MuseScore error")
    result = response.get("result") if "status" in response else response
    if isinstance(result, dict) and ("error" in result or result.get("success") is False):
        raise ToolError(str(result.get("error") or result.get("message") or "MuseScore action failed"))
    return result
