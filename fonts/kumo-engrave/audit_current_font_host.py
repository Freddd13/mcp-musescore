"""Read-only compatibility check for the newly observed installed executable."""
import argparse
import collections
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageChops

ROOT=Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    report=json.loads((args.native/'native-report.json').read_text(encoding='utf-8'))
    gliss=json.loads((args.gliss/'native-report.json').read_text(encoding='utf-8'))
    sizes=json.loads(args.sizes.read_text(encoding='utf-8'))
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    protection=json.loads((args.native/'score-protection.json').read_text(encoding='utf-8'))
    dynamics=json.loads((args.native/'dynamics-pixel-check.json').read_text(encoding='utf-8'))
    assert report['host_sha256']==gliss['host_sha256']==digest(Path(report['host']))
    assert len(report['proofs'])==21 and len(gliss['proofs'])==2
    assert all(p['symbolRegistered'] and p['textRegistered'] for p in report['proofs'].values())
    for family,font in build['fonts'].items():
        for directory in (args.native,args.gliss):
            assert digest(directory/'ScoreFonts'/family/(family+'.otf'))==font['sha256']
            assert (directory/'ScoreFonts'/family/(family+'.json')).read_bytes()==(args.fonts/family/(family+'.json')).read_bytes()
    assert protection['source_unchanged'] and protection['host_unchanged']
    assert all(r['only_font_fields_changed'] and r['all_archive_assets_preserved'] for r in protection['copies'].values())
    assert len(dynamics)==10 and all(r['shape_iou']==1 for r in dynamics)
    assert len(sizes['guards'])==5 and all(r['passed'] for r in sizes['guards'])
    for start in range(0,len(sizes['rows']),3):
        before,after=sizes['rows'][start+1:start+3]
        assert before['role']==after['role']
        assert abs(before['height_sp']-after['height_sp'])<1e-8
        assert abs(before['width_sp']-after['width_sp'])<1e-8
    gliss_checks={};dedicated_gliss=False
    for variant in ('control','study'):
        stem='gliss-'+variant+'-1'
        roots=[ET.parse(p/(stem+'.svg')).getroot() for p in (args.reference_gliss,args.gliss)]
        select=lambda root,cls:collections.Counter(ET.tostring(e,encoding='unicode') for e in root if e.get('class')==cls)
        waves=[select(r,'GlissandoSegment') for r in roots]
        assert waves[0] and waves[1]
        assert select(roots[0],'TrillSegment')==select(roots[1],'TrillSegment')
        non_gliss=[collections.Counter(ET.tostring(e,encoding='unicode') for e in r if e.get('class')!='GlissandoSegment') for r in roots]
        assert non_gliss[0]==non_gliss[1],variant
        reference=args.reference_gliss;mode='dedicated-0.71' if variant=='study' else 'control-unchanged'
        if variant=='study':
            dedicated_gliss=waves[0]==waves[1]
            if not dedicated_gliss:
                # Accept only the documented old-host fallback, with exact
                # legacy reference geometry and pixels, not arbitrary change.
                legacy=ET.parse(args.legacy_gliss/(stem+'.svg')).getroot()
                assert select(legacy,'GlissandoSegment')==waves[1]
                reference=args.legacy_gliss;mode='verified-legacy-trill-fallback'
        else:assert waves[0]==waves[1]
        # The fixture includes both straight/wavy gliss and trill control.
        for directory in (reference,args.gliss):
            path=directory/(stem+'-white.png')
            if not path.exists():
                rgba=Image.open(directory/(stem+'.png')).convert('RGBA')
                white=Image.new('RGBA',rgba.size,'white');white.alpha_composite(rgba)
                white.convert('RGB').save(path)
        images=[Image.open(p/(stem+'-white.png')).convert('RGB') for p in (reference,args.gliss)]
        assert images[0].size==images[1].size
        same=ImageChops.difference(*images).getbbox() is None
        assert same,variant
        gliss_checks[variant]=dict(mode=mode,reference=str(reference),gliss_svg_identical_to_reference=True,
                                  trill_svg_identical=True,whole_page_pixels_identical_to_reference=True)
    supported=json.loads((args.reference_gliss/'native-report.json').read_text(encoding='utf-8'))
    assert digest(Path(supported['host']))==supported['host_sha256']
    result=dict(host=report['host'],host_sha256=report['host_sha256'],native_cases=21,gliss_cases=2,
                all_font_bytes_verified=True,dynamics_cases=10,dynamics_all_iou_one=True,
                size_guards=sizes['guards'],five_actual_sizes_identical_to_verified_host=True,
                gliss_and_trill_checks=gliss_checks,original_score_protection=protection,
                current_host_basic_font_compatibility_verified=True,
                current_host_dedicated_gliss_observed=dedicated_gliss,
                supported_dedicated_gliss_host=supported['host'],supported_host_sha256=supported['host_sha256'])
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Current installed host: 21 full cases + 2 gliss cases, all font bytes verified')
    print('Five actual sizes unchanged; ten dynamics combinations exact; score/attachments protected')
    print('Gliss/trill matches explicit reference; dedicated interface observed:',dedicated_gliss)
    print('Verified 0.71 executable remains available for dedicated glissando')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('native','current-native-full-199'),('gliss','current-native-gliss-201'),
                         ('reference-gliss','native-gliss-133'),('legacy-gliss','native-gliss-104-125'),('fonts','corpus-font-141'),
                         ('sizes','current-size-audit-202/native-text-size-audit.json')]:
        p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
