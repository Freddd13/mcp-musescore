"""Package a verified local Study build; never add reference assets to Git."""
import argparse,hashlib,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def run(args):
    assert not args.output.exists(),'Preserve previous local packages'
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    files={}
    for family in ('Kumo Score Study','Kumo Score Study Text'):
        info=build['fonts'][family];font=args.fonts/family/(family+'.otf')
        assert hashlib.sha256(font.read_bytes()).hexdigest()==info['sha256']
        assert info['coverage_preserved'] and info['unchanged_outlines_and_metrics_preserved']
        for path in (args.fonts/family).iterdir():
            assert path.is_file();files[family+'/'+path.name]=path.read_bytes()
    files['TEXT_EXTRAS.md']=(ROOT/'TEXT_EXTRAS.md').read_bytes()
    sized=any(v.get('text_scale',1)!=1 for v in build['fonts']['Kumo Score Study Text']['changed'].values())
    if sized:
        files['TEXT_SIZING.md']=(ROOT/'TEXT_SIZING.md').read_bytes()
        if (ROOT/'COVERAGE_RECONCILIATION.md').exists():files['COVERAGE_RECONCILIATION.md']=(ROOT/'COVERAGE_RECONCILIATION.md').read_bytes()
    files['README.txt']=('Kumo Score Study — 本机官谱字形研究小样\n\n'
        '将 Kumo Score Study 和 Kumo Score Study Text 两个完整文件夹复制到 Evolution 偏好设置的 Score Fonts 路径，重启。\n'
        '在乐谱独立副本的 格式→样式→乐谱 中同时选择上述音乐字体与 Text 字体。第一轮保持其余样式。\n'
        '已有旧小样时成对更换两个家族的 OTF/JSON 后重启，不需重装 MCP、skill 或 Windows 字体。\n'
        '额外的 swing / ≒ 入口见 TEXT_EXTRAS.md；普通8va、sf、音符括号仍用软件原有操作。\n'
        '未修改字形保持 Leland。实际原生验证宿主和范围见项目 CORPUS_STUDY.md。\n'
        '这是本机研究构建，不是 Chaconne 字体文件；来源轮廓与公开 OFL 底库分别记录。\n').encode('utf-8')
    manifest={name:hashlib.sha256(data).hexdigest() for name,data in files.items()}
    files['SHA256.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with zipfile.ZipFile(args.output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in files.items():archive.writestr(name,data)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        for name,sha in manifest.items():assert hashlib.sha256(archive.read(name)).hexdigest()==sha
    print('Local package verified',args.output,len(files),'files')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fonts',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);run(p.parse_args())
