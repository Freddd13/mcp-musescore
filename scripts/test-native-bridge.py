"""Exercise the real QML plugin in an isolated, offscreen MuseScore 3 host."""

import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--exe", required=True, type=Path)
parser.add_argument("--score", required=True, type=Path)
parser.add_argument("--output", type=Path, default=Path(".cache/native-smoke"))
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
work = args.output.resolve()
work.mkdir(parents=True, exist_ok=True)
(work / "settings").mkdir(exist_ok=True)
source = (repo / "tests/native_smoke.qml").read_text(encoding="utf-8")
source = source.replace("__PLUGIN_URL__", (repo / "musescore-mcp-websocket.qml").as_uri())
(work / "smoke.qml").write_text(source, encoding="utf-8")
env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software", QML_DISABLE_DISK_CACHE="1")
command = [str(args.exe.resolve()), "-s", "-m", "-c", str(work / "settings"), "-p", str(work / "smoke.qml"), str(args.score.resolve())]
try:
    result = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=35)
    output, status = result.stdout, result.returncode
except subprocess.TimeoutExpired as error:
    output, status = error.stdout or b"", "timeout"
(work / "smoke.log").write_bytes(output)
report_path = work / "native-smoke.json"
if status == 0 and report_path.exists():
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    print(json.dumps({"status": status, "failures": report["failures"], "report": str(report_path)}, ensure_ascii=True))
    raise SystemExit(bool(report["failures"]))
print(json.dumps({"exit": status, "report": str(report_path)}))
print(output.decode("utf-8", errors="replace")[-6000:])
raise SystemExit(1)
