"""Attach explicit Text-route calibration without altering source geometry."""
import argparse,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'));spec=json.loads(args.spec.read_text(encoding='utf-8'))
    assert 'text_calibration' not in data,'Preserve previous calibration; use a separately reviewed migration'
    assert spec['schema']==1
    data.update(version=spec['version'],text_calibration=dict(spec,spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest()))
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Text calibration attached; all captured music geometry preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture',type=Path,required=True);p.add_argument('--spec',type=Path,default=ROOT/'source/text_calibration.json')
    p.add_argument('--output',type=Path,required=True);run(p.parse_args())
