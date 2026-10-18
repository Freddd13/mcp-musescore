"""Read back final local OTF curves for independent PDF assembly verification.

Requires fontTools. Only our generated OTF is read, never a PDF font program.
"""
import argparse,hashlib,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from capture_vector_font import exact_bounds


def run(args):
    assert not args.output.exists()
    data=json.loads(args.capture.read_text(encoding='utf-8'))
    integrated=json.loads(args.integrated.read_text(encoding='utf-8'))
    with TTFont(args.font) as font:
        glyphs=font.getGlyphSet();cmap=font.getBestCmap();rows=[]
        for row in data['rows']:
            if row.get('rejected'):continue
            name=row['choice']['symbol'];pen=RecordingPen();glyphs[cmap[integrated['glyphs'][name]['codepoint']]].draw(pen)
            rows.append(dict(symbol=name,commands=pen.value,bounds=exact_bounds(pen.value),
                             source_selected_bounds_pt=exact_bounds(row['world_commands'])))
    args.output.write_text(json.dumps(dict(font_sha256=hashlib.sha256(args.font.read_bytes()).hexdigest(),
        capture_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest(),rows=rows),separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('capture','integrated','font','output'):p.add_argument('--'+n,type=Path,required=True)
    run(p.parse_args())
