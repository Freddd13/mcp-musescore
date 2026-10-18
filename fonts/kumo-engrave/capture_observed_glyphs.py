"""Capture context-reviewed character curves, rejecting ambiguous PDF mappings.

Compare the displayed vector result to the actual original text object before
acceptance. An explicitly allowed raster fallback records a failed Unicode
mapping instead of silently turning a missing-glyph box into a score symbol.
No source font stream or PDF is saved. Output is private local study data.
"""
import argparse,ctypes,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw
from source.pdf_glyph_geometry import glyph_commands,displayed_commands
from catalog_pdf_glyphs import render_character
from capture_pdf_reference import trace_pixels
from verify_vector_font import insert_source_component,tight

ROOT=Path(__file__).resolve().parent


def compare(doc,page,text,obj,char,commands,output,scale):
    image,box,origin=render_character(doc,page,text,obj,char,scale)
    paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image);original=tight(paper)
    objects=list(page.get_objects())
    for member in objects:assert pdf.raw.FPDFPageObj_SetIsActive(member,False)
    raw=insert_source_component(page,displayed_commands(obj,commands,origin))
    a,b,c,d=box;w,h=page.get_size();pad=2
    bitmap=page.render(scale=scale,crop=(a-pad,b-pad,w-c-pad,h-d-pad))
    vector=tight(bitmap.to_pil().copy());bitmap.close()
    assert pdf.raw.FPDFPage_RemoveObject(page,raw);pdf.raw.FPDFPageObj_Destroy(raw)
    for member in objects:assert pdf.raw.FPDFPageObj_SetIsActive(member,True)
    aa=np.asarray(original.convert('L'))<160;bb=np.asarray(vector.resize(original.size).convert('L'))<160
    iou=float(np.logical_and(aa,bb).sum()/np.logical_or(aa,bb).sum())
    delta=[a-b for a,b in zip(original.size,vector.size)]
    board=Image.new('RGB',(original.width+vector.width+45,max(original.height,vector.height)+40),'white')
    ImageDraw.Draw(board).text((5,5),'Actual PDF / displayed character curves',fill='black')
    board.paste(original,(5,30));board.paste(vector,(original.width+25,30));board.save(output)
    return dict(ink_iou=iou,delta=delta,passed=iou>.95 and all(abs(v)<=3 for v in delta)),image,box,origin


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    spec=json.loads(args.spec.read_text(encoding='utf-8'));catalog=json.loads(args.catalog.read_text(encoding='utf-8'))
    rows=[];sources={}
    for choice in spec['glyphs']:
        context=catalog[choice['group']];sample=context['sample'];source=Path(sample['source'])
        sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha==sample['sha256'];sources[str(source)]=sha
        inv=json.loads((args.inventory/(sample['score']+'.json')).read_text(encoding='utf-8'))
        spaces=inv['page_geometry'][sample['page']-1]['staff_spaces'];assert spaces
        doc=pdf.PdfDocument(source);page=doc[sample['page']-1];text=page.get_textpage()
        objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=objects[sample['text_object_index']]
        commands=glyph_commands(obj,context['char'])
        verification,image,box,origin=compare(doc,page,text,obj,context['char'],commands,args.output/(choice['symbol']+'.png'),args.scale)
        width=ctypes.c_float()
        assert pdf.raw.FPDFFont_GetGlyphWidth(pdf.raw.FPDFTextObj_GetFont(obj),ord(context['char']),obj.get_font_size(),ctypes.byref(width))
        record=dict(choice=choice,source=str(source),source_sha256=sha,score=sample['score'],page=sample['page'],object_index=sample['text_object_index'],
                    char=context['char'],source_text=obj.extract(),matrix=obj.get_matrix().get(),font_size=obj.get_font_size(),
                    staff_space_pt=spaces[0]['space_pt'],commands=commands,source_advance=width.value,verification=verification)
        if not verification['passed']:
            if choice.get('reject_retains_previous'):
                record['rejected']=True
                rows.append(record)
                text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
                print(choice['symbol'],'rejected; previous glyph retained',verification,flush=True)
                continue
            assert choice.get('fallback_raster'),(choice['symbol'],verification)
            # Use only the actual displayed character, never the rejected path.
            unit=250/spaces[0]['space_pt'];loops=trace_pixels(np.asarray(image.getchannel('A'))>127)
            record['raster_outlines']=[[[round((box[0]-origin[0]+x/args.scale)*unit,6),round((box[3]-origin[1]-y/args.scale)*unit,6)] for x,y in loop] for loop in loops]
            record.pop('commands');record['fallback_reason']='Unicode-to-glyph API returned a shape unlike the original; actual rendered character used'
        rows.append(record)
        for derived in spec['derived']:
            if derived.get('group')!=choice['group']:continue
            pieces=[];checks=[]
            for index in derived['text_objects']:
                member=objects[index];character=member.extract().strip();assert len(character)==1
                member_commands=glyph_commands(member,character)
                check,*_=compare(doc,page,text,member,character,member_commands,args.output/(derived['symbol']+'-part%d.png'%index),args.scale)
                assert check['passed'];checks.append(dict(object_index=index,**check))
                pieces.extend(displayed_commands(member,member_commands,[member.get_matrix().e,member.get_matrix().f]))
            rows.append(dict(choice=derived,source=str(source),source_sha256=sha,page=sample['page'],world_commands=pieces,
                             staff_space_pt=spaces[0]['space_pt'],object_indices=derived['text_objects'],
                             origin_pt=[obj.get_matrix().e,obj.get_matrix().f],component_verification=checks))
        text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
        print(choice['symbol'],verification,'raster fallback' if 'raster_outlines' in record else 'curves',flush=True)
    output=dict(version=spec['version'],sources=sources,rows=rows,spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest(),source_unchanged=True)
    (args.output/'capture.json').write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec',type=Path,default=ROOT/'source/observed_roles.json')
    p.add_argument('--catalog',type=Path,default=ROOT/'dist/group-context-070/catalog.json');p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v2')
    p.add_argument('--output',type=Path,required=True);p.add_argument('--scale',type=float,default=64);run(p.parse_args())
