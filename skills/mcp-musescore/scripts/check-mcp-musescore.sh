#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
checkout_dir="$(CDPATH= cd -- "$script_dir/../../.." && pwd)"
default_dir="$HOME/Downloads/mcp-musescore"
if [ -f "$checkout_dir/server.py" ]; then default_dir="$checkout_dir"; fi
repo_dir="${MCP_MUSESCORE_DIR:-$default_dir}"
python_bin="${MCP_MUSESCORE_PYTHON:-$repo_dir/.venv/bin/python}"
if [ -z "${MCP_MUSESCORE_PYTHON:-}" ] && [ -f "$repo_dir/.venv/Scripts/python.exe" ]; then
  python_bin="$repo_dir/.venv/Scripts/python.exe"
fi

[ -f "$repo_dir/server.py" ] || { printf 'server.py not found in %s\n' "$repo_dir" >&2; exit 1; }
[ -x "$python_bin" ] || { printf 'Python executable not found: %s\n' "$python_bin" >&2; exit 1; }

cd "$repo_dir"
"$python_bin" -m compileall -q server.py src
"$python_bin" -c 'import server; print("MCP server import OK")'
"$python_bin" "$script_dir/probe-musescore-bridge.py"
