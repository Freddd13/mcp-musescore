"""Render every candidate PDF/font/code key, without universal encoding aliases.

Schema-3 samples keep actual source indices, including controls and spaces.
Conservative silhouette groups reduce repeated pictures for discovery only;
they do not certify meanings or erase per-key provenance. No source is saved,
no FontFile program is accessed, and physical source geometry is retained.
"""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pypdfium2 as pdf
from PIL import Image, ImageChops, ImageDraw, ImageFont
from audit_corpus_shapes import candidate
from audit_catalog_empty_occurrences import address, inspect_crop, render_object_bitmap

ROOT = Path(__file__).resolve().parent
POPCOUNT = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)


def signature(image):
    mask = image.convert('L').point(lambda v:255 if v < 128 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError('No dark ink')
    mask = mask.crop(bbox)
    aspect = mask.width/mask.height
    pixels = np.asarray(mask.resize((64,64))) > 127
    return np.packbits(pixels.flatten()), int(pixels.sum()), aspect


def group_rows(rows, shapes, minimum):
    groups, packed, areas, aspects = [], [], [], []
    for row in rows:
        if row['status'] != 'rendered':
            continue
        mask, area, aspect = shapes[row['image']]
        best = None
        if packed:
            shape_aspects = np.array(aspects)
            ratios = np.minimum(shape_aspects/aspect, aspect/shape_aspects)
            possible = np.flatnonzero(ratios >= minimum**2.5)
            if len(possible):
                masks = np.stack([packed[i] for i in possible])
                overlap = POPCOUNT[np.bitwise_and(masks,mask)].sum(axis=1)
                union = np.array(areas)[possible]+area-overlap
                scores = overlap/np.maximum(union,1)*ratios[possible]**.4
                j = int(np.argmax(scores))
                if scores[j] >= minimum:
                    best = int(possible[j]), float(scores[j])
        if best is None:
            best = len(groups), 1.0
            groups.append(dict(id='K%04d'%(len(groups)+1), representative=row['id'],
                               members=[], minimum_similarity=1.0))
            packed.append(mask);areas.append(area);aspects.append(aspect)
        group = groups[best[0]]
        group['members'].append(row['id'])
        group['minimum_similarity'] = min(group['minimum_similarity'],best[1])
        row['group'] = group['id']
        row['similarity_to_representative'] = best[1]
    return groups


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    rows, skipped, hashes, shapes = [], [], {}, {}
    files = sorted(args.inventory.glob('A*.json'))
    if args.scores:
        files = [p for p in files if p.stem in args.scores]
    for path in files:
        inv = json.loads(path.read_text(encoding='utf-8'))
        assert inv['schema'] == 3
        use_fonts = []
        for family,font in inv['fonts'].items():
            use, reason = candidate(family,font) if font['category'] != 'text' else (False,'ordinary name proposal')
            if use:
                use_fonts.append((family,font,reason))
            else:
                skipped.append(dict(score=inv['id'],font=family,category=font['category'],
                                    keys=len(font['glyphs']),reason=reason))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        hashes[inv['id']] = inv['sha256']
        if not use_fonts:
            continue
        doc = pdf.PdfDocument(source)
        pages = {}
        for family,font,reason in use_fonts:
            for cp,glyph in sorted(font['glyphs'].items()):
                row = dict(id='S%05d'%(len(rows)+1),score=inv['id'],font=family,unicode=cp,
                           codepoint=ord(glyph['char']),occurrences=glyph['count'],selection=reason,
                           errors=[],attempts=[])
                samples = sorted(glyph['samples'],key=lambda s:(not s['intersects_page_bbox'],not s['single'],-s['size_pt']))
                for sample in samples:
                    number = sample['page']
                    if number not in pages:
                        page = doc[number-1];text = page.get_textpage()
                        objects = list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text))
                        pages[number] = page,text,objects
                    page,text,objects = pages[number]
                    obj = objects[sample['text_object_index']]
                    assert obj.get_font().get_base_name() == sample['font']
                    assert re.sub(r'^[A-Z]{6}\+','',sample['font']) == family
                    assert obj.extract() == sample['object_text']
                    assert all(abs(a-b)<.0001 for a,b in zip(obj.get_bounds(),sample['bounds_pt']))
                    a,b,c,d = obj.get_bounds();bbox = page.get_bbox()
                    outside = obj.level == 0 and (c<=bbox[0] or a>=bbox[2] or d<=bbox[1] or b>=bbox[3])
                    attempt = dict(sample=sample,status='outside-visible-page' if outside else 'pending')
                    row['attempts'].append(attempt)
                    if outside:
                        continue
                    try:
                        indices = sample['source_char_indices']
                        assert indices
                        for i in indices:
                            assert not pdf.raw.FPDFText_IsGenerated(text,i)
                            assert pdf.raw.FPDFText_GetUnicode(text,i) == row['codepoint']
                            assert address(pdf.raw.FPDFText_GetTextObject(text,i)) == address(obj.raw)
                        image = render_object_bitmap(doc,page,obj,args.scale)
                        if image is None or image.convert('L').getextrema()[0] == 255:
                            attempt['status'] = 'whole-object-no-ink'
                            continue
                        whole = image
                        bounds = list(obj.get_bounds())
                        if sample['source_character_count'] != 1:
                            box = list(text.get_charbox(indices[0]))
                            measurement,image = inspect_crop(image,box,bounds,args.scale)
                            attempt['measurement'] = measurement
                            if not measurement['dark_pixels']:
                                attempt['status'] = 'character-box-no-ink'
                                continue
                            if not measurement['charbox_inside_rendered_object']:
                                attempt['status'] = 'character-object-coordinate-review'
                                continue
                            bounds = box
                        else:
                            box = list(text.get_charbox(indices[0]))
                        shape = signature(image)
                        filename = row['id']+'.png'
                        image.save(args.output/filename)
                        row.update(status='rendered',image=filename,sample=sample,bounds_pt=bounds,
                                   charbox_pt=box,bitmap_scale=args.scale,pixel_size=image.size,
                                   compound_crop=sample['source_character_count']!=1)
                        if row['compound_crop']:
                            full = row['id']+'-object.png';whole.save(args.output/full);row['whole_object_image'] = full
                        shapes[filename] = shape
                        attempt['status'] = 'rendered'
                        break
                    except (ValueError,RuntimeError) as error:
                        attempt['status'] = 'render-error';row['errors'].append(str(error))
                else:
                    row['status'] = 'needs-visibility-review'
                rows.append(row)
        for page,text,objects in pages.values():
            text.close();page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == inv['sha256']
        print(inv['id'],'candidate keys so far',len(rows),flush=True)
    groups = group_rows(rows,shapes,args.minimum)
    by_id = {r['id']:r for r in rows}
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(groups),48):
        board = Image.new('RGB',(1920,1680),'white');draw = ImageDraw.Draw(board)
        for i,group in enumerate(groups[start:start+48]):
            x,y = i%8*240,i//8*280
            row = by_id[group['representative']]
            draw.text((x+5,y+5),'%s n%d %.3f'%(group['id'],len(group['members']),group['minimum_similarity']),font=font,fill='black')
            draw.text((x+5,y+27),row['score']+' '+row['unicode']+' '+row['font'][:15],font=font,fill='black')
            draw.text((x+5,y+49),'p%d o%d %s'%(row['sample']['page'],row['sample']['text_object_index'],row['id']),font=font,fill='black')
            im = Image.open(args.output/row['image']).convert('RGB')
            bbox = ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
            if bbox:im = im.crop(bbox)
            im.thumbnail((210,195));board.paste(im,(x+(240-im.width)//2,y+77))
        board.save(args.output/('groups-%02d.png'%(start//48+1)))
    report = dict(schema=1,inventory_schema=3,source_hashes=hashes,source_hashes_unchanged=True,
                  rows=rows,skipped_font_groups=skipped,groups=groups,
                  statuses=dict(collections.Counter(r['status'] for r in rows)),
                  grouping_minimum=args.minimum,mask_size=[64,64],all_group_semantics_certified=False,
                  sample_scope='Every candidate per-PDF font/code key; not every occurrence or font handle')
    (args.output/'catalog.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Keys',len(rows),report['statuses'],'geometric groups',len(groups),'boards',(len(groups)+47)//48)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v3-176')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--scores',nargs='+')
    p.add_argument('--scale',type=float,default=24)
    p.add_argument('--minimum',type=float,default=.96)
    run(p.parse_args())
