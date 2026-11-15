"""Installed MuseScore discovery and the configuration shared with its native panel."""
from __future__ import annotations
import configparser
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def state_directory() -> Path:
    override = os.environ.get("MCP_MUSESCORE_STATE_DIR")
    if override:
        return Path(override)
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share"))
    return base / "Freddd13" / "MuseScoreMCP"


def configuration_path(application: str | None = None) -> Path:
    if application:
        return Path(application).resolve().parent / "kumo.ini"
    executable = Path(sys.executable).resolve()
    for parent in executable.parents:
        if parent.name.lower() == "mcp" and parent.parent.name.lower() == "tools":
            return parent.parent.parent / "kumo.ini"
    return executable.parents[2] / "kumo.ini"


def enabled(path: Path) -> bool:
    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read_string(path.read_text("utf-8-sig"))
        return parser.get("features", "enable_exp_feature").strip().lower() == "true"
    except (OSError, ValueError, configparser.Error):
        return False


def process_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        code = wintypes.DWORD()
        try:
            return bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def instances(application: str | None = None) -> list[dict]:
    result = []
    for path in state_directory().glob("instance-*.json"):
        try:
            value = json.loads(path.read_text("utf-8"))
            if value.get("schema") != 1 or not process_running(int(value["pid"])):
                continue
            if not 1 <= int(value["port"]) <= 65535 or value.get("host") != "127.0.0.1":
                continue
            exe = Path(value["application"]).resolve()
            if application and os.path.normcase(str(exe)) != os.path.normcase(str(Path(application).resolve())):
                continue
            if not enabled(exe.parent / "kumo.ini"):
                continue
            result.append(value)
        except (OSError, KeyError, ValueError, TypeError):
            continue
    return sorted(result, key=lambda v: (bool(v.get("active")), v.get("updated", 0)), reverse=True)


def selected_instance(application: str | None = None) -> dict:
    available = instances(application)
    try:
        selection = json.loads((state_directory() / "selection.json").read_text("utf-8"))
    except (OSError, ValueError):
        selection = {}
    chosen = next((v for v in available if v["id"] == selection.get("id")), None)
    if chosen:
        return chosen
    if len(available) == 1:
        return available[0]
    if len(available) > 1:
        raise RuntimeError("打开了多个 MuseScore 窗口，请在“AI 连接”中选择本次使用的窗口。")
    raise RuntimeError("请打开 MuseScore，并在“AI 连接”中检查扩展功能和连接状态。")


def installed_connection(application: str | None = None) -> tuple[str, int]:
    config = configuration_path(application)
    if not enabled(config):
        raise RuntimeError(f"个人扩展功能已关闭。开启 {config} 中的 enable_exp_feature 后重启 MuseScore。")
    value = selected_instance(application)
    return "127.0.0.1", int(value["port"])


def codex_configuration() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"


def codex_status() -> dict:
    import tomlkit
    config = codex_configuration()
    if not config.exists():
        return {"configured": False, "enabled": False, "configuration": str(config)}
    document = tomlkit.parse(config.read_text("utf-8-sig"))
    server = document.get("mcp_servers", {}).get("musescore")
    return {"configured": server is not None,
            "enabled": server is not None and bool(server.get("enabled", True)),
            "configuration": str(config), "program": str(server.get("command", "")) if server is not None else ""}


def _save_codex(document, old: bytes) -> str:
    import tempfile
    import uuid
    import tomlkit
    config = codex_configuration()
    config.parent.mkdir(parents=True, exist_ok=True)
    backup = ""
    if old:
        backup = str(config.with_name(config.name + ".musescore-" + time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8] + ".bak"))
        with Path(backup).open("xb") as file:
            file.write(old)
    fd, temporary = tempfile.mkstemp(prefix=".musescore-", suffix=".toml", dir=config.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as file:
            file.write(tomlkit.dumps(document))
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, config)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return backup


def set_codex_enabled(value: bool) -> dict:
    import tomlkit
    config = codex_configuration()
    if not config.exists():
        raise RuntimeError("请先点击“配置 Codex”，建立 MuseScore 连接。")
    old = config.read_bytes()
    document = tomlkit.parse(old.decode("utf-8-sig"))
    server = document.get("mcp_servers", {}).get("musescore")
    if server is None:
        raise RuntimeError("请先点击“配置 Codex”，建立 MuseScore 连接。")
    if bool(server.get("enabled", True)) == value:
        return {"ok": True, "codex": codex_status(), "message": "Codex 启动设置已保持。"}
    server["enabled"] = value
    backup = _save_codex(document, old)
    return {"ok": True, "codex": codex_status(), "backup": backup,
            "message": "已开启。请在 Codex 重新连接 MuseScore。" if value else "已关闭 Codex 自动启动。已打开的会话可在下方选择结束。"}


