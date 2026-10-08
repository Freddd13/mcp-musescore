# Public MCP tool reference

This reference describes the tools currently registered by `server.py` and the JSON actions sent to the MuseScore QML plugin. Use the Python function names when calling MCP. Use the camelCase action names only inside `processSequence`.

The server registers 30 public tools. Python names use snake_case except the preserved processSequence.

## Connection and score inspection

| MCP tool | Parameters | What it does |
|---|---|---|
| `connect_to_musescore` | none | Opens the WebSocket client connection to `ws://localhost:8765`. Returns `{success: bool}`. |
| `ping_musescore` | none | Sends the `ping` action. A healthy plugin returns `pong`. |
| `get_score` | none | Requests the current score analysis, including title, measure data, staves, voices, durations, lyrics, and pitch information when available. |
| `get_score_data` | `first_measure=1`, `last_measure=None` | JSON with inclusive 1-based measure bounds, actual/written durations and per-note ties/tuning/velocity properties. Does not change selection. Filtering occurs in Python after a full QML read. |
| `get_capabilities` | none | Bridge/application version, ticks per quarter, score availability, optional ScoreObserver presence. |
| `show_score` | `first_measure: int = 1`, `last_measure: int \| None = None` | Read-only. Renders the score as sheet music in MCP Apps hosts (VexFlow viewer). Other hosts get only a text summary; use `get_score` for data. |

Call `ping_musescore` before a mutation. Call `get_score` before and after a complex edit.

## Navigation and selection

| MCP tool | Parameters | What it does |
|---|---|---|
| `get_cursor_info` | none | Reads the current cursor/selection state and the related score context. |
| `go_to_measure` | `measure: int` | Moves to a 1-based measure and selects it. |
| `go_to_final_measure` | none | Moves to the final measure. |
| `go_to_beginning_of_score` | none | Resets the plugin cursor/selection to the beginning of the score. |
| `next_element` | none | Moves the cursor to the next score element. |
| `prev_element` | none | Moves the cursor to the previous score element. |
| `next_staff` | none | Moves the cursor to the next staff. |
| `prev_staff` | none | Moves the cursor to the previous staff. |
| `select_current_measure` | none | Selects the current measure. |
| `select_custom_range` | `start_tick: int`, `end_tick: int`, `start_staff: int`, `end_staff: int` | Selects a precise tick range across one or more zero-based staves. MuseScore uses 480 ticks per quarter note in this project. |

Navigation wrappers may return a response envelope from the bridge. Read the returned state instead of assuming a move succeeded.

## Notes, rests, lyrics, and measures

Duration values are JSON objects such as `{"numerator": 1, "denominator": 4}` for a quarter note. MIDI pitch 60 is middle C (C4); valid MIDI pitch values are 0–127.

| MCP tool | Parameters | What it does |
|---|---|---|
| `add_note` | `pitch=64`, `duration={numerator:1,denominator:4}`, `advance_cursor_after_action=true`, `add_to_chord=false` | Adds a note or stacks it on the current chord. |
| `add_rest` | `duration: dict = {numerator: 1, denominator: 4}`, `advance_cursor_after_action: bool = true` | Adds a rest at the current cursor position. |
| `add_tuplet` | `duration: dict = {numerator: 1, denominator: 4}`, `ratio: dict = {numerator: 3, denominator: 2}`, `advance_cursor_after_action: bool = true` | Adds a tuplet; the default ratio represents a triplet. |
| `add_lyrics` | `lyrics: list[str]`, `verse: int = 0` | Adds syllables to consecutive notes from the current cursor. Verse is zero-based. |
| `insert_measure` | none | Inserts a measure at the current position. |
| `append_measure` | `count: int = 1` | Appends one or more measures to the end of the score. |
| `delete_selection` | `measure: int | null = null` | Deletes the current selection, or a specified measure when provided. Treat as destructive and verify immediately. |
| `undo` | none | Undoes the last MuseScore operation. |

## Staff, instruments, and time

| MCP tool | Parameters | What it does |
|---|---|---|
| `add_instrument` | `instrument_id: str` | Adds a staff/instrument using the MuseScore instrument identifier. |
| `set_staff_mute` | `staff: int`, `mute: bool` | Legacy visibility operation, unsupported by MuseScore 3. Does not mute audio; use Mixer. |
| `set_instrument_sound` | `staff: int`, `instrument_id: str` | Opens a dialog for manual instrument selection; does not apply a sound automatically. |
| `set_time_signature` | `numerator: int = 4`, `denominator: int = 4` | Sets the time signature at the current score context. |
| `set_tempo` | `bpm: float` | Inserts visible quarter-note tempo, 5–999 BPM, at the current cursor. Does not replace markings or create a curve. |

## Batch execution

| MCP tool | Parameters | What it does |
|---|---|---|
| `processSequence` | `sequence: list[object]` | Sends a list of camelCase actions to the plugin in order. Use only when the complete sequence is known and safe. |

The currently accepted inner actions are:

```text
getScore, addNote, addRest, addTuplet, appendMeasure, deleteSelection,
getCursorInfo, goToMeasure, nextElement, prevElement, nextStaff, prevStaff,
selectCurrentMeasure, undo, insertMeasure, goToFinalMeasure,
goToBeginningOfScore, setTimeSignature, addLyrics, addInstrument,
setStaffMute, setInstrumentSound, setTempo
```

Each action uses a `params` object. Examples:

```json
{
  "sequence": [
    {"action": "goToBeginningOfScore", "params": {}},
    {"action": "addNote", "params": {"pitch": 60, "duration": {"numerator": 1, "denominator": 4}, "advanceCursorAfterAction": true}},
    {"action": "addRest", "params": {"duration": {"numerator": 1, "denominator": 4}, "advanceCursorAfterAction": true}}
  ]
}
```

setTempo has a direct set_tempo wrapper and a typed batch action. syncStateToSelection is internal. Sequences are not atomic; already completed actions remain applied. Unknown typed actions are rejected before sending, and QML checks action failures. Recursive sequences are not supported by the public schema.

## Names not currently exposed

The upstream README mentions `add_lyrics_to_current_note` and `set_title`, but the current `src/tools/` registration does not expose those tools. Do not call them as if they existed. They require a future repository change before they can be used through MCP.
