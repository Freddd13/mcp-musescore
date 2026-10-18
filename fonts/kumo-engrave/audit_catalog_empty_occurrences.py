"""Read-only all-occurrence review of three unrendered music catalogue keys.

Reads actual text objects/character boxes and rendered object bitmaps. Glyph
path API results are diagnostic only: Unicode reverse mapping can be ambiguous.
No FontFile program or modified source PDF is read/saved.
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
from PIL import Image, ImageOps

TARGETS = {'Chaconne': {3, 32}, 'CIDFont+F1': {0xf020}}
ROOT = Path(__file__).resolve().parent


def address(raw):
    return ctypes.cast(raw, ctypes.c_void_p).value


def render_object_bitmap(doc, page, obj, scale):
    raw = pdf.raw.FPDFTextObj_GetRenderedBitmap(doc, page, obj, scale)
    if not raw:
        return None
    bitmap = pdf.PdfBitmap.from_raw(raw)
    rgba = bitmap.to_pil().copy().convert('RGBA')
    bitmap.warn_on_close = False
    bitmap.close()
    white = Image.new('RGBA', rgba.size, 'white')
    white.alpha_composite(rgba)
    return white.convert('RGB')


def inspect_crop(image, box, bounds, scale, generated=False):
    a, b, c, d = bounds
    crop = [math.floor((box[0]-a)*scale), math.floor((d-box[3])*scale),
            math.ceil((box[2]-a)*scale), math.ceil((d-box[1])*scale)]
    inside = image is not None and crop[0] >= -2 and crop[1] >= -2 and crop[2] <= image.width+2 and crop[3] <= image.height+2
    clip = None
    if generated:
        status, pixels, low = 'generated-spacing-not-font-glyph', 0, None
    elif image is None:
        status, pixels, low = 'whole-object-no-bitmap', 0, None
    elif box[2] <= box[0] or box[3] <= box[1]:
        status, pixels, low = 'zero-area-character-box', 0, None
    else:
        # Padding is white: a nominal blank glyph box may extend outside the
        # text object's ink bitmap. Never turn that extension into black pixels.
        clip = Image.new('RGB', (crop[2]-crop[0], crop[3]-crop[1]), 'white')
        clip.paste(image, (-crop[0], -crop[1]))
        grey = ImageOps.grayscale(clip)
        low = grey.getextrema()[0]
        pixels = sum(grey.histogram()[:255])
        status = 'character-box-no-ink' if pixels == 0 else 'character-box-ink-review'
    return dict(status=status, dark_pixels=pixels, minimum_luma=low,
                crop_px=crop, charbox_inside_rendered_object=inside), clip


def verify_controls(args):
    """The same extraction must retain visible neighbours in real PDF objects."""
    args.output.mkdir(parents=True, exist_ok=False)
    rows = []
    for score, number, index, family, cp in [('A003', 1, 41, 'CIDFont+F1', 0xf071),
                                            ('A020', 3, 727, 'Chaconne', 40),
                                            ('A021', 2, 0, 'Chaconne', 38)]:
        data = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(data['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
        doc = pdf.PdfDocument(source)
        page = doc[number-1]
        text = page.get_textpage()
        obj = list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text))[index]
        assert re.sub(r'^[A-Z]{6}\+', '', obj.get_font().get_base_name()) == family
        match = [i for i in range(text.count_chars()) if pdf.raw.FPDFText_GetUnicode(text, i) == cp
                 and address(pdf.raw.FPDFText_GetTextObject(text, i)) == address(obj.raw)]
        assert match and not pdf.raw.FPDFText_IsGenerated(text, match[0])
        image = render_object_bitmap(doc, page, obj, args.scale)
        measurement, clip = inspect_crop(image, text.get_charbox(match[0]), obj.get_bounds(), args.scale)
        assert measurement['dark_pixels'] > 0, (score, cp, measurement)
        filename = score+'-visible-control.png'
        clip.save(args.output/filename)
        rows.append(dict(score=score, page=number, text_object_index=index, codepoint=cp,
                         font=family, image=filename, sha256=data['sha256'], **measurement))
        text.close()
        page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
    # A null text bitmap is not by itself evidence of an empty character. For
    # the two such objects render the original page with only that object active.
    data = json.loads((args.inventory/'A130.json').read_text(encoding='utf-8'))
    source = Path(data['source_path'])
    assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
    doc = pdf.PdfDocument(source)
    page = doc[2]
    text = page.get_textpage()
    objects = list(page.get_objects())
    text_objects = list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text))
    states = []
    for obj in objects:
        active = ctypes.c_int()
        assert pdf.raw.FPDFPageObj_GetIsActive(obj, ctypes.byref(active))
        states.append(bool(active.value))
        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
    isolated = []
    for index in (649, 651):
        obj = text_objects[index]
        assert obj.level == 0 and obj.extract() == ' '
        assert pdf.raw.FPDFPageObj_SetIsActive(obj, True)
        a, b, c, d = obj.get_bounds()
        w, h = page.get_size()
        renders = []
        for scale in (32, 64):
            bitmap = page.render(scale=scale, crop=(a-1, b-1, w-c-1, h-d-1))
            im = bitmap.to_pil().copy().convert('RGB')
            bitmap.close()
            extrema = ImageOps.grayscale(im).getextrema()
            assert extrema == (255, 255), (index, scale, extrema)
            renders.append(dict(scale=scale, luma=extrema))
        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
        isolated.append(dict(score='A130', page=3, text_object_index=index,
                             object_text=' ', source_sha256=data['sha256'], renders=renders))
    for obj, active in zip(objects, states):
        assert pdf.raw.FPDFPageObj_SetIsActive(obj, active)
    text.close()
    page.close()
    doc.close()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
    (args.output/'controls.json').write_text(json.dumps(dict(rows=rows, isolated_null_bitmap_objects=isolated,
        source_unchanged=True), indent=2)+'\n', encoding='utf-8')
    print('Three visible original-object controls retained ink with the same bitmap/crop function')
    print('Two null-bitmap objects isolated on the original page: white at 32x and 64x; source unchanged')


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    files = []
    for f in sorted(args.inventory.glob('A*.json')):
        data = json.loads(f.read_text(encoding='utf-8'))
        # Inventory intentionally omitted whitespace inside text runs. Therefore
        # visit every PDF using either family, even when it has no indexed key.
        if any(name in data.get('fonts', {}) for name in TARGETS):
            files.append(data)
    rows = []
    source_hashes = {}
    expected = collections.Counter()
    for data in files:
        source = Path(data['source_path'])
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        assert before == data['sha256']
        source_hashes[data['id']] = before
        for family, codes in TARGETS.items():
            for cp in codes:
                item = data.get('fonts', {}).get(family, {}).get('glyphs', {}).get('U+%04X'%cp)
                if item:
                    expected[(data['id'], family, cp)] = item['count']
        doc = pdf.PdfDocument(source)
        for number in range(1, len(doc)+1):
            page = doc[number-1]
            text = page.get_textpage()
            owners = {}
            for index, obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT], textpage=text)):
                raw_name = obj.get_font().get_base_name()
                family = re.sub(r'^[A-Z]{6}\+', '', raw_name)
                if family not in TARGETS:
                    continue
                value = obj.extract()
                if not any(ord(c) in TARGETS[family] for c in value):
                    continue
                owners[address(obj.raw)] = (index, obj, family, raw_name, value)
            bitmaps = {}
            for i in range(text.count_chars()):
                cp = pdf.raw.FPDFText_GetUnicode(text, i)
                owner = pdf.raw.FPDFText_GetTextObject(text, i)
                info = owners.get(address(owner))
                if not info:
                    continue
                index, obj, family, raw_name, value = info
                if cp not in TARGETS[family]:
                    continue
                generated = pdf.raw.FPDFText_IsGenerated(text, i)
                unicode_error = pdf.raw.FPDFText_HasUnicodeMapError(text, i)
                assert generated in (0, 1) and unicode_error in (0, 1)
                key = (index, args.scale)
                if key not in bitmaps:
                    bitmaps[key] = render_object_bitmap(doc, page, obj, args.scale)
                image = bitmaps[key]
                box = list(text.get_charbox(i))
                measurement, clip = inspect_crop(image, box, obj.get_bounds(), args.scale, generated)
                if measurement['dark_pixels']:
                    clip.save(args.output/('%s-p%d-o%d-c%d.png'%(data['id'], number, index, i)))
                glyph = pdf.raw.FPDFFont_GetGlyphPath(obj.get_font(), cp, 1000)
                segments = pdf.raw.FPDFGlyphPath_CountGlyphSegments(glyph) if glyph else None
                # Match inventory's documented omission of whitespace inside runs.
                eligible = not chr(cp).isspace() or len(value) == 1
                rows.append(dict(score=data['id'], page=number, text_object_index=index,
                                 char_index=i, font=family, raw_font=raw_name, codepoint=cp,
                                 object_text=value, charbox_pt=box,
                                 bitmap_scale=args.scale, **measurement,
                                 generated_by_pdfium=bool(generated), unicode_mapping_error=bool(unicode_error),
                                 glyph_api_segments=segments, inventory_counted=eligible))
            text.close()
            page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before
        print(data['id'], 'checked; cumulative character occurrences', len(rows), flush=True)
    actual = collections.Counter((r['score'], r['font'], r['codepoint']) for r in rows if r['inventory_counted'])
    report = dict(source_hashes=source_hashes, source_unchanged=True, rows=rows,
                  expected_inventory_characters=sum(expected.values()), all_occurrences=len(rows),
                  statuses=dict(collections.Counter(r['status'] for r in rows)),
                  glyph_api_segment_counts=dict(collections.Counter(str(r['glyph_api_segments']) for r in rows)),
                  all_inventory_occurrences_accounted=actual == expected,
                  generated_spacing_count=sum(r['generated_by_pdfium'] for r in rows),
                  actual_source_character_count=sum(not r['generated_by_pdfium'] for r in rows),
                  glyph_api_alone_proves_no_ink=False,
                  all_occurrences_no_ink=all(r['dark_pixels'] == 0 for r in rows))
    (args.output/'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Inventory', sum(expected.values()), 'actual', len(rows), 'statuses', report['statuses'])
    print('Glyph API segments (diagnostic)', report['glyph_api_segment_counts'])
    assert actual == expected, (actual-expected, expected-actual)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory', type=Path, default=ROOT/'dist/corpus-v2')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--scale', type=float, default=32)
    p.add_argument('--controls-only', action='store_true')
    args = p.parse_args()
    (verify_controls if args.controls_only else run)(args)
