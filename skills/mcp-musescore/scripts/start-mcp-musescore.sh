#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
checkout_dir="$(CDPATH= cd -- "$script_dir/../../.." && pwd)"
default_dir="$HOME/Downloads/mcp-musescore"
if [ -f "$checkout_dir/server.py" ]; then default_dir="$checkout_dir"; fi
repo_dir="${MCP_MUSESCORE_DIR:-$default_dir}"
server="$repo_dir/server.py"
python_bin="${MCP_MUSESCORE_PYTHON:-$repo_dir/.venv/bin/python}"
if [ -z "${MCP_MUSESCORE_PYTHON:-}" ] && [ -f "$repo_dir/.venv/Scripts/python.exe" ]; then
  python_bin="$repo_dir/.venv/Scripts/python.exe"
fi

if [ ! -f "$server" ]; then
  printf 'mcp-musescore repository not found: %s\n' "$repo_dir" >&2
  printf 'Set MCP_MUSESCORE_DIR to the checkout containing server.py.\n' >&2
  exit 1
fi

if [ ! -x "$python_bin" ]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="$(command -v python3)"
  else
    printf 'No usable Python executable found: %s\n' "$python_bin" >&2
    exit 1
  fi
fi

cd "$repo_dir"
exec "$python_bin" "$server" "$@"
