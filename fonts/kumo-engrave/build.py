"""Build isolated OFL prototypes without recompiling unaffected CFF glyphs.

The source is a parameterized, independently drawn four-cubic affine ellipse,
not a traced/extracted reference glyph. Run with fontTools 4.38.0.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import zipfile
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
KAPPA = 4 * (math.sqrt(2) - 1) / 3


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def profile_design(design, profile):
    resolved = copy.deepcopy(design)
    resolved["glyphs"].update(design["profiles"][profile].get("glyph_overrides", {}))
    return resolved


def ellipse(pen, cx, cy, rx, ry, shear, reverse=False):
    """Four cubic arcs; reverse the hole so CFF nonzero filling stays hollow."""
    direction = -1 if reverse else 1

    def pt(x, y):
        return (cx + rx * x, cy + direction * ry * y + shear * rx * x)

    pen.moveTo(pt(1, 0))
    for points in [((1, KAPPA), (KAPPA, 1), (0, 1)),
                   ((-KAPPA, 1), (-1, KAPPA), (-1, 0)),
                   ((-1, -KAPPA), (-KAPPA, -1), (0, -1)),
                   ((KAPPA, -1), (1, -KAPPA), (1, 0))]:
        pen.curveTo(*(pt(*point) for point in points))
    pen.closePath()


def outline(spec, counter_scale):
    x0, y0, x1, y1 = spec["outer_box"]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, extent_y = (x1 - x0) / 2, (y1 - y0) / 2
    shear = spec["outer_shear"]
    ry = math.sqrt(extent_y ** 2 - (shear * rx) ** 2)
    result = RecordingPen()
    ellipse(result, cx, cy, rx, ry, shear)
    if "counter" in spec:
        hole = spec["counter"]
        ellipse(result, cx, cy, hole["radius_x"], hole["radius_y"] * counter_scale,
                hole["shear"], reverse=True)
    return result


def bounds(glyph_set, name):
    pen = BoundsPen(glyph_set)
    glyph_set[name].draw(pen)
    return pen.bounds


def rename(font, family, version, addition):
    ps_name = family.replace(" ", "")
    replacements = {1: family, 2: "Regular", 3: f"{ps_name};{version};Freddd13",
                    4: family, 5: f"Version {version}", 6: ps_name,
                    16: family, 17: "Regular"}
    for record in font["name"].names:
        if record.nameID in replacements:
            record.string = replacements[record.nameID].encode(record.getEncoding())
        elif record.nameID == 0:
            record.string = (record.toUnicode() + " " + addition).encode(record.getEncoding(), errors="replace")
    for name_id, value in replacements.items():
        font["name"].setName(value, name_id, 3, 1, 0x409)
    cff = font["CFF "].cff
    cff.fontNames = [ps_name]
    top = cff.topDictIndex[0]
    top.FullName, top.FamilyName, top.version = family, family, version
    top.Notice = getattr(top, "Notice", "") + " " + addition
    font["head"].fontRevision = float(version)
    # Any original signature no longer authenticates a renamed/modified font.
    if "DSIG" in font:
        del font["DSIG"]


def make_font(base_path, output_path, family, design, profile):
    font = TTFont(base_path, recalcTimestamp=False)
    rename(font, family, design["version"], design["copyright_addition"])
    changed = []
    if profile != "control":
        top = font["CFF "].cff.topDictIndex[0]
        cmap = font.getBestCmap()
        for symbol, spec in design["glyphs"].items():
            name = cmap[int(spec["codepoint"], 16)]
            advance = font["hmtx"].metrics[name][0]
            # Type 2 encodes width relative to nominalWidthX, not absolute hmtx width.
            width_delta = advance - getattr(top.Private, "nominalWidthX", 0)
            pen = T2CharStringPen(width_delta, font.getGlyphSet())
            outline(spec, design["profiles"][profile]["counter_scale"]).replay(pen)
            top.CharStrings[name] = pen.getCharString(private=top.Private, globalSubrs=top.GlobalSubrs)
            changed.append((symbol, name))
    font.save(output_path)
    font.close()
    return changed


def update_head_metadata(meta, font_path, changed, design):
    with TTFont(font_path) as font:
        glyphs = font.getGlyphSet()
        unit = design["units_per_staff_space"]
        for symbol, name in changed:
            x0, y0, x1, y1 = bounds(glyphs, name)
            meta["glyphBBoxes"][symbol] = {"bBoxNE": [round(x1 / unit, 6), round(y1 / unit, 6)],
                                         "bBoxSW": [round(x0 / unit, 6), round(y0 / unit, 6)]}
            spec = design["glyphs"][symbol]
            sx0, sy0, sx1, sy1 = spec["outer_box"]
            cx, cy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
            rx = (sx1 - sx0) / 2
            ry = math.sqrt(((sy1 - sy0) / 2) ** 2 - (spec["outer_shear"] * rx) ** 2)

            def edge(x, upper):
                x = min(max(x, sx0), sx1)
                height = ry * math.sqrt(max(0, 1 - ((x - cx) / rx) ** 2))
                return cy + spec["outer_shear"] * (x - cx) + (height if upper else -height)

            anchors = meta["glyphsWithAnchors"].setdefault(symbol, {})
            # Keep ordinary stem attachment points; update optical cutouts and split anchors.
            for corner, fraction, upper in [("cutOutNW", .17, True), ("cutOutSE", .83, False)]:
                x = sx0 + fraction * (sx1 - sx0)
                y = edge(x, upper) + (1 if upper else -1)
                anchors[corner] = [round(x / unit, 6), round(y / unit, 6)]
            for key, point in list(anchors.items()):
                if key.startswith("splitStem"):
                    x = point[0] * unit
                    anchors[key] = [point[0], round(edge(x, "Up" in key) / unit, 6)]


def draw_svg(font_path, output_path):
    """Actual rebuilt glyphs at common scale on staff lines, editable SVG."""
    with TTFont(font_path) as font:
        cmap, glyphs = font.getBestCmap(), font.getGlyphSet()
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1700 460">',
                 '<rect width="1700" height="460" fill="white"/>']
        for index, cp in enumerate([0xE0A4, 0xE0A3, 0xE0A2]):
            x = 90 + index * 540
            for line in range(-2, 3):
                y = 230 + line * 70
                parts.append(f'<path d="M{x-35} {y}h470" stroke="#777" stroke-width="6.37"/>')
            pen = SVGPathPen(glyphs)
            glyphs[cmap[cp]].draw(pen)
            parts.append(f'<path d="{pen.getCommands()}" transform="translate({x+110} 230) scale(.28 -.28)" fill="black"/>')
        parts.append('</svg>')
        output_path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def build(output):
    design = load_json(ROOT / "source/design.json")
    baseline = load_json(ROOT / "BASELINE.json")
    for name, expected in baseline["files"].items():
        actual = hashlib.sha256((ROOT / "vendor" / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Baseline hash mismatch: {name}")
    output.mkdir(parents=True, exist_ok=True)
    report = {"version": design["version"], "baseline": baseline, "profiles": {}}
    for profile, config in design["profiles"].items():
        active_design = profile_design(design, profile)
        family = config["family"]
        pack = output / profile
        for is_text in [False, True]:
            name = family + (" Text" if is_text else "")
            directory = pack / name
            directory.mkdir(parents=True, exist_ok=True)
            base_file = "FinaleMaestroText-Regular.otf" if is_text else "FinaleMaestro.otf"
            font_path = directory / (name + ".otf")
            changed = make_font(ROOT / "vendor" / base_file, font_path, name, active_design,
                                "control" if is_text else profile)
            metadata_file = "Finale Maestro Text.json" if is_text else "FinaleMaestro.json"
            meta = copy.deepcopy(load_json(ROOT / "vendor" / metadata_file))
            meta.update(fontName=name, fontVersion=float(design["version"]))
            update_head_metadata(meta, font_path, changed, active_design)
            write_json(directory / (name + ".json"), meta)
            license_text = (ROOT / "vendor/OFL.txt").read_text(encoding="utf-8")
            (directory / "OFL.txt").write_text(design["copyright_addition"] + "\n\n" + license_text,
                                               encoding="utf-8")
            (directory / "SOURCE.txt").write_text(
                "OFL derivative of MakeMusic Finale Maestro.\n"
                f"Kumo prototype {design['version']}; profile {profile}.\n"
                "Only the three normal notehead glyphs are redesigned; Text outlines are unchanged.\n"
                "Source, baseline hashes and limitations: fonts/kumo-engrave in Freddd13/mcp-musescore.\n",
                encoding="utf-8")
            if not is_text:
                draw_svg(font_path, pack / "noteheads.svg")
        report["profiles"][profile] = {"family": family, "description": config["description"]}
    write_json(output / "build-report.json", report)
    print(f"Built {len(design['profiles'])} isolated profile pairs in {output}")


def package(output):
    """Package an explicit allowlist, including the latest validation report."""
    design = load_json(ROOT / "source/design.json")
    validation = load_json(output / "validation.json")
    assert set(validation) == set(design["profiles"]), "Validate every current profile first"
    files = []
    for profile in design["profiles"]:
        family = design["profiles"][profile]["family"]
        for suffix, key in [("", "music_sha256"), (" Text", "text_sha256")]:
            name = family + suffix
            file = output / profile / name / (name + ".otf")
            assert hashlib.sha256(file.read_bytes()).hexdigest() == validation[profile][key], "Font changed since validation"
        files.extend((p, p.relative_to(output).as_posix())
                     for p in sorted((output / profile).rglob("*")) if p.is_file())
    for name in ["build-report.json", "validation.json"]:
        if (output / name).exists():
            files.append((output / name, name))
    for name in ["README.md", "VERIFICATION.md", "CHANGELOG.md", "DESIGN_BRIEF.md", "verification.json"]:
        if (ROOT / name).exists():
            files.append((ROOT / name, name))
    with zipfile.ZipFile(output / "kumo-engrave-0.1.0-prototypes.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for file, member in sorted(files, key=lambda pair: pair[1]):
            info = zipfile.ZipInfo(member, date_time=(2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--package-only", action="store_true")
    args = parser.parse_args()
    (package if args.package_only else build)(args.output.resolve())
