"""Package the unchanged 0.500 font pair with current usage/coverage documents.

Creates a new local ZIP, preserves earlier packages, validates every entry and
does not include source PDFs, raw reference images, or the separate app build.
"""
import argparse
import hashlib
import json
import re
import urllib.parse
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DOCS=('CURRENT_USAGE.md','FONT_DELIVERY.md','TEXT_SIZING.md','TEXT_EXTRAS.md','NATIVE_GLISSANDO.md')
WEB_ROOT='https://github.com/Freddd13/mcp-musescore/blob/codex/musescore-evolution/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def package_document(path):
    """Keep bundled links local; resolve optional research links to the repo."""
    project=ROOT.parents[1]
    def rewrite(match):
        label,target=match.groups()
        if target.startswith(('http:','https:','#','mailto:')):return match.group(0)
        bare,separator,anchor=target.partition('#');resolved=(path.parent/bare).resolve()
        if resolved.parent==ROOT and resolved.name in DOCS:return match.group(0)
        if resolved.is_file() and project in resolved.parents:
            url=WEB_ROOT+urllib.parse.quote(resolved.relative_to(project).as_posix(),safe='/')
            if separator:url+='#'+anchor
            return '['+label+']('+url+')'
        return match.group(0)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',rewrite,path.read_text(encoding='utf-8')).encode('utf-8')


def run(args):
    assert not args.output.exists(),'Use a new package filename; previous packages are preserved'
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    entries={}
    for family in ('Kumo Score Study','Kumo Score Study Text'):
        for path in sorted((args.fonts/family).iterdir()):
            if path.is_file():entries[family+'/'+path.name]=path.read_bytes()
        assert digest(entries[family+'/'+family+'.otf'])==build['fonts'][family]['sha256']
        entries[family+'/Leland-FONTLOG.txt']=(ROOT/'vendor/leland/FONTLOG.txt').read_bytes()
    for name in DOCS:entries[name]=package_document(ROOT/name)
    entries['README.txt']=entries['CURRENT_USAGE.md']
    entries['FONTLOG_CURRENT.txt']=('Kumo Score Study 0.500 / local study\n\n'
        'Leland music/Text baseline coverage retained. Unprocessed outlines and metrics are unchanged.\n'
        '112 symbol codepoints processed; 19 Text size calibrations retained.\n'
        '0.500 updates Coda and accent-staccato below source curves.\n'
        '2026-10-19 complete-local package updates documents, resource coverage and the local trial-host instructions only.\n'
        'Production OTF and JSON bytes are identical to the earlier 0.500 package.\n'
        'Reference PDF text-object/page-path studies remain local; no original FontFile program is included.\n'
        'Leland license and original FONTLOG accompany each family. See FONT_DELIVERY.md for actual scope.\n').encode('utf-8')
    manifest={name:digest(data) for name,data in sorted(entries.items())}
    entries['SHA256.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in entries.items():archive.writestr(name,data)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist())==set(entries)
        for name,sha in manifest.items():assert digest(archive.read(name))==sha
        # All relative bundled documentation links must resolve in this ZIP.
        for name in DOCS:
            text=archive.read(name).decode('utf-8')
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
                if target.startswith(('http:','https:','#','mailto:')):continue
                assert target.split('#')[0] in entries,(name,target)
    print('Local complete package entries',len(entries),'sha256',digest(args.output.read_bytes()))
    print('Both Study OTF/JSON payloads unchanged; original license/FONTLOG retained; documentation links checked')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fonts',type=Path,default=ROOT/'dist/corpus-font-141')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
