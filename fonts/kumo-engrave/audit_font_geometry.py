"""Verify exact declared Study changes and preserve every unlisted outline/metric."""
import argparse,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen


def run(args):
    report={}
    build=json.loads((args.after/'build-report.json').read_text(encoding='utf-8'))
    for family in ('Kumo Score Control','Kumo Score Control Text','Kumo Score Study','Kumo Score Study Text'):
        fonts=[TTFont(p/family/(family+'.otf')) for p in (args.before,args.after)]
        a,b=fonts;assert a.getGlyphOrder()==b.getGlyphOrder()
        assert a.getBestCmap()==b.getBestCmap()
        allowed={build['fonts'][family]['changed'][name]['glyph'] for name in args.changed_symbols} if family.startswith('Kumo Score Study') else set()
        metric_changes={name for name in a.getGlyphOrder() if a['hmtx'].metrics[name]!=b['hmtx'].metrics[name]}
        assert metric_changes<=allowed,(family,metric_changes)
        for tag in ('head','hhea','OS/2','GSUB','GPOS','GDEF'):
            assert (tag in a)==(tag in b)
            if tag in a:
                if tag=='head':
                    # Font version/checksum/date describe the release, not its geometry.
                    for key in ('unitsPerEm','xMin','yMin','xMax','yMax'):assert getattr(a[tag],key)==getattr(b[tag],key)
                else:assert a[tag].compile(a)==b[tag].compile(b),tag
        sets=[f.getGlyphSet() for f in fonts]
        outline_changes=set()
        for name in a.getGlyphOrder():
            pens=[RecordingPen(),RecordingPen()]
            for glyphs,pen in zip(sets,pens):glyphs[name].draw(pen)
            if pens[0].value!=pens[1].value:outline_changes.add(name)
        assert outline_changes==allowed,(family,outline_changes,allowed)
        report[family]=dict(glyphs=len(a.getGlyphOrder()),all_unlisted_outlines_metrics_preserved=True,
            cmap_vertical_metrics_layout_identical=True,changed_outlines=sorted(outline_changes),changed_metrics=sorted(metric_changes))
        for font in fonts:font.close()
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Only declared outlines/metrics changed; all other geometry, cmap, vertical metrics and layout preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('before','after','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--changed-symbols',nargs='*',default=[],help='Exact expected Study outline changes; Control must remain identical')
    run(p.parse_args())
