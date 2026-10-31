"""CLI regression and curated source-location checks, not musical accuracy tests."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/piano-engraving/scripts/engraving_library.py"
LIBRARY = ROOT / "docs/engraving"
spec = importlib.util.spec_from_file_location("engraving_skill_locator", SCRIPT)
locator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(locator)


class EngravingLibraryTests(unittest.TestCase):
    def run_cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(SCRIPT),
                                 "--repo", str(ROOT), *args], capture_output=True)
        self.assertEqual(result.returncode, expected, result.stderr.decode("utf8"))
        return json.loads(result.stdout) if expected == 0 else result

    def test_existing_topic_listing_and_all_twenty_routes(self):
        listed = self.run_cli("--list-topics")["topics"]
        self.assertEqual(len(listed), 20)
        for topic, names in listed.items():
            with self.subTest(topic=topic):
                data = self.run_cli("--topic", topic)
                self.assertNotIn("matches", data)
                self.assertEqual(data["references"], [str(LIBRARY / n) for n in names])
                self.assertTrue(all(Path(p).is_file() for p in data["references"]))

    def test_curated_source_locations(self):
        cases = [
            ("notation", "6:3 等值", "DOUBLED_TUPLET_STUDY.md"),
            ("rhythm", "摇摆 共同起点", "SWING_ALIGNMENT_STUDY.md"),
            ("piano", "S.P. A八度", "PREFERENCES.md"),
            ("baseline", "共同Segment 保存", "USER_COMBINED_REVIEW.md"),
            ("cross-staff", "跨谱表 休止", "CROSS_STAFF_STUDY.md"),
        ]
        for topic, question, expected in cases:
            with self.subTest(question=question):
                data = self.run_cli("--topic", topic, "--query", question, "--limit", "3")
                self.assertIn(expected, [Path(m["path"]).name for m in data["matches"]])
                self.assertLessEqual(len(data["matches"]), 3)
                self.assertEqual(data["references"], [m["path"] for m in data["matches"]])
                self.assertEqual(len(set(data["references"])), len(data["references"]))
                for match in data["matches"]:
                    self.assertGreater(match["line"], 0)
                    self.assertLessEqual(len(match["excerpt"]), 700)
                    source = Path(match["path"]).read_text(encoding="utf8")
                    self.assertIn(match["excerpt"].strip("…"), source)
                    lines = source.splitlines()
                    self.assertTrue(lines[match["line"] - 1].strip())

    def test_fullwidth_ratio_works_like_ascii(self):
        def matches(query):
            return self.run_cli("--topic", "notation", "--query", query)["matches"]
        self.assertEqual(matches("６：３ 等值"), matches("6:3 等值"))

    def test_missing_query_has_no_fake_references(self):
        data = self.run_cli("--topic", "notation", "--query", "zzzz_unmatched_268034")
        self.assertEqual(data["matches"], [])
        self.assertEqual(data["references"], [])
        self.assertEqual(data["matching_files"], 0)
        self.assertEqual(len(data["start_here"]), 3)

    def test_invalid_limits_and_empty_search(self):
        for args in [("--limit", "3"), ("--query", "rest", "--limit", "0"),
                     ("--query", "rest", "--limit", "21"), ("--query", "   ")]:
            with self.subTest(args=args):
                self.run_cli(*args, expected=2)

    def test_search_keeps_library_sources_unchanged(self):
        def snapshot():
            return {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in LIBRARY.rglob("*.md")}
        before = snapshot()
        self.run_cli("--topic", "spacing", "--query", "变音记号 共同时间列", "--limit", "2")
        self.assertEqual(before, snapshot())


if __name__ == "__main__":
    unittest.main()
