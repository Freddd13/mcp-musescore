"""Fit Leland's arrowheads to the observed wave body; retain cubic segments.

This is an explicit baseline adaptation, not a claim of recovered source-score
arrow geometry. The ordinary wave comes from the source run. Only the arrowhead
and its proportions come from the OFL baseline.
"""
import argparse,copy,hashlib,json,math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from source.contours import sample_contours,filled_intervals,area

ROOT=Path(__file__).resolve().parent


def polygon_commands(loops):
    result=[]
    for points in loops:
        result.append(('moveTo',[points[0]]))
        result.extend(('lineTo',[p]) for p in points[1:]);result.append(('closePath',[]))
    return result


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);data=json.loads(args.capture.read_text(encoding='utf-8'))
    baseline=ROOT/'vendor/leland/Leland.otf';font=TTFont(baseline);rec=RecordingPen()
    font.getGlyphSet()['wiggleArpeggiatoUpArrow'].draw(rec)
    # Retain Leland's wings and tip verbatim. Replace its wavy root with the
    # observed period, so the repeated run does not end in a different wave.
    assert rec.value[4]==('lineTo',((72,135),)) and rec.value[15]==('lineTo',((8,-44),))
    head=RecordingPen();head.value=rec.value[:5]+[('lineTo',((72,41),))]+rec.value[15:]
    source=copy.deepcopy(data['glyphs']['wiggleArpeggiatoUp']);loops=source['outlines']
    oldmeta=json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))
    old=oldmeta['glyphBBoxes']['wiggleArpeggiatoUp'];scale=(source['bounds'][3]-source['bounds'][1])/((old['bBoxNE'][1]-old['bBoxSW'][1])*250)
    at=source['advance'];spans=filled_intervals(loops,at);low,high=spans[0][0],spans[-1][1]
    dx=at-72*scale;dy=(low+high)/2-88*scale
    adapted=[(op,[[round(x*scale+dx,6),round(y*scale+dy,6)] for x,y in points]) for op,points in head.value]
    hp=RecordingPen()
    for op,points in adapted:getattr(hp,op)(*[tuple(p) for p in points])
    head_loops=sample_contours(hp,steps=64)
    # Same fill orientation in overlapping closed contours avoids cancellation.
    if area(head_loops[0])*area(loops[0])<0:
        # Reverse curves without flattening them.
        from fontTools.pens.reverseContourPen import ReverseContourPen
        reverse=RecordingPen();hp.replay(ReverseContourPen(reverse));hp=reverse
        adapted=[(op,[list(p) for p in points]) for op,points in hp.value];head_loops=sample_contours(hp,steps=64)
    commands=copy.deepcopy(source.get('commands') or polygon_commands(loops))+adapted
    bounds=BoundsPen(None)
    for op,points in commands:getattr(bounds,op)(*[tuple(p) for p in points])
    box=list(bounds.bounds);advance=int(math.ceil(box[2]))
    sm=json.loads(args.glyphnames.read_text(encoding='utf-8'))
    for name,mirror in [('wiggleArpeggiatoUpArrow',False),('wiggleArpeggiatoDownArrow',True)]:
        b=copy.deepcopy(box);ll=copy.deepcopy(loops+head_loops);cc=copy.deepcopy(commands)
        if mirror:
            origin=box[0]+box[2]
            ll=[[[origin-x,y] for x,y in v] for v in ll]
            cc=[(op,[[origin-x,y] for x,y in pts]) for op,pts in cc]
        data['glyphs'][name]=dict(codepoint=int(sm[name]['codepoint'][2:],16),outlines=ll,commands=cc,
            bounds=b,advance=advance,repeat=None,mode='baseline-arrow-adaptation',smufl=True,
            source_key='Leland arrowhead + observed wave interior',
            notes=['OFL baseline wings/tip retain cubic geometry; wave period and root match source union; not recovered source arrow'])
    data['arrow_adaptation']=dict(baseline_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
        uniform_head_scale=scale,root=[at,(low+high)/2],source='Leland arrowhead, source-reference wave body')
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Adapted two arrow ends, total',len(data['glyphs']),'head scale',scale,'advance',advance)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'));run(p.parse_args())
