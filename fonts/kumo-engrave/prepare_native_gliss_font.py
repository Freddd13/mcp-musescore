"""Enable opt-in native glissando rendering without changing captured outlines."""
import argparse,hashlib,json
from pathlib import Path


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'))
    assert 'native_engraving' not in data
    assert data['glyphs']['wiggleGlissando'].get('commands')
    data.update(version='0.490',native_engraving=dict(wavyGlissandoGlyph='wiggleGlissando'),
        native_engraving_parent_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest())
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Native glissando declaration enabled; all captured geometry and Text calibration retained')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('capture','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
