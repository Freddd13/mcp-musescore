"""Render all objects of the 269 previously sampled hidden font groups.

Keeps full strings so control-encoded letters/ligatures and musical composites
are not lost by whitespace stripping or Unicode glyph reverse mapping. Every
object has provenance; boards show distinct source font/string orientations,
with exact-image separation when Unicode mapping is ambiguous.
"""
import argparse
import collections
import ctypes
import hashlib
import json
import math
import re
from pathlib import Path
import pypdfium2 as pdf
from PIL import Image, ImageChops, ImageDraw, ImageFont
from source.reviewed_catalog_roles import PENDING_HASH

ROOT = Path(__file__).resolve().parent


def address(raw):
    return ctypes.cast(raw, ctypes.c_void_p).value


def compact_boards(args):
    """Show every representative with less whitespace, grouped by source font."""
    args.output.mkdir(parents=True, exist_ok=False)
    data = json.loads(args.compact_from.read_text(encoding='utf-8'))
    grouped = collections.defaultdict(list)
    for index, row in enumerate(data['representatives']):
        grouped[row['group']].append((index, row))
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)
    board = Image.new('RGB', (1920, 2200), 'white')
    draw = ImageDraw.Draw(board)
    bottoms = [0, 0, 0]
    serial = 1
    placements = []
    for group, values in grouped.items():
        tiles = []
        left, top = 6, 30
        for index, row in values:
            if row['status'] == 'rendered':
                im = Image.open(args.compact_from.parent/row['image']).convert('RGB')
                im.thumbnail((290, 42))
            else:
                im = Image.new('RGB', (48, 24), 'white')
                ImageDraw.Draw(im).text((0, 2), 'NO INK', font=small, fill='red')
            width = max(im.width, 46)+12
            if left+width > 626:
                left, top = 6, top+65
            tiles.append((left, top, im, index))
            left += width
        height = top+70
        assert height < 2200, (group, height)
        column = min(range(3), key=lambda c:bottoms[c])
        if bottoms[column]+height > 2200:
            board.save(args.output/('compact-%02d.png'%serial))
            serial += 1
            board = Image.new('RGB', (1920, 2200), 'white')
            draw = ImageDraw.Draw(board)
            bottoms = [0, 0, 0]
            column = 0
        x, y = column*640, bottoms[column]
        row = values[0][1]
        draw.rectangle((x+1, y+1, x+632, y+height-2), outline='#cccccc')
        draw.text((x+7, y+5), group+' '+row['score']+' '+row['font']+' / '+str(len(values)), font=font, fill='black')
        for dx, dy, im, index in tiles:
            draw.text((x+dx, y+dy), 'R%04d'%index, font=small, fill='#666666')
            board.paste(im, (x+dx, y+dy+16))
        placements.append(dict(group=group, board=serial, indices=[i for i, row in values],
                               cell=[x, y, x+632, y+height]))
        bottoms[column] += height
    board.save(args.output/('compact-%02d.png'%serial))
    result = dict(input_sha256=hashlib.sha256(args.compact_from.read_bytes()).hexdigest(),
                  representatives=len(data['representatives']), groups=len(grouped), boards=serial,
                  placements=placements, note='Identification only; fitted images do not show physical font sizes.')
    (args.output/'layout.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('All representatives', len(data['representatives']), 'groups', len(grouped), 'compact boards', serial)


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    assert hashlib.sha256(args.catalog.read_bytes()).hexdigest() == PENDING_HASH
    pending = json.loads(args.catalog.read_text(encoding='utf-8'))
    by_score = collections.defaultdict(dict)
    for group in pending['groups']:
        by_score[group['score']][group['font']] = group
    rows = []
    representatives = {}
    source_hashes = {}
    for score, families in by_score.items():
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        source_hashes[score] = inv['sha256']
        doc = pdf.PdfDocument(source)
        font_slots = {}
        for number in range(1, len(doc)+1):
            page = doc[number-1]
            text = page.get_textpage()
            objects = {}
            for index, obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text)):
                raw_name = obj.get_font().get_base_name()
                family = re.sub(r'^[A-Z]{6}\+', '', raw_name)
                if family not in families:
                    continue
                pointer = address(pdf.raw.FPDFTextObj_GetFont(obj))
                if pointer not in font_slots:
                    font_slots[pointer] = len(font_slots)+1
                objects[address(obj.raw)] = dict(obj=obj, index=index, family=family,
                                               raw_font=raw_name, slot=font_slots[pointer], chars=[])
            for i in range(text.count_chars()):
                item = objects.get(address(pdf.raw.FPDFText_GetTextObject(text, i)))
                if item is None:
                    continue
                generated = pdf.raw.FPDFText_IsGenerated(text, i)
                error = pdf.raw.FPDFText_HasUnicodeMapError(text, i)
                assert generated in (0, 1) and error in (0, 1)
                item['chars'].append(dict(index=i, codepoint=pdf.raw.FPDFText_GetUnicode(text, i),
                                          generated=bool(generated), unicode_mapping_error=bool(error)))
            for item in objects.values():
                obj = item['obj']
                group = families[item['family']]
                value = obj.extract()
                matrix = obj.get_matrix()
                angle = round(math.degrees(math.atan2(matrix.b, matrix.a)), 2)
                row = dict(group=group['id'], score=score, font=item['family'], raw_font=item['raw_font'],
                           font_slot=item['slot'], page=number, text_object_index=item['index'],
                           object_text=value, bounds_pt=obj.get_bounds(), matrix=matrix.get(),
                           angle_degrees=angle, source_characters=item['chars'])
                raw = pdf.raw.FPDFTextObj_GetRenderedBitmap(doc, page, obj, args.scale)
                ink = None
                if raw:
                    bitmap = pdf.PdfBitmap.from_raw(raw)
                    rgba = bitmap.to_pil().copy().convert('RGBA')
                    bitmap.warn_on_close = False
                    bitmap.close()
                    white = Image.new('RGBA', rgba.size, 'white')
                    white.alpha_composite(rgba)
                    paper = white.convert('RGB')
                    box = ImageChops.difference(paper, Image.new('RGB', paper.size, 'white')).getbbox()
                    if box:
                        ink = paper.crop(box)
                if ink is None:
                    row.update(status='no-visible-object-bitmap', image_sha256=None)
                else:
                    sha = hashlib.sha256(str(ink.size).encode('ascii')+ink.tobytes()).hexdigest()
                    row.update(status='rendered', image_sha256=sha, ink_pixel_size=ink.size)
                ambiguous = not value or any(not c['generated'] and (c['unicode_mapping_error'] or c['codepoint'] == 0)
                                              for c in item['chars'])
                identity = (group['id'], item['slot'], value, angle, row['image_sha256'] if ambiguous else None)
                if identity not in representatives or (ink is not None and representatives[identity]['status'] != 'rendered'):
                    rep = dict(row)
                    if ink is not None:
                        filename = '%s-p%d-o%d.png'%(group['id'], number, item['index'])
                        ink.save(args.output/filename)
                        rep['image'] = filename
                    representatives[identity] = rep
                rows.append(row)
            text.close()
            page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        print(score, 'objects checked', sum(r['score'] == score for r in rows), flush=True)
    actual = collections.Counter(r['group'] for r in rows)
    assert actual == {g['id']: g['objects'] for g in pending['groups']}
    reps = sorted(representatives.values(), key=lambda r:(r['group'], r['font_slot'], r['object_text'], r['page'], r['text_object_index']))
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    for start in range(0, len(reps), 30):
        board = Image.new('RGB', (2000, 1800), 'white')
        draw = ImageDraw.Draw(board)
        for i, rep in enumerate(reps[start:start+30]):
            x, y = i%5*400, i//5*300
            label = '%s %s p%d o%d'%(rep['group'], rep['score'], rep['page'], rep['text_object_index'])
            draw.text((x+6, y+6), label, font=font, fill='black')
            code_label = ' '.join('%04X'%c['codepoint'] for c in rep['source_characters'] if not c['generated'])
            draw.text((x+6, y+29), code_label[:38], font=font, fill='black')
            if rep['status'] == 'rendered':
                im = Image.open(args.output/rep['image'])
                im.thumbnail((380, 210))
                board.paste(im, (x+10, y+65))
            else:
                draw.text((x+8, y+85), 'NO VISIBLE BITMAP / REVIEW', font=font, fill='red')
        board.save(args.output/('objects-%02d.png'%(start//30+1)))
    report = dict(catalog_sha256=PENDING_HASH, source_hashes=source_hashes, source_unchanged=True,
                  objects=rows, representatives=reps, group_counts=dict(actual),
                  source_keys=sorted({(r['group'], r['font_slot'], c['codepoint']) for r in rows
                                      for c in r['source_characters'] if not c['generated']}),
                  object_statuses=dict(collections.Counter(r['status'] for r in rows)),
                  representative_statuses=dict(collections.Counter(r['status'] for r in reps)),
                  all_objects_accounted=True, semantic_roles_certified=False,
                  same_text_other_sizes_individually_certified=False)
    (args.output/'objects.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Groups', len(actual), 'all objects', len(rows), report['object_statuses'],
          'distinct-string/font/orientation representatives', len(reps), 'source keys', len(report['source_keys']))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog', type=Path, default=ROOT/'dist/pending-fonts-01/catalog.json')
    p.add_argument('--inventory', type=Path, default=ROOT/'dist/corpus-v2')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--scale', type=float, default=12)
    p.add_argument('--compact-from', type=Path)
    args = p.parse_args()
    (compact_boards if args.compact_from else run)(args)
