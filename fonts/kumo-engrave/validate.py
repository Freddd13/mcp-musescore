"""Check source hashes, semantic roundtrip, coverage, widths and metadata."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

from build import ROOT, bounds, load_json, profile_design, base_files
from source.contours import sample_contours, inside, area


def record(glyphs, name):
    pen = RecordingPen()
    glyphs[name].draw(pen)
    return pen.value


def validate(output):
    design = load_json(ROOT / "source/design.json")
    files = dict(load_json(ROOT / "BASELINE.json")["files"])
    files.update(load_json(ROOT / "LELAND_BASELINE.json")["files"])
    for name, expected in files.items():
        assert hashlib.sha256((ROOT / "vendor" / name).read_bytes()).hexdigest() == expected
    result = {}
    for profile, config in design["profiles"].items():
        active_design = profile_design(design, profile)
        music_base, text_base, metadata_base, _ = base_files(config)
        control = config.get("control", profile == "control")
        changed = []
        for is_text in [False, True]:
            family = config["family"] + (" Text" if is_text else "")
            folder = output / profile / family
            digest = hashlib.sha256((folder / (family + ".otf")).read_bytes()).hexdigest()
            if is_text:
                text_digest = digest
            else:
                music_digest = digest
            base_name = text_base if is_text else music_base
            with TTFont(ROOT / "vendor" / base_name) as base, TTFont(folder / (family + ".otf")) as new:
                assert base.getGlyphOrder() == new.getGlyphOrder(), "Glyph order/coverage changed"
                assert base.getBestCmap() == new.getBestCmap(), "Unicode coverage changed"
                expected_metrics = dict(base["hmtx"].metrics)
                advance_changes = {}
                if not control and not is_text:
                    for symbol,spec in active_design["glyphs"].items():
                        if "advance" in spec:
                            name=base.getBestCmap()[int(spec["codepoint"],16)]
                            old=expected_metrics[name]
                            expected_metrics[name]=(spec["advance"],old[1])
                            advance_changes[symbol]=dict(before=old[0],after=spec["advance"])
                assert expected_metrics == new["hmtx"].metrics, "Undeclared advance/side-bearing change"
                if not is_text:
                    music_advance_changes = advance_changes
                assert new["head"].unitsPerEm == 1000
                counts = len(new.getGlyphOrder())
                if is_text:
                    text_count = counts
                else:
                    music_count = counts
                before, after = base.getGlyphSet(), new.getGlyphSet()
                allowed = set() if control or is_text else {
                    new.getBestCmap()[int(spec["codepoint"], 16)] for spec in active_design["glyphs"].values()}
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
                    source_meta = load_json(ROOT / "vendor" / metadata_base)
                    for symbol, spec in ({} if control else active_design["glyphs"]).items():
                        name = new.getBestCmap()[int(spec["codepoint"], 16)]
                        actual = bounds(after, name)
                        box = meta["glyphBBoxes"][symbol]
                        expected = [*box["bBoxSW"], *box["bBoxNE"]]
                        assert all(abs(a / 250 - b) < 1e-5 for a, b in zip(actual, expected))
                        for anchor in ["stemUpSE", "stemDownNW"]:
                            if anchor in source_meta["glyphsWithAnchors"].get(symbol, {}):
                                assert meta["glyphsWithAnchors"][symbol][anchor] == source_meta["glyphsWithAnchors"][symbol][anchor]
                        if spec.get("head"):
                            recording=RecordingPen();after[name].draw(recording)
                            contours=sample_contours(recording,128)
                            assert len(contours)==(1 if symbol=='noteheadBlack' else 2)
                            if len(contours)==2:
                                assert area(contours[0])*area(contours[1])<0,"Counter winding"
                                assert all(inside(contours[0],p) for p in contours[1]),"Counter leaves exterior"
                            for key in ('stemDownNW','stemUpSE'):
                                point=meta['glyphsWithAnchors'][symbol].get(key)
                                if point:
                                    x=point[0]*250+(8 if key=='stemDownNW' else -8)
                                    y=point[1]*250
                                    assert inside(contours[0],(x,y)),(symbol,key,'detached stem')
                                    assert len(contours)==1 or not inside(contours[1],(x,y)),(symbol,key,'stem enters counter')
                        if not control and "counter" in spec:
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
                           "changed_outlines": changed, "advances_preserved": not bool(music_advance_changes),
                           "declared_advance_changes": music_advance_changes,
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
