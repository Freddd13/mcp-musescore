"""Resolve non-visible hidden-font objects by page bounds and isolated rendering.

All source PDFs are read only. Object activation changes are in memory and
restored; no PDF or embedded font program is saved. Full-page renders protect
against empty/misleading character bounds before enlarged local inspection.
"""
import argparse
import collections
import ctypes
import hashlib
import json
from pathlib import Path
import pypdfium2 as pdf
from PIL import ImageOps
from source.reviewed_catalog_roles import HIDDEN_OBJECTS_HASH

ROOT = Path(__file__).resolve().parent
OBJECTS_SHA = HIDDEN_OBJECTS_HASH


def address(raw):
    return ctypes.cast(raw, ctypes.c_void_p).value


def raster_extrema(page, scale, crop=None):
    kwargs = dict(scale=scale)
    if crop is not None:
        kwargs['crop'] = crop
    bitmap = page.render(**kwargs)
    image = bitmap.to_pil().copy().convert('RGB')
    bitmap.close()
    return ImageOps.grayscale(image).getextrema(), image


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    assert hashlib.sha256(args.objects.read_bytes()).hexdigest() == OBJECTS_SHA
    data = json.loads(args.objects.read_text(encoding='utf-8'))
    pending = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in data['objects']:
        if row['status'] != 'rendered':
            pending[row['score']][row['page']].append(row)
    result = []
    controls = []
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
            within = []
            for row in rows:
                obj = objects[row['text_object_index']]
                assert obj.level == 0, 'Nested form needs transformed page bounds, not local bounds'
                assert obj.extract() == row['object_text']
                assert obj.get_font().get_base_name() == row['raw_font']
                assert all(abs(a-b) < .0001 for a, b in zip(obj.get_bounds(), row['bounds_pt']))
                a, b, c, d = obj.get_bounds()
                record = dict(score=score, page=number, text_object_index=row['text_object_index'],
                              group=row['group'], object_text=row['object_text'], bounds_pt=obj.get_bounds(),
                              page_bbox=page.get_bbox(), level=0, source_sha256=inv['sha256'])
                if c <= 0 or a >= w or d <= 0 or b >= h:
                    record['status'] = 'wholly-outside-visible-page'
                    result.append(record)
                else:
                    within.append((obj, record))
            if within:
                top = [pdf.raw.FPDFPage_GetObject(page, i) for i in range(pdf.raw.FPDFPage_CountObjects(page))]
                states = []
                for obj in top:
                    value = ctypes.c_int()
                    assert pdf.raw.FPDFPageObj_GetIsActive(obj, ctypes.byref(value))
                    states.append(bool(value.value))
                    assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                try:
                    for obj, record in within:
                        assert address(obj.raw) in {address(o) for o in top}
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, True)
                        whole, whole_image = raster_extrema(page, 2)
                        a, b, c, d = obj.get_bounds()
                        left, bottom, right, upper = max(0, a-2), max(0, b-2), min(w, c+2), min(h, d+2)
                        local, local_image = raster_extrema(page, 32, (left, bottom, w-right, h-upper))
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                        record.update(whole_page_2x_luma=whole, local_32x_luma=local,
                                      status='isolated-page-no-ink' if whole == local == (255, 255) else 'visible-in-page-render-review')
                        if record['status'] == 'visible-in-page-render-review':
                            prefix='%s-p%d-o%d'%(score, number, record['text_object_index'])
                            whole_image.save(args.output/(prefix+'-page.png'))
                            local_image.save(args.output/(prefix+'-local.png'))
                        result.append(record)
                    # A known-visible neighbouring object must survive isolation.
                    candidates=[r for r in data['objects'] if r['score']==score and r['page']==number and r['status']=='rendered']
                    for candidate in candidates:
                        obj=objects[candidate['text_object_index']]
                        a,b,c,d=obj.get_bounds()
                        if obj.level or c<=0 or a>=w or d<=0 or b>=h:
                            continue
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, True)
                        extrema, image=raster_extrema(page, 2)
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, False)
                        if extrema[0]<255:
                            controls.append(dict(score=score, page=number, text_object_index=candidate['text_object_index'],
                                                 whole_page_2x_luma=extrema))
                            break
                    else:
                        raise AssertionError(('No visible isolated control on source page',score,number))
                finally:
                    for obj, active in zip(top, states):
                        assert pdf.raw.FPDFPageObj_SetIsActive(obj, active)
            text.close()
            page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        print(score, 'non-visible objects resolved', sum(r['score'] == score for r in result), flush=True)
    expected={(r['score'],r['page'],r['text_object_index']) for r in data['objects'] if r['status']!='rendered'}
    actual={(r['score'],r['page'],r['text_object_index']) for r in result}
    assert expected==actual and len(actual)==len(result)==500
    report=dict(input_sha256=OBJECTS_SHA, rows=result, visible_controls=controls,
                statuses=dict(collections.Counter(r['status'] for r in result)), source_hashes_unchanged=True,
                all_500_accounted=True, no_source_pdf_saved=True)
    (args.output/'visibility.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('All 500 accounted:',report['statuses'],'visible source-page controls',len(controls))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--objects',type=Path,default=ROOT/'dist/hidden-all-objects-169/objects.json')
    p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v2')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
