"""Local vector-path atlas font for identifying outlined PDF objects.

Supplementary PUA values are inventory IDs, never production SMuFL mappings.
Even-odd paths are labelled and must be checked against PDF rendering before
production use; the atlas is a diagnostic, not a usable score font.
"""
import argparse,hashlib,json,math
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.paths.read_text(encoding='utf-8'));assert hashlib.sha256(Path(data['source']).read_bytes()).hexdigest()==data['sha256']
    order=['.notdef'];cmap={};strings={};metrics={};items=[]
    p=T2CharStringPen(250,None);strings['.notdef']=p.getCharString();metrics['.notdef']=(250,0)
    for index,item in enumerate(data['paths']):
        glyph='p%05d'%index;cp=0xf0000+index;order.append(glyph);cmap[cp]=glyph
        x0,y0,x1,y1=item['bounds_pt'];unit=250/item['staff_space_pt'];ox=x0;oy=(y0+y1)/2
        rec=RecordingPen();active=False
        for op,points in item['commands']:
            points=[tuple(round(v*65536)/65536 for v in ((x-ox)*unit,(y-oy)*unit)) for x,y in points]
            if op=='moveTo':
                if active:rec.closePath()
                active=True
            getattr(rec,op)(*points)
            if op=='closePath':active=False
        if active:rec.closePath()
        # Filled isolated move-only subpaths have no ink. Type 2 correctly
        # drops them; do not let their points enlarge the expected ink box.
        bound=BoundsPen(None,ignoreSinglePoints=True);rec.replay(bound)
        if bound.bounds is None:raise ValueError('Empty path '+glyph)
        b=bound.bounds;advance=int(math.ceil(b[2]));pen=T2CharStringPen(advance,None,roundTolerance=0);rec.replay(pen)
        # The input includes backtracking spurs on some slur/beam outlines.
        # Keep their segment sequence for a strict geometry round trip rather
        # than letting CFF specialization erase zero-area excursions.
        strings[glyph]=pen.getCharString(optimize=False);metrics[glyph]=(advance,int(math.floor(b[0])))
        items.append(dict(index=index,unicode=cp,glyph=glyph,page=item['page'],object_index=item['object_index'],
            bounds_units=b,bounds_pt=item['bounds_pt'],fill_mode=item['fill_mode'],
            calibration=dict(staff_space_pt=item['staff_space_pt'],origin_pt=[ox,oy]),
            curves=sum(op=='curveTo' for op,pts in item['commands']),contours=sum(op=='moveTo' for op,pts in item['commands'])))
    fb=FontBuilder(1000,isTTF=False);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap)
    fb.setupCFF('KumoPathInventory',dict(FullName='Kumo Path Inventory',FamilyName='Kumo Path Inventory',Weight='Regular'),strings,{})
    fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1000,descent=-1000)
    fb.setupNameTable(dict(familyName='Kumo Path Inventory',styleName='Regular',uniqueFontIdentifier='KumoPathInventory;0.1',fullName='Kumo Path Inventory',psName='KumoPathInventory',version='Version 0.1'))
    fb.setupOS2(sTypoAscender=1000,sTypoDescender=-1000,usWinAscent=30000,usWinDescent=30000)
    fb.setupPost();fb.save(args.output/'path-inventory.otf')
    with TTFont(args.output/'path-inventory.otf') as saved:
        glyphs=saved.getGlyphSet();top=saved['CFF '].cff.topDictIndex[0]
        assert len(saved.getGlyphOrder())==len(items)+1
        for row in items:
            bound=BoundsPen(glyphs,ignoreSinglePoints=True);glyphs[row['glyph']].draw(bound)
            assert all(abs(a-b)<.001 for a,b in zip(bound.bounds,row['bounds_units'])),row['index']
            cs=top.CharStrings[row['glyph']];cs.draw(RecordingPen())
            assert cs.width==saved['hmtx'].metrics[row['glyph']][0],row['index']
    report=dict(source=data['source'],sha256=data['sha256'],path_capture_sha256=hashlib.sha256(args.paths.read_bytes()).hexdigest(),
                cff_bounds_and_widths_verified=True,items=items)
    (args.output/'index.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Local diagnostic font:',len(items),'page paths with original cubic segments; no SMuFL roles assigned.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--paths',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);run(p.parse_args())
