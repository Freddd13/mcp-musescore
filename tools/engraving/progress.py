"""Check evidence references and print engraving X/Y coverage (standard library).

This checks recorded scope and arithmetic, not the truth of reading claims or
musical understanding. It does not read private PDFs or mutate any files.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "docs" / "engraving"


def load(relative: str) -> dict:
    return json.loads((LIBRARY / relative).read_text(encoding="utf-8"))


def reference(relative: str) -> None:
    path = (LIBRARY / relative).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f"Missing or external project evidence: {relative}")


def check_items(items: list[dict], planned: int, key: str = "id") -> int:
    ids = [item[key] for item in items]
    if len(ids) != planned or len(set(ids)) != planned:
        raise ValueError(f"Expected {planned} unique {key} entries, got {len(ids)}")
    return sum(item.get("status") == "complete" for item in items)


def summary() -> dict:
    data = load("progress.json")
    inventory = load(data["corpus"]["inventory"])
    reviews = load(data["corpus"]["first_pass"])
    scores = {item["id"]: item for item in inventory["scores"]}
    planned_scores = data["corpus"]["planned_scores"]
    planned_pages = data["corpus"]["planned_pages"]
    if len(scores) != planned_scores or sum(s["pages"] for s in scores.values()) != planned_pages:
        raise ValueError("Inventory changed; revise scope explicitly before changing denominators")
    if len(reviews["scores"]) != planned_scores or {s["id"] for s in reviews["scores"]} != set(scores):
        raise ValueError("First-pass score coverage does not match the inventory")
    screened = close = 0
    for item in reviews["scores"]:
        source = scores[item["id"]]
        full = item["all_pages_screened"]
        detail = item["full_page_detail_viewed"]
        if sorted(full) != list(range(1, source["pages"] + 1)):
            raise ValueError(f"First-pass coverage incomplete: {item['id']}")
        if len(detail) != len(set(detail)) or not set(detail).issubset(full):
            raise ValueError(f"Invalid detailed page coverage: {item['id']}")
        if item["source_sha256"] != source["sha256"]:
            raise ValueError(f"First-pass source mismatch: {item['id']}")
        reference("corpus/" + item["note"])
        screened += len(full)
        close += len(detail)
    deep = data["deep_reading"]
    deep_done = check_items(deep["scores"], deep["planned_scores"])
    deep_pages = 0
    for item in deep["scores"]:
        if item["id"] not in scores or item["pages"] != scores[item["id"]]["pages"]:
            raise ValueError(f"Unknown or changed deep-reading input: {item['id']}")
        if item["status"] == "complete":
            reference(item["note"])
            reference(item["evidence"])
            deep_pages += item["pages"]
        else:
            reference(item["prior_partial_or_topical_note"])
    checked = data["corpus"]["closeout_completed_ids"]
    if len(checked) != len(set(checked)) or not set(checked).issubset(scores):
        raise ValueError("Invalid all-score closeout IDs")
    gould = data["gould"]
    reference(gould["source_note"])
    book_pages: set[int] = set()
    for start, end in gould["read_printed_ranges"]:
        pages = {p + gould["verified_pdf_offset"] for p in range(start, end + 1)}
        if end < start or not pages or book_pages.intersection(pages):
            raise ValueError("Book page ranges reversed or overlapping")
        book_pages.update(pages)
    if min(book_pages) < 1 or max(book_pages) > gould["planned_pdf_pages"]:
        raise ValueError("Book pages outside the planned source")
    resources = data["resources"]
    resource_done = check_items(resources["items"], resources["planned_items"])
    reference(resources["source_note"])
    transfer = data["skill_transfer"]
    transfer_done = check_items(transfer["scenarios"], transfer["planned_scenarios"])
    for item in transfer["scenarios"]:
        reference(item["reference"])
    user = data["user_score"]
    milestone_done = check_items(user["milestones"], 4)
    for item in user["milestones"]:
        reference(item["reference"])
    spec = importlib.util.spec_from_file_location(
        "engraving_library", ROOT / "skills/piano-engraving/scripts/engraving_library.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for topic_files in module.TOPICS.values():
        for filename in topic_files:
            reference(filename)
    if len(module.TOPICS) != data["release"]["planned_topics"]:
        raise ValueError("Skill topic count changed; update the release record")
    return {"as_of": data["as_of"], "scope_revision": data["scope_revision"],
            "goal_status": data["goal_status"], "note": data["counting_policy"],
            "first_pass_scores": [len(reviews["scores"]), planned_scores],
            "first_pass_pages": [screened, planned_pages], "historical_detail_pages": close,
            "deep_scores": [deep_done, deep["planned_scores"]],
            "deep_pages": [deep_pages, sum(s["pages"] for s in deep["scores"])],
            "all_score_closeout": [len(checked), planned_scores],
            "gould_pages_conservative": [len(book_pages), gould["planned_pdf_pages"]],
            "public_resource_scopes": [resource_done, resources["planned_items"]],
            "skill_transfer_scenarios": [transfer_done, transfer["planned_scenarios"]],
            "user_integrated_rounds": [user["completed_integrated_rounds"], user["planned_integrated_rounds"]],
            "user_milestones": [milestone_done, len(user["milestones"])],
            "skill_topics": [len(module.TOPICS), data["release"]["planned_topics"]],
            "release": data["release"]["tag"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate references and scope; still prints the summary")
    parser.parse_args()
    try:
        print(json.dumps(summary(), ensure_ascii=False, indent=2))
        return 0
    except (KeyError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
