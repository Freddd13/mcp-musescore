"""Locate the maintained engraving library; read-only, Python standard library."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

COMMON = ("README.md", "PREFERENCES.md", "JUDGMENT_GUIDE.md")
TOPICS = {
    "overview": ("FOUNDATION_REVIEW.md",),
    "spacing": ("SPACING_DECISIONS.md", "USER_SPACING_APPLICATION.md", "SPACING_CANDIDATES.md", "SPACING_STUDY.md"),
    "rhythm": ("RHYTHM_READING.md", "NOTATION_DETAILS.md"),
    "beams": ("BEAM_STEM_STUDY.md", "RHYTHM_READING.md"),
    "curves": ("CURVES_STUDY.md",),
    "piano": ("PIANO_TEXTURE_STUDY.md",),
    "cross-staff": ("CROSS_STAFF_STUDY.md", "PIANO_TEXTURE_STUDY.md"),
    "notation": ("NOTATION_DETAILS.md",),
    "layout": ("SPACING_DECISIONS.md", "EXTERNAL_PRACTICE.md", "CASES.md"),
    "sources": ("SOURCES.md", "BEHIND_BARS_NOTES.md", "RESOURCE_PLAN_MAPPING.md"),
    "cases": ("corpus/INDEX.md", "CASES.md", "CASES_EXPANDED.md"),
    "baseline": ("INPUT_HISTORY.md",),
    "implementation": ("IMPLEMENTATION.md",),
}


def validate_repo(value: str | Path) -> Path:
    root = Path(value).expanduser().resolve()
    library = root / "docs" / "engraving"
    missing = [name for name in COMMON if not (library / name).is_file()]
    if missing:
        raise ValueError(f"No engraving library at {library}; missing {', '.join(missing)}. Pass --repo with the mcp-musescore checkout.")
    return root


def locate_repo(explicit: str | None) -> tuple[Path, str]:
    if explicit is not None:
        return validate_repo(explicit), "--repo"
    configured = os.environ.get("MCP_MUSESCORE_DIR")
    if configured:
        return validate_repo(configured), "MCP_MUSESCORE_DIR"
    parents = Path(__file__).resolve().parents
    candidates = []
    if len(parents) > 3:
        candidates.append((parents[3], "skill-realpath"))
    current = Path.cwd().resolve()
    candidates.extend((p, "working-directory-ancestor") for p in (current, *current.parents))
    for candidate, origin in candidates:
        try:
            return validate_repo(candidate), origin
        except ValueError:
            pass
    raise ValueError("Engraving library not found. Pass --repo or set MCP_MUSESCORE_DIR to the maintained mcp-musescore checkout; copying this skill alone does not copy the library.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Maintained mcp-musescore checkout; explicit value takes precedence.")
    parser.add_argument("--topic", choices=TOPICS, default="overview")
    parser.add_argument("--list-topics", action="store_true")
    args = parser.parse_args(argv)
    if args.list_topics:
        print(json.dumps({"topics": TOPICS}, ensure_ascii=False, indent=2))
        return 0
    try:
        root, origin = locate_repo(args.repo)
        library = root / "docs" / "engraving"
        selected = [library / name for name in TOPICS[args.topic]]
        for path in selected:
            if not path.is_file():
                raise ValueError(f"Missing reference {path}; update or check this checkout before claiming it was read.")
        print(json.dumps({
            "repository": str(root), "repository_resolution": origin,
            "knowledge_base": str(library), "topic": args.topic,
            "start_here": [str(library / name) for name in COMMON],
            "references": [str(path) for path in selected],
        }, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
