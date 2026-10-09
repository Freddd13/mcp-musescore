"""Native Windows font-only proofs in a new, isolated directory; originals read-only.

No global font installation, no user preferences, no score overwrites, no PDF
authoring. Requires a MuseScore 3 Evolution executable and a completed build.
"""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_style_xml(root):
    root = copy.deepcopy(root)
    for score in root.findall("Score"):
        for style in score.findall("Style"):
            score.remove(style)
    return ET.tostring(root)


def set_font(source, destination, family, text_family):
    root = ET.fromstring(source)
    score = root.find("Score")
    style = score.find("Style")
    if style is None:
        style = ET.SubElement(score, "Style")
    for key, value in [("musicalSymbolFont", family), ("musicalTextFont", text_family)]:
        element = style.find(key)
        if element is None:
            element = ET.SubElement(style, key)
        element.text = value
    ET.ElementTree(root).write(destination, encoding="utf-8", xml_declaration=True)
    assert no_style_xml(ET.fromstring(source)) == no_style_xml(ET.parse(destination).getroot())


def run(args):
    out = args.output.resolve()
    if out.exists():
        raise ValueError("Use a new output directory; proofs never replace earlier files")
    out.mkdir(parents=True)
    fonts = out / "ScoreFonts"
    fonts.mkdir()
    design = json.loads((ROOT / "source/design.json").read_text(encoding="utf-8"))
    selected = args.profiles.split(',') if args.profiles else list(design["profiles"])
    for profile in selected:
        config = design["profiles"][profile]
        for family in [config["family"], config["family"] + " Text"]:
            shutil.copytree(args.fonts / profile / family, fonts / family)
    config = out / "config"
    (config / "MuseScore").mkdir(parents=True)
    (config / "MuseScore/MuseScore3Evo.ini").write_text(
        "[application]\npaths\\myScoreFonts=" + fonts.as_posix() + "\n", encoding="utf-8")
    env = os.environ.copy()
    env.update(QT_QPA_PLATFORM="windows", QT_QUICK_BACKEND="software", QML_DISABLE_DISK_CACHE="1")
    prefix = [str(args.musescore), "-s", "-m", "-c", str(config)]

    def convert(label, options, source):
        result = subprocess.run(prefix + options + [str(source)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (out / (label + ".log")).write_bytes(result.stdout)
        if result.returncode:
            raise RuntimeError(f"Native conversion failed ({result.returncode}): {label}")
        print(label, "OK", flush=True)

    fixture = out / "fixture.mscx"
    convert("import-fixture", ["-o", str(fixture)], args.fixture or ROOT / "fixtures/piano-heads.musicxml")
    inputs = {"fixture": fixture.read_bytes()}
    originals = {}
    if args.score:
        source = args.score.resolve()
        originals[str(source)] = digest(source)
        if source.suffix.lower() == ".mscz":
            with zipfile.ZipFile(source) as archive:
                candidates = [n for n in archive.namelist() if n.endswith(".mscx")]
                if len(candidates) != 1:
                    raise ValueError("Expected one primary MSCX in score archive")
                inputs["user"] = archive.read(candidates[0])
        else:
            inputs["user"] = source.read_bytes()
    results = {"host": str(args.musescore), "host_sha256": digest(args.musescore),
               "originals": originals, "font_config": str(config),
               "text_mode": args.text_mode, "proofs": {}}
    variants = {"maestro": "Finale Maestro", "leland": "Leland", **{k: design["profiles"][k]["family"] for k in selected}}
    for sample, source in inputs.items():
        for variant, family in variants.items():
            label = sample + "-" + variant
            score = out / (label + ".mscx")
            # The built-in Text family has Qt substitutions that a renamed family
            # does not inherit. Keep Text fixed when judging notehead changes.
            text_family = family + " Text" if args.text_mode == "paired" else args.fixed_text
            set_font(source, score, family, text_family)
            probe = out / (label + "-probe.qml")
            report_path = out / (label + "-probe.json")
            probe.write_text('''import QtQuick 2.0
import MuseScore 3.0
import FileIO 3.0
MuseScore {
    menuPath: "Plugins.Kumo isolated font proof"
    requiresScore: true
    FileIO { id: report }
    onRun: {
        var symbol = curScore.style.value("musicalSymbolFont");
        var text = curScore.style.value("musicalTextFont");
        var names = Qt.fontFamilies();
        var data = {symbol: symbol, text: text, pages: curScore.npages,
                    symbolRegistered: names.indexOf(symbol) >= 0,
                    textRegistered: names.indexOf(text) >= 0};
        report.source = REPORT_PATH;
        report.write(JSON.stringify(data, null, 2));
    }
}
'''.replace("REPORT_PATH", json.dumps(str(report_path))), encoding="utf-8")
            convert(label + "-svg", ["-p", str(probe), "-o", str(out / (label + ".svg"))], score)
            state = json.loads(report_path.read_text(encoding="utf-8"))
            if state["symbol"] != family or state["text"] != text_family or not state["symbolRegistered"] or not state["textRegistered"]:
                raise RuntimeError(f"Font registration not verified: {state}")
            convert(label + "-png", ["-r", str(args.dpi), "-o", str(out / (label + ".png"))], score)
            results["proofs"][label] = state
    for path, expected in originals.items():
        assert digest(Path(path)) == expected, "Original score changed"
    (out / "native-report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("Verified original hash and native registration; results in", out, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--musescore", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fonts", type=Path, default=ROOT / "dist")
    parser.add_argument("--score", type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--profiles", help="Comma-separated profiles to render; default all")
    parser.add_argument("--fixture", type=Path, help="Alternative authored MusicXML fixture")
    parser.add_argument("--fixed-text", default="Finale Maestro Text")
    parser.add_argument("--text-mode", choices=["fixed", "paired"], default="fixed",
                        help="fixed isolates noteheads; paired tests experimental renamed Text")
    run(parser.parse_args())
