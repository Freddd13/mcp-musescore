---
name: mcp-musescore
description: Use the Freddd13 MuseScore 3 Evolution MCP bridge with Codex to read, analyze, navigate, compose and edit an open score. Supports piano score analysis and verified notation edits; consult capability limits for playback and engraving.
metadata:
  short-description: Control an open MuseScore score
---

# MuseScore MCP

Use this skill when a user asks to inspect, compose, edit, navigate, or analyze a score in MuseScore through the configured `mcp-musescore` server.

## Read the right detail

- Read [references/tools.md](references/tools.md) before choosing a tool or constructing a batch sequence. It documents the public MCP tools and bridge limitations.
- Read [references/architecture.md](references/architecture.md) when diagnosing connection, plugin, port, response-envelope, or MuseScore-version problems.
- Read [references/client-configuration.md](references/client-configuration.md) when a client needs a stdio configuration.
- Read [references/runtime.md](references/runtime.md) when installing, selecting a Python runtime, or using the repository's CLI helpers.

## Routing rule

Prefer a purpose-built CLI command when it is actually available in the current environment for the requested operation. If no such CLI command is available, use the public MCP tools documented in `references/tools.md`. Never invent a MuseScore CLI command. The repository's `fastmcp dev` command is an MCP inspector/development helper; it is not a replacement for the live MuseScore editing tools.

## Preconditions and startup

- MuseScore 3 Evolution must be open with a score loaded.
- The `musescore-mcp-websocket.qml` plugin must be enabled and running from MuseScore's Plugins menu.
- The plugin listens on `ws://127.0.0.1:8765` using QtWebSockets. Windows installations need the matching Qt5WebSockets.dll in addition to the QML module.
- The MCP client must launch the repository's `server.py` over stdio. Use `scripts/start-mcp-musescore.sh` or `scripts/start-mcp-musescore.ps1` for a manual launch; set `MCP_MUSESCORE_DIR` when the repository is not in `~/Downloads/mcp-musescore`.
- Run `scripts/check-mcp-musescore.sh` or its PowerShell equivalent when a deterministic bridge probe is needed.

If a tool reports `Not connected to MuseScore`, do not retry mutations blindly: start or reload the MuseScore plugin, call `ping_musescore`, and only then continue.

## Operating sequence

1. Call `ping_musescore` to verify the bridge.
2. Call `get_capabilities`, then `get_score_data` for authoritative JSON before editing. Keep `get_score` for a compact LilyPond reading view. Measure numbers are 1-based; staves and voices are 0-based.
3. Use navigation and selection tools to place the cursor precisely.
4. Use a direct mutation for one or two deliberate edits; use `processSequence` for a known batch.
5. Read `get_score_data` after each mutation batch and report what was verified. The server serializes calls on a single socket. A lost write response is ambiguous and is never automatically replayed.
6. Saving or exporting `.mscz`, PDF, or audio remains a MuseScore UI action unless another configured tool provides it.

## Guardrails

- Do not claim that an edit succeeded without a follow-up read from MuseScore.
- Preserve the user's score, cursor, and selection unless the requested operation changes them.
- Resolve pitch, duration, staff, voice, measure, and cursor-advance intent from the user's request and score. Ask only for material missing details.
- Sequences are not atomic: completed actions remain applied, each with its own undo. Inspect `failedIndex` and `completedCount` before recovery.
- `set_staff_mute` is a legacy visibility operation, unsupported on MuseScore 3; it never provides audio mute. `set_instrument_sound` opens a manual dialog. No automatic SF2 selection, pedal curves, final MIDI velocity calculation or physical piano tuning is currently exposed.
- Use structured timing and per-note ties for analysis; the LilyPond and VexFlow views are approximate. Final engraving must be checked in MuseScore.
- Use `undo` when a just-made mutation is wrong and the score state is still safe to reverse.
- Treat the JSON returned by the bridge as authoritative. The upstream README contains historical names such as `add_lyrics_to_current_note` and `set_title` that are not currently registered public MCP tools; do not call them unless the repository exposes them in a future version.
- `processSequence` is camelCase because that is the registered Python tool name. Its inner `action` values are also camelCase QML actions; see the reference for the supported set.

## Portability

This is a Codex skill with `agents/openai.yaml` metadata. Install the folder into a Codex skill discovery location; configuring the MCP server is a separate step. Read client-configuration.md for the installer and runtime.md for launch/probe helpers.

## Piano workflows

For harmony, voicing, hand span, voice leading and rhythm checks, read a bounded measure range and provide proposals with measure/staff/voice/tick coordinates. Hand assignment and fingering are musical judgments, not guaranteed facts from staff numbers. Avoid counting tied continuations as fresh attacks. Velocity offsets/types are stored properties, not final rendered MIDI velocity. New Evolution observer/preview and performance write tools are future extensions; do not invent their names.