def _link_skill(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform != "win32":
        target.symlink_to(source, target_is_directory=True)
        return
    script = ("$ErrorActionPreference = 'Stop'; "
              "New-Item -ItemType Junction -Path $env:MUSESCORE_SKILL_TARGET "
              "-Target $env:MUSESCORE_SKILL_SOURCE | Out-Null")
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        env={**os.environ, "MUSESCORE_SKILL_TARGET": str(target), "MUSESCORE_SKILL_SOURCE": str(source)},
        check=True, capture_output=True, timeout=8, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def _skill_version(contents: bytes) -> str:
    lines = contents.decode("utf-8-sig", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.fullmatch(r"""[ \t]*version:[ \t]*["']?([^"'\r\n]+?)["']?[ \t]*""", line)
        if match:
            return match.group(1).strip()
    return ""


def _matches_digest(contents: bytes, expected: str) -> bool:
    return (hashlib.sha256(contents).hexdigest() == expected
            or (b"\r\n" in contents
                and hashlib.sha256(contents.replace(b"\r\n", b"\n")).hexdigest() == expected))


def _research_manifest(path: Path) -> dict:
    try:
        result = json.loads(path.read_text("utf-8-sig"))
        return result if isinstance(result, dict) else {}
    except (OSError, ValueError):
        return {}


def _pinned_skill_digest(guide: Path, source: Path, version: str) -> str:
    manifest = _research_manifest(guide.parent / "manifest.json")
    digests = manifest.get("sha256")
    if manifest.get("version") != version or not isinstance(digests, dict):
        return ""
    expected = digests.get("skill/SKILL.md", "")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        return ""
    try:
        if (_matches_digest(source.read_bytes(), expected)
                and _matches_digest(guide.read_bytes(), digests.get(guide.name, ""))):
            return expected
    except OSError:
        pass
    return ""


def check_codex_skills(application: str | None, configure: bool = False) -> list[dict]:
    """Locate installed skills and their local research, optionally linking known sources."""
    executable = Path(application).absolute() if application else Path(sys.executable).absolute()
    upstream = Path(__file__).resolve().parents[1]
    specifications = [
        ("piano-engraving", "钢琴净书", "mcp-musescore", "MCP_MUSESCORE_DIR",
         Path("docs/engraving/README.md"), Path("skills/piano-engraving"), None),
        ("piano-midi-expression", "钢琴力度", "music-explore", "PIANO_EXPRESSION_DIR",
         Path("output/releases/piano-expression-0.3.3/START_HERE.md"),
         Path("output/releases/piano-expression-0.3.3/skill"), "piano-expression-0.3.3"),
    ]
    reports = []
    for name, label, directory, variable, library, skill_source, pinned in specifications:
        target = Path.home() / ".agents" / "skills" / name
        codex = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" / name
        roots = [target.resolve().parents[1], upstream]
        if os.environ.get(variable):
            roots.insert(0, Path(os.environ[variable]).expanduser())
        roots.extend(parent / directory for parent in executable.parents)
        roots.append(upstream.parent / directory)
        matching = None
        rejected = None
        expected = ""
        for root in roots:
            guide, source = root / library, root / skill_source / "SKILL.md"
            if not guide.is_file() or not source.is_file():
                continue
            if pinned:
                expected = _pinned_skill_digest(guide, source, pinned)
                if not expected:
                    rejected = rejected or guide.parent
                    continue
            matching = root
            break
        install_error = ""
        skill = next((directory / "SKILL.md" for directory in (target, codex)
                      if (directory / "SKILL.md").is_file()), target / "SKILL.md")
        if configure and matching and not (skill.is_file() or target.exists() or target.is_symlink()):
            try:
                _link_skill((matching / skill_source).resolve(), target)
            except (OSError, subprocess.SubprocessError) as error:
                install_error = str(error).splitlines()[0]
        try:
            contents = skill.read_bytes()
        except OSError:
            contents = None
        installed = contents is not None
        matches = _matches_digest(contents, expected) if installed and expected else None
        version = pinned if matches else _skill_version(contents) if installed else ""
        library_version = ""
        if matching:
            library_version = pinned or _research_manifest(
                matching / "docs/engraving/release_1_0_0_evidence.json").get("version", "")
        reports.append({
            "name": name, "label": label, "installed": installed,
            "skill": str(skill), "source": str(skill.resolve()) if installed else "",
            "research": str((matching / library).resolve()) if matching else "",
            "version": version, "researchVersion": library_version,
            "requiredVersion": pinned or "", "matchesRelease": matches,
            "researchError": (f"资料版本或校验值与 {pinned} 不符：{rejected}"
                              if rejected and not matching else ""),
            "configureError": install_error,
        })
    return reports


def register_codex(application: str | None = None) -> dict:
    import tomlkit
    config = codex_configuration()
    old = config.read_bytes() if config.exists() else b""
    document = tomlkit.parse(old.decode("utf-8-sig")) if old else tomlkit.document()
    servers = document.setdefault("mcp_servers", tomlkit.table())
    server = servers.setdefault("musescore", tomlkit.table())
    arguments = ([] if getattr(sys, "frozen", False) else [str(Path(__file__).resolve().parents[1] / "launcher.py")]) + ["--stdio"]
    if application:
        arguments += ["--application", str(Path(application).resolve())]
    # Only this server's launch fields change. Other tables and comments remain.
    server["command"] = str(Path(sys.executable).resolve())
    server["args"] = arguments
    for key in ("url", "auth", "bearer_token_env_var", "http_headers", "env_http_headers"):
        if key in server:
            del server[key]
    server.setdefault("enabled", True)
    server["startup_timeout_sec"] = 20
    server["tool_timeout_sec"] = 60
    backup = _save_codex(document, old)
    return {"ok": True, "configuration": str(config), "backup": backup, "codex": codex_status(),
            "skills": check_codex_skills(application, configure=True),
            "message": "已配置 MuseScore。重新连接 Codex 或新建对话后，可以读取当前乐谱。" if server["enabled"] else "已配置 MuseScore。Codex 启动仍为关闭，可在下方勾选开启。"}
