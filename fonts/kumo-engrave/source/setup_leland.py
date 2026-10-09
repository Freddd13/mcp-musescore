"""Freeze a licensed local baseline; run once, not as part of normal builds."""
import copy
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(r'E:\programming\funcodes\muse3_dev\MuseScore\fonts\leland')
names=['Leland.otf','LelandText.otf','leland_metadata.json','LICENSE.txt','FONTLOG.txt','README.md']
files={}
for name in names:
    data=(BASE/name).read_bytes()
    dest=ROOT/'vendor/leland'/name
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        assert dest.read_bytes()==data
    else:
        dest.write_bytes(data)
    files['leland/'+name]=hashlib.sha256(data).hexdigest()
manifest=dict(source='Freddd13/MuseScore fonts/leland',source_revision='ba0308e8f2a2ad2b78badfbd28c01e9b10bc869c',version='0.80',files=files)
(ROOT/'LELAND_BASELINE.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
path=ROOT/'source/design.json'
d=json.loads(path.read_text(encoding='utf-8'))
d['version']='0.200';d['release_version']='0.2.0'
d['profiles']['leland-control']=dict(family='Kumo Piano Control',baseline='leland',control=True,counter_scale=1,description='Leland rename-only control.')
heads={
 'noteheadBlack':dict(codepoint='E0A4',outer_box=[0,-136,325,136],outer_shear=.246153846),
 'noteheadHalf':dict(codepoint='E0A3',outer_box=[0,-136,325,136],outer_shear=.246153846,counter=dict(radius_x=140,radius_y=74,shear=.36)),
 'noteheadWhole':dict(codepoint='E0A2',outer_box=[0,-134,373,136],outer_shear=0,counter=dict(radius_x=74,radius_y=99,shear=-.64))}
d['profiles']['piano']=dict(family='Kumo Piano',baseline='leland',palette=True,counter_scale=1,glyph_overrides=heads,description='Leland-based piano palette: independent common heads, clefs, rests, accidentals, arpeggios, flags and dots; Animenz printed references are observational only.')
path.write_bytes((json.dumps(d,indent=2)+'\n').encode())
print('Frozen Leland files; new profiles use Leland, earlier profiles retain Maestro.')
