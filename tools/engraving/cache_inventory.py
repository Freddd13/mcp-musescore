"""Read-only inventory of this project's engraving cache; never follows links.

Print JSON to stdout. Logical and Windows on-disk bytes are separate; no files
are removed, compressed, moved, or hashed. Original score folders are not read.
"""
from __future__ import annotations

import ctypes
import json
import os
from pathlib import Path
import shutil
import sys


def inventory(root: Path) -> dict:
    root = root.resolve()
    rows: dict[str, dict] = {}
    skipped: list[str] = []
    errors: list[dict] = []
    physical = None
    if os.name == "nt":
        from ctypes import wintypes
        physical = ctypes.WinDLL("kernel32", use_last_error=True).GetCompressedFileSizeW
        physical.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
        physical.restype = wintypes.DWORD
    pending = [root]
    while pending:
        folder = pending.pop()
        try:
            entries = list(os.scandir(folder))
        except OSError as exc:
            errors.append({"path": str(folder), "error": str(exc)})
            continue
        for entry in entries:
            path = Path(entry.path)
            try:
                stat = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or getattr(stat, "st_file_attributes", 0) & 0x400:
                    skipped.append(str(path.relative_to(root)))
                    continue
                if entry.is_dir(follow_symlinks=False):
                    pending.append(path)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                relative = path.relative_to(root)
                key = relative.parts[0] if len(relative.parts) > 1 else "(root files)"
                row = rows.setdefault(key, {"directory": key, "files": 0, "logical_bytes": 0,
                                            "on_disk_bytes": 0, "on_disk_unknown_files": 0})
                row["files"] += 1
                row["logical_bytes"] += stat.st_size
                if physical is not None:
                    from ctypes import wintypes
                    high = wintypes.DWORD()
                    ctypes.set_last_error(0)
                    low = physical(str(path), ctypes.byref(high))
                    if low == 0xFFFFFFFF and ctypes.get_last_error():
                        row["on_disk_unknown_files"] += 1
                    else:
                        row["on_disk_bytes"] += (high.value << 32) | low
                else:
                    row["on_disk_unknown_files"] += 1
            except OSError as exc:
                errors.append({"path": str(path), "error": str(exc)})
    ordered = sorted(rows.values(), key=lambda row: row["logical_bytes"], reverse=True)
    usage = shutil.disk_usage(root)
    return {"schema_version": 1, "cache_root": str(root),
            "note": "Windows GetCompressedFileSizeW bytes are per path, not deduplicated by hardlink identity or a volume-free-space delta; concurrent tasks may change the cache.",
            "total": {key: sum(row[key] for row in ordered)
                      for key in ("files", "logical_bytes", "on_disk_bytes", "on_disk_unknown_files")},
            "volume_free_bytes": usage.free, "directories": ordered,
            "skipped_links_or_reparse_points": skipped, "errors": errors}


if __name__ == "__main__":
    cache = Path(__file__).resolve().parents[2] / "tmp" / "engraving"
    result = inventory(cache)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if result["errors"] else 0)
