"""Independently isolate every blank whole object from the schema-3 delta.

Page objects are toggled only in memory and restored in finally. No source PDF
is saved and no embedded font program is accessed. Full-page and local renders
are both required, with a visible text-object control on each source page.
"""
import argparse
import collections
import ctypes
import hashlib
import json
import re
from pathlib import Path

import pypdfium2 as pdf
from PIL import Image, ImageDraw, ImageFont
from audit_catalog_empty_occurrences import render_object_bitmap
from audit_hidden_object_visibility import address, raster_extrema

ROOT = Path(__file__).resolve().parent
DELTA_SHA = '97c4d4aa5873e592b208990837b47dfccd8b1678680287d8c5f7c073325aeb0e'


def run(args):
    assert hashlib.sha256(args.delta.read_bytes()).hexdigest() == DELTA_SHA
    data = json.loads(args.delta.read_text(encoding='utf-8'))
    args.output.mkdir(parents=True, exist_ok=False)
    pending = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in data['unrendered_objects']:
        pending[row['score']][row['page']].append(row)
    results, controls = [], []
    for score, pages in pending.items():
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256'] == data['source_hashes'][score]
        doc = pdf.PdfDocument(source)
        for number, rows in pages.items():
            page = doc[number-1]
            text = page.get_textpage()
            objects = list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text))
            w, h = page.get_size()
            assert page.get_rotation() == 0
            assert all(abs(a-b) < .001 for a, b in zip(page.get_bbox(), (0, 0, w, h)))
            top = [pdf.raw.FPDFPage_GetObject(page, i) for i in range(pdf.raw.FPDFPage_CountObjects(page))]
            top_addresses = {address(o) for o in top}
            states = []
            for obj in top:
                value = ctypes.c_int()
                assert pdf.raw.FPDFPageObj_GetIsActive(obj, ctypes.byref(value))
                states.append(bool(value.value))
            try:
                for obj in top:
                    assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                for row in rows:
                    obj = objects[row['text_object_index']]
                    assert obj.level == row['level'] == 0 and address(obj.raw) in top_addresses
                    assert obj.extract() == row['object_text']
                    assert obj.get_font().get_base_name() == row['raw_font']
                    assert all(abs(a-b) < .0001 for a, b in zip(obj.get_bounds(), row['bounds_pt']))
                    assert pdf.raw.FPDFPageObj_SetIsActive(obj, True)
                    try:
                        whole, whole_image = raster_extrema(page, 2)
                        a, b, c, d = obj.get_bounds()
                        left, bottom, right, upper = max(0, a-2), max(0, b-2), min(w, c+2), min(h, d+2)
                        assert left < right and bottom < upper
                        local, local_image = raster_extrema(page, 32, (left, bottom, w-right, h-upper))
                    finally:
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                    record = dict(row, whole_page_2x_luma=whole, local_32x_luma=local,
                                  resolution='isolated-page-no-ink' if whole == local == (255, 255)
                                  else 'visible-in-page-render-review')
                    if record['resolution'] != 'isolated-page-no-ink':
                        prefix = '%s-p%d-o%d' % (score, number, row['text_object_index'])
                        whole_image.save(args.output/(prefix+'-page.png'))
                        local_image.save(args.output/(prefix+'-local.png'))
                    results.append(record)
                for index, obj in enumerate(objects):
                    a, b, c, d = obj.get_bounds()
                    if obj.level or address(obj.raw) not in top_addresses or c <= 0 or a >= w or d <= 0 or b >= h:
                        continue
                    assert pdf.raw.FPDFPageObj_SetIsActive(obj, True)
                    try:
                        extrema, _ = raster_extrema(page, 2)
                    finally:
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                    if extrema[0] < 255:
                        controls.append(dict(score=score, page=number, text_object_index=index,
                                             whole_page_2x_luma=extrema))
                        break
                else:
                    raise AssertionError(('No visible control', score, number))
            finally:
                for obj, state in zip(top, states):
                    assert pdf.raw.FPDFPageObj_SetIsActive(obj, state)
            text.close()
            page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        print(score, 'isolated objects', sum(r['score'] == score for r in results), flush=True)
    key = lambda r: (r['score'], r['page'], r['text_object_index'])
    assert {key(r) for r in results} == {key(r) for r in data['unrendered_objects']}
    assert len(results) == len(data['unrendered_objects']) == 72
    # U+0000 does not reliably set PDFium's map-error flag. Inspect every
    # visible object containing it, not just distinct extracted strings.
    zero_objects = {key(r):r for r in data['rows'] if r['codepoint'] == 0
                    and r['status'] == 'ambiguous-visible-compound-review'}
    zero_results = []
    for (score, number, index), row in sorted(zero_objects.items()):
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['source_hashes'][score]
        doc = pdf.PdfDocument(source)
        page = doc[number-1]
        text = page.get_textpage()
        obj = list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text))[index]
        assert obj.extract() == row['object_text'] and obj.get_font().get_base_name() == row['raw_font']
        image = render_object_bitmap(doc, page, obj, 16)
        assert image is not None and image.convert('L').getextrema()[0] < 255
        filename = 'zero-%s-p%d-o%d.png' % (score, number, index)
        image.save(args.output/filename)
        zero_results.append(dict(row, image=filename, image_sha256=hashlib.sha256(image.tobytes()).hexdigest()))
        text.close();page.close();doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['source_hashes'][score]
    assert len(zero_results) == 17
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    board = Image.new('RGB', (1800, 1080), 'white')
    draw = ImageDraw.Draw(board)
    for i, row in enumerate(zero_results):
        x, y = i%3*600, i//3*180
        draw.text((x+5, y+5), '%s p%d o%d %s' % (row['score'], row['page'], row['text_object_index'], row['font']), font=font, fill='black')
        im = Image.open(args.output/row['image'])
        im.thumbnail((580, 130));board.paste(im, (x+8, y+35))
    board.save(args.output/'zero-objects.png')
    # Old "space-only glyphs" from these two subsets were extraction output,
    # not actual U+0020 source characters. Reopen every object in each family.
    removed = []
    for entry in data['removed']:
        score, family = entry['score'], entry['font']
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['source_hashes'][score]
        doc = pdf.PdfDocument(source)
        object_rows = []
        for number in range(1, len(doc)+1):
            page = doc[number-1];text = page.get_textpage()
            targets = {}
            for index, obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text)):
                if re.sub(r'^[A-Z]{6}\+', '', obj.get_font().get_base_name()) == family:
                    targets[address(obj.raw)] = dict(page=number, text_object_index=index,
                        extracted_text=obj.extract(), source_codes=[], generated_codes=[])
            for i in range(text.count_chars()):
                row = targets.get(address(pdf.raw.FPDFText_GetTextObject(text, i)))
                if row is not None:
                    field = 'generated_codes' if pdf.raw.FPDFText_IsGenerated(text, i) else 'source_codes'
                    row[field].append(pdf.raw.FPDFText_GetUnicode(text, i))
            object_rows.extend(targets.values())
            text.close();page.close()
        doc.close()
        assert all(set(r['source_codes']) == {0} for r in object_rows)
        assert sum(len(r['source_codes']) for r in object_rows) == inv['fonts'][family]['glyphs']['U+0000']['count']
        assert sum(r['extracted_text'].strip() == '' and bool(r['extracted_text']) for r in object_rows) == entry['old']['count']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['source_hashes'][score]
        removed.append(dict(score=score, font=family, objects=object_rows,
                            actual_U0020_source_occurrences=0, actual_source_code=0))
    report = dict(delta_sha256=DELTA_SHA, rows=results, controls=controls,
                  statuses=dict(collections.Counter(r['resolution'] for r in results)),
                  zero_code_visible_objects=zero_results, removed_extraction_keys=removed,
                  source_hashes_unchanged=True, source_pdf_saved=False)
    (args.output/'visibility.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(report['statuses'], 'page controls', len(controls))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--delta', type=Path, default=ROOT/'dist/inventory-delta-review-179/delta.json')
    p.add_argument('--inventory', type=Path, default=ROOT/'dist/corpus-v3-176')
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args())
