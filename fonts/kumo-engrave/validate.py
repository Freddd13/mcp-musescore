"""Check source hashes, semantic roundtrip, coverage, widths and metadata."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

from build import ROOT, bounds, load_json, profile_design


def record(glyphs, name):
    pen = RecordingPen()
    glyphs[name].draw(pen)
    return pen.value


def validate(output):
    design = load_json(ROOT / "source/design.json")
    for name, expected in load_json(ROOT / "BASELINE.json")["files"].items():
        assert hashlib.sha256((ROOT / "vendor" / name).read_bytes()).hexdigest() == expected
    result = {}
    for profile, config in design["profiles"].items():
        active_design = profile_design(design, profile)
        changed = []
        for is_text in [False, True]:
            family = config["family"] + (" Text" if is_text else "")
            folder = output / profile / family
            digest = hashlib.sha256((folder / (family + ".otf")).read_bytes()).hexdigest()
            if is_text:
                text_digest = digest
            else:
                music_digest = digest
            base_name = "FinaleMaestroText-Regular.otf" if is_text else "FinaleMaestro.otf"
            with TTFont(ROOT / "vendor" / base_name) as base, TTFont(folder / (family + ".otf")) as new:
                assert base.getGlyphOrder() == new.getGlyphOrder(), "Glyph order/coverage changed"
                assert base.getBestCmap() == new.getBestCmap(), "Unicode coverage changed"
                assert base["hmtx"].metrics == new["hmtx"].metrics, "Advances/side bearings changed"
                assert new["head"].unitsPerEm == 1000
                counts = len(new.getGlyphOrder())
                if is_text:
                    text_count = counts
                else:
                    music_count = counts
                before, after = base.getGlyphSet(), new.getGlyphSet()
                allowed = set() if profile == "control" or is_text else {
                    new.getBestCmap()[int(spec["codepoint"], 16)] for spec in design["glyphs"].values()}
                for name in base.getGlyphOrder():
                    different = record(before, name) != record(after, name)
                    assert not different or name in allowed, f"Unexpected outline change: {name}"
                    if different:
                        changed.append(name)
                    # CFF width must agree with hmtx even for freshly encoded glyphs.
                    char = new["CFF "].cff.topDictIndex[0].CharStrings[name]
                    char.draw(RecordingPen())
                    assert char.width == new["hmtx"].metrics[name][0], f"CFF width differs: {name}"
                assert set(changed if not is_text else []) == allowed, "Expected redesign not present"
                assert new["name"].getDebugName(1) == family, "Family name mismatch"
                assert new["CFF "].cff.fontNames == [family.replace(" ", "")]
                meta = load_json(folder / (family + ".json"))
                assert meta["fontName"] == family
                if not is_text:
                    source_meta = load_json(ROOT / "vendor/FinaleMaestro.json")
                    for symbol, spec in active_design["glyphs"].items():
                        name = new.getBestCmap()[int(spec["codepoint"], 16)]
                        actual = bounds(after, name)
                        box = meta["glyphBBoxes"][symbol]
                        expected = [*box["bBoxSW"], *box["bBoxNE"]]
                        assert all(abs(a / 250 - b) < 1e-5 for a, b in zip(actual, expected))
                        for anchor in ["stemUpSE", "stemDownNW"]:
                            if anchor in source_meta["glyphsWithAnchors"][symbol]:
                                assert meta["glyphsWithAnchors"][symbol][anchor] == source_meta["glyphsWithAnchors"][symbol][anchor]
                        if profile != "control" and "counter" in spec:
                            # Analytic hole must remain fully inside the outer ellipse.
                            x0, y0, x1, y1 = spec["outer_box"]
                            rx = (x1 - x0) / 2
                            ry = math.sqrt(((y1 - y0) / 2) ** 2 - (spec["outer_shear"] * rx) ** 2)
                            hole = spec["counter"]
                            for i in range(512):
                                angle = i * math.tau / 512
                                x = hole["radius_x"] * math.cos(angle)
                                y = hole["radius_y"] * config["counter_scale"] * math.sin(angle) + hole["shear"] * x
                                assert (x / rx) ** 2 + ((y - spec["outer_shear"] * x) / ry) ** 2 < .98
        result[profile] = {"music_glyphs": music_count, "text_glyphs": text_count,
                           "music_sha256": music_digest, "text_sha256": text_digest,
                           "changed_outlines": changed, "advances_preserved": True,
                           "normal_stem_anchors_preserved": True}
    # Open is a controlled counter experiment: black glyph and all outer arcs
    # must be byte-for-byte equivalent at the recorded outline level.
    families = [design["profiles"][p]["family"] for p in ["balanced", "open"]]
    with TTFont(output / "balanced" / families[0] / (families[0] + ".otf")) as a, \
            TTFont(output / "open" / families[1] / (families[1] + ".otf")) as b:
        for spec in design["glyphs"].values():
            name = a.getBestCmap()[int(spec["codepoint"], 16)]
            ra, rb = record(a.getGlyphSet(), name), record(b.getGlyphSet(), name)
            assert ra[:6] == rb[:6], "Open unexpectedly changed an outer contour"
            if "counter" not in spec:
                assert ra == rb
    (output / "validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    validate(parser.parse_args().output.resolve())
