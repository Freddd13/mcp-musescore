"""Inventory actual live PDF font resources and render every resource/code key.

Unlike family-name grouping, a resource is identified by FPDF_FONT within one
live document. All pages/textpages stay open until capture completes, so a
released page cannot cause handle reuse. Handles never identify fonts across
documents/runs. No FontFile program is read or source document saved.
"""
import argparse
import collections
import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageChops,ImageDraw,ImageFont
from audit_catalog_empty_occurrences import address,inspect_crop,render_object_bitmap
from catalog_corpus_keys import POPCOUNT,group_rows,signature
from source.reviewed_corpus_keys import CATALOG_SHA

ROOT=Path(__file__).resolve().parent


def rank(sample):
    return (not sample['intersects_page_bbox'],not sample['single'],
            abs(sample['size_pt']/sample['staff_space_pt']-4),-sample['size_pt'])


def run(args):
    assert hashlib.sha256(args.baseline.read_bytes()).hexdigest()==CATALOG_SHA
    baseline=json.loads(args.baseline.read_text(encoding='utf-8'))
    base_rows={(r['score'],r['font'],r['codepoint']):r for r in baseline['rows']}
    base_shapes={r['id']:signature(Image.open(args.baseline.parent/r['image'])) for r in baseline['rows'] if r['status']=='rendered'}
    families=collections.defaultdict(set)
    for r in baseline['rows']:families[r['score']].add(r['font'])
    args.output.mkdir(parents=True,exist_ok=False)
    rows=[];resources=[];hashes={};shapes={};scan_counts={}
    scores=sorted(args.scores or baseline['source_hashes'])
    for score in scores:
        inv=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        source=Path(inv['source_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']==baseline['source_hashes'][score]
        hashes[score]=inv['sha256']
        if not families[score]:
            scan_counts[score]=dict(pages=inv['pages'],objects=0,source_characters=0,resources=0)
            continue
        doc=pdf.PdfDocument(source);pages={};slots={};keys={};object_count=0;character_count=0
        for number in range(1,len(doc)+1):
            page=doc[number-1];text=page.get_textpage()
            objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text))
            pages[number]=page,text,objects
            owners={};characters=collections.defaultdict(list)
            for index,obj in enumerate(objects):
                raw_name=obj.get_font().get_base_name();family=re.sub(r'^[A-Z]{6}\+','',raw_name)
                if family not in families[score]:continue
                owners[address(obj.raw)]=(index,obj,raw_name,family)
            for i in range(text.count_chars()):
                if pdf.raw.FPDFText_IsGenerated(text,i):continue
                owner=owners.get(address(pdf.raw.FPDFText_GetTextObject(text,i)))
                if owner:
                    characters[owner[0]].append((i,pdf.raw.FPDFText_GetUnicode(text,i)))
            for index,obj,raw_name,family in owners.values():
                pointer=address(pdf.raw.FPDFTextObj_GetFont(obj))
                assert pointer is not None
                if pointer not in slots:
                    slots[pointer]=dict(id='%s:F%03d'%(score,len(slots)+1),score=score,font=family,raw_name=raw_name,
                                        objects=0,source_characters=0,pages=[],codepoints=set())
                resource=slots[pointer]
                assert resource['raw_name']==raw_name and resource['font']==family
                resource['objects']+=1;object_count+=1
                if number not in resource['pages']:resource['pages'].append(number)
                actual=characters[index];resource['source_characters']+=len(actual);character_count+=len(actual)
                grouped=collections.defaultdict(list)
                for i,cp in actual:grouped[cp].append(i)
                for cp,indices in grouped.items():
                    resource['codepoints'].add(cp)
                    key=resource['id'],cp
                    entry=keys.setdefault(key,dict(resource=resource['id'],score=score,font=family,raw_name=raw_name,
                        codepoint=cp,unicode='U+%04X'%cp,occurrences=0,samples=[]))
                    entry['occurrences']+=len(indices)
                    matrix=obj.get_matrix();size=math.hypot(matrix.a,matrix.b)*obj.get_font_size()
                    a,b,c,d=obj.get_bounds();bbox=page.get_bbox()
                    spaces=inv['page_geometry'][number-1]['staff_spaces']
                    sp=spaces[0]['space_pt'] if spaces else size/4 or 1
                    sample=dict(page=number,text_object_index=index,font=raw_name,size_pt=size,
                                matrix=matrix.get(),bounds_pt=obj.get_bounds(),level=obj.level,
                                single=len(actual)==1,source_character_count=len(actual),
                                source_char_indices=indices,object_text=obj.extract(),staff_space_pt=sp,
                                intersects_page_bbox=c>bbox[0] and a<bbox[2] and d>bbox[1] and b<bbox[3])
                    entry['samples'].append(sample);entry['samples'].sort(key=rank);del entry['samples'][3:]
        expected=collections.Counter({(family,int(cp[2:],16)):g['count'] for family in families[score]
            for cp,g in inv['fonts'][family]['glyphs'].items()})
        actual=collections.Counter()
        for entry in keys.values():actual[(entry['font'],entry['codepoint'])]+=entry['occurrences']
        assert actual==expected,(score,actual-expected,expected-actual)
        assert object_count==sum(inv['fonts'][f]['objects'] for f in families[score])
        for family in families[score]:
            assert {r['raw_name'] for r in slots.values() if r['font']==family}==set(inv['fonts'][family]['raw_names'])
        scan_counts[score]=dict(pages=len(doc),objects=object_count,source_characters=character_count,resources=len(slots))
        for resource in slots.values():
            resource['codepoints']=sorted(resource['codepoints']);resources.append(resource)
        for entry in sorted(keys.values(),key=lambda r:(r['resource'],r['codepoint'])):
            row=dict(entry,id='R%05d'%(len(rows)+1),attempts=[])
            parent=base_rows[score,entry['font'],entry['codepoint']]
            row['family_code_sample']=parent['id'];row['family_code_status']=parent['status']
            if parent['status']=='rendered':row['family_code_group']=parent['group']
            for sample in entry['samples']:
                page,text,objects=pages[sample['page']];obj=objects[sample['text_object_index']]
                assert obj.get_font().get_base_name()==entry['raw_name'] and obj.extract()==sample['object_text']
                attempt=dict(page=sample['page'],text_object_index=sample['text_object_index'])
                row['attempts'].append(attempt)
                a,b,c,d=obj.get_bounds();bbox=page.get_bbox()
                if obj.level==0 and (c<=bbox[0] or a>=bbox[2] or d<=bbox[1] or b>=bbox[3]):
                    attempt['status']='outside-visible-page';continue
                image=render_object_bitmap(doc,page,obj,args.scale)
                if image is None or image.convert('L').getextrema()[0]==255:
                    attempt['status']='whole-object-no-ink';continue
                full=image;bounds=list(obj.get_bounds());indices=sample['source_char_indices'];i=indices[0]
                assert pdf.raw.FPDFText_GetUnicode(text,i)==entry['codepoint']
                assert not pdf.raw.FPDFText_IsGenerated(text,i)
                assert address(pdf.raw.FPDFText_GetTextObject(text,i))==address(obj.raw)
                if not sample['single']:
                    box=list(text.get_charbox(i));measurement,image=inspect_crop(image,box,bounds,args.scale)
                    attempt['measurement']=measurement
                    if not measurement['dark_pixels']:
                        attempt['status']='character-box-no-ink';continue
                    if not measurement['charbox_inside_rendered_object']:
                        attempt['status']='coordinate-review';continue
                    bounds=box
                try:shape=signature(image)
                except ValueError:
                    attempt['status']='no-dark-ink';continue
                filename=row['id']+'.png';image.save(args.output/filename);shapes[filename]=shape
                row.update(status='rendered',image=filename,sample=sample,bounds_pt=bounds,bitmap_scale=args.scale,
                           compound_crop=not sample['single'])
                if not sample['single']:
                    full_name=row['id']+'-object.png';full.save(args.output/full_name);row['whole_object_image']=full_name
                if parent['status']=='rendered':
                    mask,area,aspect=shape;other,other_area,other_aspect=base_shapes[parent['id']]
                    overlap=int(POPCOUNT[np.bitwise_and(mask,other)].sum())
                    row['same_family_code_similarity']=overlap/max(area+other_area-overlap,1)*min(aspect/other_aspect,other_aspect/aspect)**.4
                attempt['status']='rendered';break
            else:row['status']='needs-visibility-review'
            rows.append(row)
        for page,text,objects in pages.values():text.close();page.close()
        doc.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']
        print(score,'live resources',len(slots),'resource/code keys',len(keys),'source characters',character_count,flush=True)
    groups=group_rows(rows,shapes,args.minimum)
    rename={g['id']:'F%04d'%(i+1) for i,g in enumerate(groups)}
    for group in groups:group['id']=rename[group['id']]
    for row in rows:
        if 'group' in row:row['group']=rename[row['group']]
    by_id={r['id']:r for r in rows};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(groups),48):
        board=Image.new('RGB',(1920,1680),'white');draw=ImageDraw.Draw(board)
        for i,group in enumerate(groups[start:start+48]):
            x,y=i%8*240,i//8*280;row=by_id[group['representative']]
            draw.text((x+5,y+5),'%s n%d'%(group['id'],len(group['members'])),font=font,fill='black')
            draw.text((x+5,y+27),row['resource']+' '+row['unicode'],font=font,fill='black')
            draw.text((x+5,y+49),'p%d o%d %s'%(row['sample']['page'],row['sample']['text_object_index'],row['id']),font=font,fill='black')
            im=Image.open(args.output/row['image']).convert('RGB')
            bbox=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
            if bbox:im=im.crop(bbox)
            im.thumbnail((210,195));board.paste(im,(x+(240-im.width)//2,y+77))
        board.save(args.output/('resources-%02d.png'%(start//48+1)))
    report=dict(schema=1,baseline_sha256=CATALOG_SHA,source_hashes=hashes,scan_counts=scan_counts,
                resources=resources,rows=rows,groups=groups,source_hashes_unchanged=True,
                all_family_code_counts_reconciled=True,pages_retained_until_document_capture_complete=True,
                resource_ids_are_run_local=True,font_file_stream_read_by_script=False,
                font_file_program_extracted=False,source_pdf_saved=False,
                statuses=dict(collections.Counter(r['status'] for r in rows)),
                grouping_minimum=args.minimum,group_semantics_certified=False)
    (args.output/'resources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Sources',len(hashes),'resources',len(resources),'keys',len(rows),report['statuses'],'groups',len(groups))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,default=ROOT/'dist/all-candidate-keys-186/catalog.json')
    p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v3-176')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--scores',nargs='+')
    p.add_argument('--scale',type=float,default=24);p.add_argument('--minimum',type=float,default=.96)
    run(p.parse_args())
