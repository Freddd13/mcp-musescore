"""Configuration checks the fixed piano research release before linking its skill."""
import hashlib
import json
from pathlib import Path

import pytest

from src import runtime


PIN = "piano-expression-0.3.3"


@pytest.fixture
def expression_release(tmp_path, monkeypatch):
    home = tmp_path / "user"
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    # Exclude real sibling research checkouts from the fake installation.
    isolated = Path(tmp_path.anchor) / "mcp-skill-configuration-fixture"
    monkeypatch.setattr(runtime, "__file__", str(isolated / "src" / "runtime.py"))
    monkeypatch.setenv("CODEX_HOME", str(home / ".codex"))
    root = tmp_path / "钢琴研究"
    monkeypatch.setenv("PIANO_EXPRESSION_DIR", str(root))
    release = root / "output" / "releases" / PIN
    files = {
        "START_HERE.md": b"# Fixed piano expression study\n",
        "skill/SKILL.md": b"---\nname: piano-midi-expression\n---\n# Fixed skill\n",
    }
    for name, contents in files.items():
        path = release / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
    (release / "manifest.json").write_text(json.dumps({
        "version": PIN,
        "sha256": {name: hashlib.sha256(contents).hexdigest() for name, contents in files.items()},
    }), encoding="utf-8")
    return release, home / ".agents" / "skills" / "piano-midi-expression"


def expression_report(configure=False):
    installation = Path(Path.home().anchor) / "mcp-skill-configuration-fixture" / "MuseScore3Evo.exe"
    return next(report for report in runtime.check_codex_skills(str(installation), configure=configure)
                if report["name"] == "piano-midi-expression")


def test_verified_release_links_matching_skill(expression_release, monkeypatch):
    release, target = expression_release
    missing = expression_report()
    assert missing["researchVersion"] == PIN
    assert missing["version"] == ""
    assert missing["matchesRelease"] is None
    links = []

    def link(source, destination):
        links.append((source, destination))
        destination.mkdir(parents=True)
        contents = (source / "SKILL.md").read_bytes().replace(b"\n", b"\r\n")
        (destination / "SKILL.md").write_bytes(contents)

    monkeypatch.setattr(runtime, "_link_skill", link)
    report = expression_report(configure=True)
    assert (release / "skill", target) in links
    assert report["installed"]
    assert report["matchesRelease"]
    assert report["version"] == report["researchVersion"] == report["requiredVersion"] == PIN


def test_existing_old_skill_is_reported_and_preserved(expression_release, monkeypatch):
    _, target = expression_release
    target.mkdir(parents=True)
    contents = b'---\nname: piano-midi-expression\nversion: "0.2.0"\n---\n# Keep my files\n'
    (target / "SKILL.md").write_bytes(contents)
    links = []
    monkeypatch.setattr(runtime, "_link_skill", lambda source, destination: links.append(destination))
    report = expression_report(configure=True)
    assert target not in links
    assert (target / "SKILL.md").read_bytes() == contents
    assert report["version"] == "0.2.0"
    assert report["researchVersion"] == report["requiredVersion"] == PIN
    assert report["matchesRelease"] is False


@pytest.mark.parametrize("changed", ["manifest.json", "skill/SKILL.md", "START_HERE.md"])
def test_changed_release_is_not_linked(expression_release, monkeypatch, changed):
    release, target = expression_release
    (release / changed).write_text("Unverified content\n", encoding="utf-8")
    links = []
    monkeypatch.setattr(runtime, "_link_skill", lambda source, destination: links.append(destination))
    report = expression_report(configure=True)
    assert target not in links
    assert not report["installed"]
    assert report["version"] == report["researchVersion"] == ""
    assert report["requiredVersion"] == PIN
    assert report["researchError"]
