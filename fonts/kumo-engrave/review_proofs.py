"""Compare opaque native PNGs and create common-scale review boards (Pillow)."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from PIL import Image, ImageChops, ImageDraw, ImageFont


def opaque(path):
    image = Image.open(path).convert("RGBA")
    paper = Image.new("RGBA", image.size, "white")
    paper.alpha_composite(image)
    return paper.convert("RGB")


def review(root):
    root = root.resolve()
    native = json.loads((root / "native-report.json").read_text(encoding="utf-8"))
    proofs = {}
    labels_present = list(native['proofs'])
    raw = sorted(p for p in root.glob("*.png")
                 if any(re.fullmatch(re.escape(label)+r'-\d+',p.stem) for label in labels_present))
    for file in raw:
        opaque(file).save(file.with_name(file.stem + "-white.png"))
    for file in raw:
        baseline = 'leland' if '-leland-' in file.name and '-leland-control-' not in file.name else 'maestro'
        counterpart = 'leland-control' if baseline=='leland' else 'control'
        if ('-'+baseline+'-') not in file.name:
            continue
        control = file.with_name(file.name.replace('-'+baseline+'-', '-'+counterpart+'-'))
        if not control.exists():continue
        before, after = opaque(file), opaque(control)
        assert before.size == after.size, "Rename-only control changed page dimensions"
        bbox = ImageChops.difference(before, after).getbbox()
        proofs[file.stem] = {"control_pixel_identical": bbox is None, "difference_bbox": bbox}
        # MuseScore 3 has name-specific Leland bracket branches. The authored
        # two-staff fixture excludes this; six-staff originals do not.
        if native["text_mode"] == "fixed" and (baseline!='leland' or file.name.startswith('fixture-')):
            assert bbox is None, "Music-only control must reproduce the baseline"
    try:
        label_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    except OSError:
        label_font = ImageFont.load_default()
    labels = {"maestro": "Finale Maestro (baseline)", "balanced": "Kumo Engrave",
              "open": "Kumo Engrave Open (larger counters)"}
    if (root / "fixture-jp-1.png").exists():
        labels = {"maestro": "Finale Maestro (baseline)",
                  "open": "Kumo Engrave Open (initial engineering study)",
                  "jp": "Kumo Engrave JP (publication-direction study)"}
    if (root/'fixture-piano-1.png').exists():
        labels={'maestro':'Finale Maestro (fixed Leland Text)',
                'leland-control':'Kumo Piano Control (unmodified Leland; same host name branches)',
                'piano':'Kumo Piano 0.2 (independent palette)'}
    # Identical pixel boxes, never independently fitting a glyph or staff.
    cases = [("fixture", 1, (160, 330, 1430, 545), "fixture"),
             ("user", 2, (80, 420, 1400, 850), "user-p2"),
             ("user", min(native['proofs'].get('user-piano',{}).get('pages',9),9), (60, 65, 1430, 680), "user-last-page")]
    boards = []
    if 'piano' in labels:
        for page in range(1,native['proofs']['fixture-piano']['pages']+1):
            image=opaque(root/f'fixture-piano-{page}.png')
            cases.append(('fixture',page,(70,170,image.width-50,image.height-80),'palette-p'+str(page)))
    for sample, page, box, title in cases:
        if not (root / f"{sample}-maestro-{page}.png").exists():
            continue
        rows = []
        for variant in labels:
            crop = opaque(root / f"{sample}-{variant}-{page}.png").crop(box)
            crop = crop.resize((crop.width * 2, crop.height * 2))
            row = Image.new("RGB", (crop.width, crop.height + 50), "white")
            row.paste(crop, (0, 50))
            ImageDraw.Draw(row).text((10, 8), labels[variant], font=label_font, fill="black")
            rows.append(row)
        board = Image.new("RGB", (rows[0].width, sum(row.height for row in rows)), "white")
        y = 0
        for row in rows:
            board.paste(row, (0, y))
            y += row.height
        path = root / ("comparison-" + title + ".png")
        board.save(path)
        boards.append(path.name)
    report = {"text_mode": native["text_mode"], "opaque_control_comparison": proofs,
              "leland_host_name_branches": 'Authored two-staff fixture must match; full-score differences are recorded. bracket.cpp caps brace span at 4 and adjusts bracket ends only for the exact Leland name.',
              "boards": boards, "originals_unchanged": True}
    for path, expected in native["originals"].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected
    (root / "review-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    review(parser.parse_args().output)
