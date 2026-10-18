"""Compare source-character inventories and render all newly indexed positions.

No Unicode whitespace/name is treated as a semantic verdict. Visible crops,
ambiguous compounds and unrendered whole objects remain explicit review queues.
Source documents and previous checkpoints are read only.
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
from audit_catalog_empty_occurrences import inspect_crop, render_object_bitmap

ROOT=Path(__file__).resolve().parent


def address(raw):
    return ctypes.cast(raw,ctypes.c_void_p).value


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    additions=[];removed=[];inventories={};targets=collections.defaultdict(lambda:collections.defaultdict(set))
    for path in sorted(args.after.glob('A*.json')):
        new=json.loads(path.read_text(encoding='utf-8'));old=json.loads((args.before/path.name).read_text(encoding='utf-8'))
        assert new['schema']==3 and old['schema']==2
        assert new['sha256']==old['sha256'] and new['pages']==old['pages'] and new['text_objects']==old['text_objects']
        assert set(new['fonts'])==set(old['fonts'])
        inventories[new['id']]=new
        for family,font in new['fonts'].items():
            previous=old['fonts'][family]
            assert font['objects']==previous['objects']
            for cp in sorted(set(font['glyphs'])-set(previous['glyphs'])):
                glyph=font['glyphs'][cp]
                additions.append(dict(score=new['id'],font=family,unicode=cp,codepoint=int(cp[2:],16),
                                      category=font['category'],count=glyph['count'],samples=glyph['samples']))
                targets[new['id']][family].add(int(cp[2:],16))
            for cp in sorted(set(previous['glyphs'])-set(font['glyphs'])):
                removed.append(dict(score=new['id'],font=family,unicode=cp,old=previous['glyphs'][cp]))
    rows=[];reviews={};unrendered={};sources={}
    for score,families in targets.items():
        inv=inventories[score];source=Path(inv['source_path'])
        possible_codes={c for values in families.values() for c in values}
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256'];sources[score]=inv['sha256']
        doc=pdf.PdfDocument(source)
        for number in range(1,len(doc)+1):
            page=doc[number-1];text=page.get_textpage();owners={};bitmaps={}
            for index,obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)):
                family=re.sub(r'^[A-Z]{6}\+','',obj.get_font().get_base_name())
                if family in families:owners[address(obj.raw)]=(index,obj,family)
            for i in range(text.count_chars()):
                cp=pdf.raw.FPDFText_GetUnicode(text,i)
                if cp not in possible_codes:continue
                if pdf.raw.FPDFText_IsGenerated(text,i):continue
                info=owners.get(address(pdf.raw.FPDFText_GetTextObject(text,i)))
                if not info:continue
                index,obj,family=info
                if cp not in families[family]:continue
                objkey=(score,number,index)
                if index not in bitmaps:bitmaps[index]=render_object_bitmap(doc,page,obj,args.scale)
                image=bitmaps[index];box=list(text.get_charbox(i));bounds=list(obj.get_bounds());bbox=list(page.get_bbox())
                error=pdf.raw.FPDFText_HasUnicodeMapError(text,i);assert error in (0,1)
                measurement,clip=inspect_crop(image,box,bounds,args.scale)
                image_ink=image is not None and image.convert('L').getextrema()[0]<255
                outside=obj.level==0 and (bounds[2]<=bbox[0] or bounds[0]>=bbox[2] or bounds[3]<=bbox[1] or bounds[1]>=bbox[3])
                if outside:status='object-outside-visible-page'
                elif not image_ink:status='unrendered-whole-object-review'
                elif error or cp==0:status='ambiguous-visible-compound-review'
                elif measurement['dark_pixels']:status='visible-target-character-review'
                else:status='no-target-ink-in-original-bitmap'
                row=dict(score=score,page=number,text_object_index=index,char_index=i,font=family,codepoint=cp,
                         object_text=obj.extract(),raw_font=obj.get_font().get_base_name(),level=obj.level,
                         charbox_pt=box,bounds_pt=bounds,page_bbox=bbox,unicode_mapping_error=bool(error),
                         status=status,measurement=measurement)
                rows.append(row)
                if status=='unrendered-whole-object-review':unrendered[objkey]=row
                if status.endswith('compound-review') or status=='visible-target-character-review':
                    identity=(score,family,cp,obj.extract(),hashlib.sha256(image.tobytes()).hexdigest() if error or cp==0 else None)
                    if identity not in reviews:
                        serial=len(reviews)+1;filename='review-%04d.png'%serial
                        image.save(args.output/filename)
                        if clip is not None and measurement['dark_pixels']:clip.save(args.output/('character-%04d.png'%serial))
                        reviews[identity]=dict(row,image=filename,serial=serial)
            text.close();page.close()
        doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']
        print(score,'newly indexed source positions',sum(r['score']==score for r in rows),flush=True)
    expected=collections.Counter({(r['score'],r['font'],r['codepoint']):r['count'] for r in additions})
    actual=collections.Counter((r['score'],r['font'],r['codepoint']) for r in rows)
    assert actual==expected,(actual-expected,expected-actual)
    review_rows=list(reviews.values());font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(review_rows),24):
        board=Image.new('RGB',(1800,1440),'white');draw=ImageDraw.Draw(board)
        for i,row in enumerate(review_rows[start:start+24]):
            x,y=i%4*450,i//4*240
            draw.text((x+5,y+5),'R%04d %s %s U+%04X'%(row['serial'],row['score'],row['font'],row['codepoint']),font=font,fill='black')
            draw.text((x+5,y+29),'p%d o%d %s'%(row['page'],row['text_object_index'],row['status'][:22]),font=font,fill='black')
            im=Image.open(args.output/row['image']);im.thumbnail((425,160));board.paste(im,(x+10,y+65))
        board.save(args.output/('review-board-%02d.png'%(start//24+1)))
    report=dict(source_hashes=sources,source_hashes_unchanged=True,added=additions,removed=removed,
                rows=rows,reviews=review_rows,unrendered_objects=list(unrendered.values()),
                status_counts=dict(collections.Counter(r['status'] for r in rows)),
                all_new_key_occurrences_accounted=True,semantic_roles_certified=False)
    (args.output/'delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Added per-PDF keys',len(additions),'all source positions',len(rows),report['status_counts'])
    print('Visible review representatives',len(review_rows),'unrendered whole objects',len(unrendered),'removed synthetic/other keys',len(removed))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--before',type=Path,default=ROOT/'dist/corpus-v2')
    p.add_argument('--after',type=Path,default=ROOT/'dist/corpus-v3-176')
    p.add_argument('--output',type=Path,required=True);p.add_argument('--scale',type=float,default=16)
    run(p.parse_args())
