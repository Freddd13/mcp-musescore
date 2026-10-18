"""Ensure a metadata-only font release preserves every outline and metric."""
import argparse,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen


def run(args):
    report={}
    for family in ('Kumo Score Control','Kumo Score Control Text','Kumo Score Study','Kumo Score Study Text'):
        fonts=[TTFont(p/family/(family+'.otf')) for p in (args.before,args.after)]
        a,b=fonts;assert a.getGlyphOrder()==b.getGlyphOrder()
        assert a.getBestCmap()==b.getBestCmap()
        assert a['hmtx'].metrics==b['hmtx'].metrics
        for tag in ('head','hhea','OS/2','GSUB','GPOS','GDEF'):
            assert (tag in a)==(tag in b)
            if tag in a:
                if tag=='head':
                    # Font version/checksum/date describe the release, not its geometry.
                    for key in ('unitsPerEm','xMin','yMin','xMax','yMax'):assert getattr(a[tag],key)==getattr(b[tag],key)
                else:assert a[tag].compile(a)==b[tag].compile(b),tag
        sets=[f.getGlyphSet() for f in fonts]
        for name in a.getGlyphOrder():
            pens=[RecordingPen(),RecordingPen()]
            for glyphs,pen in zip(sets,pens):glyphs[name].draw(pen)
            assert pens[0].value==pens[1].value,(family,name)
        report[family]=dict(glyphs=len(a.getGlyphOrder()),all_outlines_metrics_cmap_layout_identical=True)
        for font in fonts:font.close()
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Every Music/Text outline, advance, vertical metric and layout table preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('before','after','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
