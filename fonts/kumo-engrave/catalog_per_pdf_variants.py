"""Render per-PDF keys and group same-code shape variants for human review.

Source PDF text objects only, no FontFile programs. Geometric groups and
baseline similarity are discovery aids, never automatic semantic certification.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image, ImageDraw, ImageFont
from audit_corpus_shapes import fingerprint
from catalog_pdf_glyphs import render_character

ROOT = Path(__file__).resolve().parent


def similarity(a, aspect_a, b, aspect_b):
    return float(np.logical_and(a, b).sum()/max(np.logical_or(a, b).sum(), 1))*min(aspect_a/aspect_b, aspect_b/aspect_a)**.4


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    baseline = json.loads(args.baseline.read_text(encoding='utf-8'))
    base_shapes = {}
    for key, row in baseline.items():
        if row['status'] == 'rendered':
            base_shapes[row['unicode']] = fingerprint(Image.open(args.baseline.parent/row['image']).convert('RGBA'))
    rows = []
    source_hashes = {}
    shapes = {}
    for score in args.scores:
        data = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(data['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
        source_hashes[score] = data['sha256']
        doc = pdf.PdfDocument(source)
        pages = {}
        for cp, glyph in sorted(data['fonts'][args.family]['glyphs'].items()):
            row = dict(score=score, font=args.family, unicode=cp, occurrences=glyph['count'], errors=[])
            for sample in sorted(glyph['samples'], key=lambda s:(not s.get('single', True), -s['size_pt'])):
                number = sample['page']
                if number not in pages:
                    page = doc[number-1]
                    text = page.get_textpage()
                    pages[number] = page, text, list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text))
                page, text, objects = pages[number]
                obj = objects[sample['text_object_index']]
                try:
                    im, box, origin = render_character(doc, page, text, obj, glyph['char'], args.scale)
                    mask, aspect = fingerprint(im)
                    filename = score+'-'+cp[2:]+'.png'
                    im.save(args.output/filename)
                    row.update(status='rendered', image=filename, sample=sample, bounds_pt=box, origin_pt=origin)
                    shapes[filename] = mask, aspect
                    if cp in base_shapes:
                        bm, ba = base_shapes[cp]
                        row['selected_baseline_similarity'] = similarity(mask, aspect, bm, ba)
                    break
                except (ValueError, RuntimeError) as error:
                    row['errors'].append(str(error))
            else:
                row['status'] = 'unrendered'
            rows.append(row)
        for page, text, objects in pages.values():
            text.close()
            page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
        print(score, 'per-PDF keys', len(data['fonts'][args.family]['glyphs']), flush=True)
    groups = []
    for row in rows:
        if row['status'] != 'rendered':
            continue
        mask, aspect = shapes[row['image']]
        choices = []
        for group in groups:
            if group['unicode'] != row['unicode']:
                continue
            other, oa = shapes[group['representative']['image']]
            choices.append((similarity(mask, aspect, other, oa), group))
        match = max(choices, key=lambda item:item[0]) if choices else None
        if match and match[0] >= args.minimum:
            group = match[1]
            group['minimum_similarity'] = min(group['minimum_similarity'], match[0])
        else:
            group = dict(id='V%03d'%(len(groups)+1), unicode=row['unicode'], representative=row, members=[], minimum_similarity=1)
            groups.append(group)
        group['members'].append(row)
    groups.sort(key=lambda g:(g['unicode'], g['id']))
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    for start in range(0, len(groups), 24):
        board = Image.new('RGB', (1800, 1520), 'white')
        draw = ImageDraw.Draw(board)
        for i, group in enumerate(groups[start:start+24]):
            x, y = i%6*300, i//6*380
            row = group['representative']
            draw.text((x+6, y+6), group['id']+' '+group['unicode']+' n'+str(len(group['members'])), font=font, fill='black')
            draw.text((x+6, y+28), row['score']+' p%d obj%d'%(row['sample']['page'], row['sample']['text_object_index']), font=font, fill='black')
            draw.text((x+6, y+50), 'baseline %.3f'%row.get('selected_baseline_similarity', -1), font=font, fill='black')
            im = Image.open(args.output/row['image']).convert('RGBA')
            paper = Image.new('RGBA', im.size, 'white')
            paper.alpha_composite(im)
            im = paper.convert('RGB')
            im.thumbnail((260, 260))
            board.paste(im, (x+(300-im.width)//2, y+85))
        board.save(args.output/('variants-%02d.png'%(start//24+1)))
    report = dict(source_hashes=source_hashes, source_unchanged=True, family=args.family,
                  baseline_sha256=hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
                  minimum_group_similarity=args.minimum, rows=rows, groups=groups,
                  category_counts=dict(collections.Counter(r['status'] for r in rows)),
                  semantic_roles_certified=False)
    (args.output/'variants.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Per-PDF keys', len(rows), report['category_counts'], 'same-code geometric groups', len(groups))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory', type=Path, default=ROOT/'dist/corpus-v2')
    p.add_argument('--baseline', type=Path, default=ROOT/'dist/chaconne-catalog-v2/catalog.json')
    p.add_argument('--family', default='Chaconne')
    p.add_argument('--scores', nargs='+', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--scale', type=float, default=16)
    p.add_argument('--minimum', type=float, default=.9)
    run(p.parse_args())
