"""Measure native SVG ink against staff space and make equal-scale comparisons.

Requires fontTools and Pillow. Reads authored/native copies only. Labels identify
the renamed Leland baseline, the previous Study and the corrected Study. Crop
windows share fixed staff-space extents; glyphs are never independently resized.
"""
import argparse,json,statistics,xml.etree.ElementTree as ET
from pathlib import Path
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageDraw

NS='{http://www.w3.org/2000/svg}'


def measure(directory,variant,page=2,fixture='user',roles=('Dynamic','OttavaSegment')):
    stem=fixture+'-'+variant+'-'+str(page)
    root=ET.parse(directory/(stem+'.svg')).getroot();w,h=map(float,root.get('viewBox').split()[2:])
    spaces=[];paths={}
    for e in root.iter():
        role=e.get('class')
        if role=='StaffLines' and e.tag==NS+'polyline':
            pts=[tuple(map(float,p.split(','))) for p in e.get('points').split()]
            levels=sorted(set(round(y,3) for x,y in pts))
            spaces.extend(b-a for a,b in zip(levels,levels[1:]) if b-a>.1)
        if e.tag==NS+'path' and role in roles:
            assert not e.get('transform'),'Handle SVG transforms explicitly before measuring'
            p=BoundsPen(None);parse_path(e.get('d'),p)
            if p.bounds:paths.setdefault(role,[]).append(p.bounds)
    # MuseScore emits each of the five staff lines as a separate polyline.
    if not spaces:
        ys=sorted({float(e.get('points').split()[0].split(',')[1]) for e in root.iter(NS+'polyline') if e.get('class')=='StaffLines'})
        gaps=[b-a for a,b in zip(ys,ys[1:]) if b-a>1]
        assert gaps;small=min(gaps);spaces=[v for v in gaps if abs(v-small)<.1]
    sp=statistics.median(spaces);image=Image.open(directory/(stem+'-white.png')).convert('RGB')
    assert abs(image.width/w-image.height/h)<.001
    return dict(space_svg=sp,paths=paths,image=image,svg_width=w,svg_height=h)


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    inputs=[('Leland Text baseline',args.before,'control'),(args.before_label,args.before,'study'),(args.after_label,args.after,'study')]
    records=[]
    guards=[]
    for role,title,index,fixture,page in [('Dynamic','mf',0,'user',2),('OttavaSegment','8',0,'user',2),
            ('OttavaSegment','8va',0,'integration',1),('PedalSegment','Ped',0,'palette',1),('PedalSegment','pedal-star',1,'palette',1)]:
        crops=[]
        for label,directory,variant in inputs:
            r=measure(directory,variant,page,fixture,(role,))
            box=r['paths'][role][index];sp=r['space_svg'];cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
            # Enough context above and below to see the mark beside real notes.
            crop=(cx-8*sp,cy-5*sp,cx+13*sp,cy+6*sp);ratio=r['image'].width/r['svg_width']
            crop=tuple(round(v*ratio) for v in crop);im=r['image'].crop(crop)
            crops.append((label,im));records.append(dict(label=label,role=title,width_sp=(box[2]-box[0])/sp,height_sp=(box[3]-box[1])/sp,space_svg=sp,bounds_svg=box))
        assert max(im.width for label,im in crops)-min(im.width for label,im in crops)<=1,'Different physical scales'
        cell_h=max(im.height for label,im in crops)+26;board=Image.new('RGB',(max(im.width for label,im in crops),cell_h*len(crops)),'white')
        draw=ImageDraw.Draw(board)
        for i,(label,im) in enumerate(crops):
            draw.text((8,i*cell_h+5),label+' / '+title,fill='black');board.paste(im,(0,i*cell_h+24))
        board.save(args.output/(title+'-native-comparison.png'))
        ratio=records[-1]['height_sp']/records[-3]['height_sp']
        guards.append(dict(role=title,corrected_to_baseline_height_ratio=ratio,passed=.9<=ratio<=1.1))
    (args.output/'native-text-size-audit.json').write_text(json.dumps(dict(rows=records,guards=guards),indent=2)+'\n',encoding='utf-8')
    for row in records:print(row['label'],row['role'],'height_sp',round(row['height_sp'],4),'width_sp',round(row['width_sp'],4))
    assert all(r['passed'] for r in guards),'Review actual-context size change; do not blindly update the tolerance'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('before','after','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--before-label',default='Study 0.470');p.add_argument('--after-label',default='Study 0.480 corrected')
    run(p.parse_args())
