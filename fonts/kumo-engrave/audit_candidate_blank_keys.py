"""Resolve all 117 unrendered candidate keys using actual source positions.

Reuse pinned all-occurrence evidence by exact source position, never by a
global family/code alias. Scan every remaining position independently. A blank
character crop is evidence about this source occurrence, not a font program.
"""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

import pypdfium2 as pdf
from PIL import Image, ImageDraw, ImageFont
from audit_catalog_empty_occurrences import address, inspect_crop, render_object_bitmap
from source.reviewed_corpus_keys import CATALOG_SHA
from source.reviewed_inventory_delta import DELTA_SHA
from source.reviewed_catalog_roles import EMPTY_CATALOG_AUDIT_HASH, EMPTY_CATALOG_CONTROLS_HASH

ROOT = Path(__file__).resolve().parent


def pinned(path, expected):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected,path
    return json.loads(path.read_text(encoding='utf-8'))


def identity(r):
    return r['score'],r['page'],r['text_object_index'],r['char_index'],r['font'],r['codepoint']


def font_key(r):
    return r['score'],r['font'],r['codepoint']


def run(args):
    catalog = pinned(args.catalog,CATALOG_SHA)
    empty = pinned(args.empty,EMPTY_CATALOG_AUDIT_HASH)
    controls = pinned(args.empty_controls,EMPTY_CATALOG_CONTROLS_HASH)
    delta = pinned(args.delta,DELTA_SHA)
    args.output.mkdir(parents=True,exist_ok=False)
    pending = [r for r in catalog['rows'] if r['status']!='rendered']
    expected = collections.Counter({font_key(r):r['occurrences'] for r in pending})
    assert len(pending)==117 and sum(expected.values())==544
    evidence = {}
    isolated = {(r['score'],r['page'],r['text_object_index']):r for r in controls['isolated_null_bitmap_objects']}
    for r in empty['rows']:
        if r['generated_by_pdfium'] or font_key(r) not in expected:continue
        assert not r['dark_pixels']
        if r['status']=='whole-object-no-bitmap':
            proof = isolated[(r['score'],r['page'],r['text_object_index'])]
            assert proof['renders'] == [dict(scale=32,luma=[255,255]),dict(scale=64,luma=[255,255])]
        evidence[identity(r)] = dict(r,proof='catalog-empty-159 + controls-166')
    for r in delta['rows']:
        if font_key(r) not in expected or identity(r) in evidence:continue
        assert r['status']=='no-target-ink-in-original-bitmap' and not r['measurement']['dark_pixels']
        evidence[identity(r)] = dict(r,proof='inventory-delta-review-179')
    known = collections.Counter(font_key(r) for r in evidence.values())
    assert not (known-expected)
    missing = expected-known
    assert len(missing)==16 and sum(missing.values())==72
    images = []
    for score in sorted({k[0] for k in missing}):
        families = collections.defaultdict(set)
        for s,f,cp in missing:
            if s==score:families[f].add(cp)
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source = Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']==catalog['source_hashes'][score]
        doc = pdf.PdfDocument(source)
        for number in range(1,len(doc)+1):
            page = doc[number-1];text = page.get_textpage();owners={};bitmaps={}
            for index,obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)):
                family = re.sub(r'^[A-Z]{6}\+','',obj.get_font().get_base_name())
                if family in families:owners[address(obj.raw)] = index,obj,family
            for i in range(text.count_chars()):
                cp = pdf.raw.FPDFText_GetUnicode(text,i)
                if pdf.raw.FPDFText_IsGenerated(text,i):continue
                info = owners.get(address(pdf.raw.FPDFText_GetTextObject(text,i)))
                if not info:continue
                index,obj,family = info
                if cp not in families[family]:continue
                if index not in bitmaps:
                    image = render_object_bitmap(doc,page,obj,32)
                    assert image is not None,'A new null bitmap requires independent page isolation'
                    bitmaps[index] = image
                    filename = '%s-p%d-o%d.png'%(score,number,index)
                    image.save(args.output/filename)
                    images.append(dict(image=filename,label='%s p%d o%d'%(score,number,index)))
                image = bitmaps[index]
                measurement,clip = inspect_crop(image,text.get_charbox(i),obj.get_bounds(),32)
                assert not measurement['dark_pixels'],(score,number,index,i,measurement)
                row = dict(score=score,page=number,text_object_index=index,char_index=i,font=family,codepoint=cp,
                           object_text=obj.extract(),charbox_pt=text.get_charbox(i),bounds_pt=obj.get_bounds(),
                           proof='new-source-object-32x',measurement=measurement)
                evidence[identity(row)] = row
            text.close();page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']
        print(score,'remaining source positions checked',sum(font_key(r)[0]==score and r['proof']=='new-source-object-32x' for r in evidence.values()),flush=True)
    actual = collections.Counter(font_key(r) for r in evidence.values())
    assert actual==expected and len(evidence)==544
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for start in range(0,len(images),32):
        board = Image.new('RGB',(1920,1440),'white');draw = ImageDraw.Draw(board)
        for i,row in enumerate(images[start:start+32]):
            x,y = i%4*480,i//4*180
            draw.text((x+5,y+5),row['label'],font=font,fill='black')
            im=Image.open(args.output/row['image']);im.thumbnail((455,130));board.paste(im,(x+8,y+38))
        board.save(args.output/('objects-%02d.png'%(start//32+1)))
    for score,sha in catalog['source_hashes'].items():
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(Path(inv['source_path']).read_bytes()).hexdigest()==sha==inv['sha256']
    report = dict(catalog_sha256=CATALOG_SHA,empty_sha256=EMPTY_CATALOG_AUDIT_HASH,
                  controls_sha256=EMPTY_CATALOG_CONTROLS_HASH,delta_sha256=DELTA_SHA,
                  pending_keys=117,actual_source_positions=544,rows=list(evidence.values()),
                  proof_counts=dict(collections.Counter(r['proof'] for r in evidence.values())),
                  new_whole_objects=len(images),source_hashes_unchanged=True,
                  all_pending_key_source_positions_accounted=True,font_program_emptiness_claimed=False)
    (args.output/'visibility.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('117 keys / 544 actual source positions',report['proof_counts'],'new whole objects',len(images))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('catalog','all-candidate-keys-186/catalog.json'),('empty','catalog-empty-159/audit.json'),
                         ('empty-controls','catalog-empty-controls-166/controls.json'),
                         ('delta','inventory-delta-review-179/delta.json'),('inventory','corpus-v3-176')]:
        p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
