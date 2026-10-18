"""Compare the same font geometry with/without the native gliss declaration."""
import argparse,collections,json,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageChops


def elements(path,exclude=()):
    root=ET.parse(path).getroot()
    return collections.Counter(ET.tostring(e,encoding='unicode') for e in root
        if e.get('class') not in exclude)


def run(args):
    records={}
    for variant in ('control','study'):
        a=args.before/('gliss-'+variant+'-1.svg');b=args.after/a.name
        # Only the declared wavy gliss run may change; straight gliss is a
        # polyline, so check it separately from the changed wave paths.
        assert elements(a,('GlissandoSegment',))==elements(b,('GlissandoSegment',)),variant
        roots=[ET.parse(p).getroot() for p in (a,b)]
        straight=[collections.Counter(ET.tostring(e,encoding='unicode') for e in r
            if e.get('class')=='GlissandoSegment' and e.tag.endswith('polyline')) for r in roots]
        assert straight[0]==straight[1]
        same=elements(a)==elements(b)
        assert same==(variant=='control')
        images=[Image.open(p.with_name(p.stem+'-white.png')).convert('RGB') for p in (a,b)]
        pixel_same=ImageChops.difference(*images).getbbox() is None
        assert pixel_same==(variant=='control')
        records[variant]=dict(non_gliss_elements_identical=True,straight_identical=True,
            all_svg_elements_identical=same,all_pixels_identical=pixel_same,
            wave_paths=[sum(e.get('class')=='GlissandoSegment' and e.tag.endswith('path') for e in r) for r in roots])
    args.output.write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print('Only opted-in wavy gliss rendering changed; control, straight and trill preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('before','after','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
