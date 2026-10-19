"""Prepare a separate local 0.71 host with Study fonts and private settings.

Copies the already validated install tree, never changes the user's installed
program/configuration. The destination must be new and under this study's dist.
The launcher is for the user to open interactively; this tool does not run it.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
HOST_SHA='be8c3894c01256fbe039085981dbd5ccd26da8e0a7b80f051e81b15be2878d8b'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    source=args.source.resolve();out=args.output.resolve();dist=(ROOT/'dist').resolve()
    assert dist in out.parents and not out.exists()
    assert source!=out and source not in out.parents
    assert digest(source/'bin/MuseScore3Evo.exe')==HOST_SHA
    files={p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()}
    shutil.copytree(source,out)
    for name,sha in files.items():assert digest(out/name)==sha
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    study_fonts={}
    for family in ('Kumo Score Study','Kumo Score Study Text'):
        shutil.copytree(args.fonts/family,out/'ScoreFonts'/family)
        sha=digest(out/'ScoreFonts'/family/(family+'.otf'))
        assert sha==build['fonts'][family]['sha256'];study_fonts[family]=sha
    profile=out/'profile/MuseScore';profile.mkdir(parents=True)
    (profile/'MuseScore3Evo.ini').write_bytes(('[application]\npaths\\myScoreFonts='+(out/'ScoreFonts').as_posix()+'\n').encode('utf-8'))
    # User double-clicks this interactive launcher after closing the old GUI.
    # Fixed arguments only; it does not forward arbitrary shell input.
    (out/'Start-Font-Study.cmd').write_bytes(b'@echo off\r\nstart "" "%~dp0bin\\MuseScore3Evo.exe" -c "%~dp0profile"\r\n')
    (out/'READ_ME.txt').write_bytes(('Evolution 0.71 字体本机试用构建\n\n'
        '先退出正在运行的Evolution，再双击Start-Font-Study.cmd。此构建使用独立profile，已配置两套Kumo Score Study字体。\n'
        '打开乐谱副本，在格式→样式→乐谱同时选Kumo Score Study和Kumo Score Study Text。源谱勿覆盖。\n'
        '现有安装程序和原设置未替换。这里的配置独立，字体本身不依赖MCP；需要桥接时按项目插件说明启用。\n'
        '这是本机已验证构建的完整副本，未承诺跨机器安装。移动目录后请重新指定Score Fonts路径。\n'
        '源码定位：Freddd13/MuseScore personal-v0.71.0；波浪滑音可选接口已在原生谱例验证。\n'
        '字体使用说明：mcp-musescore/fonts/kumo-engrave/CURRENT_USAGE.md。\n').encode('utf-8'))
    assert digest(source/'bin/MuseScore3Evo.exe')==HOST_SHA
    manifest=dict(host_sha256=HOST_SHA,source=str(source),destination=str(out),native_source_files=files,
                  all_native_files_identical=True,native_source_tag='personal-v0.71.0',study_font_hashes=study_fonts,
                  independent_profile=True,installed_program_or_user_preferences_modified=False,
                  launcher_executed=False)
    (out/'FONT_STUDY_HOST.json').write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('Separate 0.71 host copied:',len(files),'native files, fonts preconfigured; original installation unchanged')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'../../tmp/fi')
    p.add_argument('--fonts',type=Path,default=ROOT/'dist/corpus-font-141')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
