"""Prepare reproducible alternate instances for the remaining raster shapes."""
import argparse,hashlib,json
from pathlib import Path
from source.reviewed_catalog_roles import CATALOG_HASHES

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    choices=json.loads(args.choices.read_text(encoding='utf-8'))
    path=args.study/choices['catalog']/'catalog.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==CATALOG_HASHES[choices['catalog']]
    catalog=json.loads(path.read_text(encoding='utf-8'));selected={};glyphs=[]
    for row in choices['choices']:
        name=row['symbol'];selected[name]=catalog[row['key']]
        glyphs.append(dict(group=name,symbol=name,mode=row['mode'],replace=True,
            calibration='nominal',reject_retains_previous=True))
    for name,data in [('catalog',selected),('spec',dict(version=choices['version'],glyphs=glyphs,derived=[]))]:
        (args.output/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Alternate source instances prepared; comparison is required before integration')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--choices',type=Path,default=ROOT/'source/alternate_curve_choices.json')
    p.add_argument('--study',type=Path,default=ROOT/'dist');p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
