"""Build a LOCAL seven-glyph proof from captured raster contours.

Not part of build.py profiles or its ZIP allowlist. It is not a public font
release. Requires fontTools; preserves source data provenance in the folder.
"""
import argparse,json,math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import RecordingPen
from build import ROOT,rename,bounds
from source.contours import vertical_edges,inside,area


def run(args):
    data=json.loads(args.capture.read_text(encoding='utf-8'))
    if args.output.exists():raise ValueError('Use a new proof font directory')
    args.output.mkdir(parents=True)
    name='Kumo PDF Study';font=TTFont(ROOT/'vendor/leland/Leland.otf',recalcTimestamp=False)
    rename(font,name,'0.401',' Local raster study from user-provided PDF. Not the Chaconne font file.')
    font['name'].setName('Leland baseline portions retain OFL. User-reference shapes are included only in a local unpublished study; no redistribution license is granted for them.',13,3,1,0x409)
    meta=json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))
    top=font['CFF '].cff.topDictIndex[0];cmap=font.getBestCmap();report={}
    for symbol,item in data['glyphs'].items():
        glyph=cmap[item['codepoint']];loops=item['outlines']
        xs=[p[0] for v in loops for p in v];ys=[p[1] for v in loops for p in v]
        box=[min(xs),min(ys),max(xs),max(ys)];advance=int(math.ceil(box[2]))
        font['hmtx'].metrics[glyph]=(advance,int(math.floor(box[0])))
        # Raster contours need fractional coordinates; integer rounding makes
        # enlarged letters visibly rough even at high capture resolution.
        pen=T2CharStringPen(advance-getattr(top.Private,'nominalWidthX',0),font.getGlyphSet(),roundTolerance=0)
        # Quantize absolute points to Type 2's 16.16 grid first. Otherwise
        # rounding thousands of relative deltas accumulates a small drift.
        def point(p):return tuple(round(v*65536)/65536 for v in p)
        for points in loops:
            pen.moveTo(point(points[0]))
            for vertex in points[1:]:pen.lineTo(point(vertex))
            pen.closePath()
        top.CharStrings[glyph]=pen.getCharString(private=top.Private,globalSubrs=top.GlobalSubrs)
        meta['glyphBBoxes'][symbol]={'bBoxSW':[box[0]/250,box[1]/250],'bBoxNE':[box[2]/250,box[3]/250]}
        anchors=meta['glyphsWithAnchors'].setdefault(symbol,{})
        if symbol in ('noteheadBlack','noteheadHalf'):
            for key,x,side,inset in [('stemDownNW',box[0]+2,box[0],12),('stemUpSE',box[2]-2,box[2],-12)]:
                lo,hi=vertical_edges(loops[0],x);y=(lo+hi)/2+inset
                assert inside(loops[0],(x,y))
                assert len(loops)==1 or not inside(loops[1],(x,y))
                anchors[key]=[side/250,y/250]
        if symbol.startswith('notehead'):
            for key,q,upper in [('cutOutNW',.17,True),('cutOutNE',.83,True),('cutOutSW',.17,False),('cutOutSE',.83,False)]:
                x=box[0]+q*(box[2]-box[0]);lo,hi=vertical_edges(loops[0],x)
                anchors[key]=[x/250,((hi+1) if upper else (lo-1))/250]
            if len(loops)>1:
                assert area(loops[0])*area(loops[1])<0
                assert all(inside(loops[0],p) for p in loops[1])
        report[symbol]=dict(advance=advance,bounds_sp=[v/250 for v in box],anchors=anchors)
    meta.update(fontName=name,fontVersion=.401)
    font.save(args.output/(name+'.otf'))
    (args.output/(name+'.json')).write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    (args.output/'metrics.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    # Coverage, widths, actual boxes and the change boundary are checked after
    # saving the real font, independently of the in-memory builder state.
    with TTFont(ROOT/'vendor/leland/Leland.otf') as base, TTFont(args.output/(name+'.otf')) as result:
        assert base.getBestCmap()==result.getBestCmap() and base.getGlyphOrder()==result.getGlyphOrder()
        allowed={cmap[v['codepoint']] for v in data['glyphs'].values()}
        for glyph in base.getGlyphOrder():
            a,b=RecordingPen(),RecordingPen();base.getGlyphSet()[glyph].draw(a);result.getGlyphSet()[glyph].draw(b)
            assert (a.value!=b.value)==(glyph in allowed)
            char=result['CFF '].cff.topDictIndex[0].CharStrings[glyph];char.draw(RecordingPen())
            assert char.width==result['hmtx'].metrics[glyph][0]
        for symbol,item in data['glyphs'].items():
            actual=bounds(result.getGlyphSet(),cmap[item['codepoint']])
            assert all(abs(a/250-b)<1e-5 for a,b in zip(actual,report[symbol]['bounds_sp']))
    print('Local proof: seven glyphs, coverage, CFF widths, holes and head connections checked.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
