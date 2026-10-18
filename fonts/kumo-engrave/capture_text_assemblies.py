"""Validate mixed PDF text as a whole before selecting curve components.

Character boxes can include neighboring ink. Reconstruct a complete comparison
span (one whole formula side, or e+k when extracting e) from displayed glyph
paths and character origins; retain the comparison and all positions. Curves stay private and
are not called correct merely because a Unicode lookup returned a path.
"""
import argparse,ctypes,hashlib,json
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw
from source.pdf_glyph_geometry import glyph_commands,displayed_commands
from verify_vector_font import insert_source_component,tight
from catalog_pending_fonts import render_object

ROOT=Path(__file__).resolve().parent


def object_characters(text,obj):
    address=ctypes.cast(obj.raw,ctypes.c_void_p).value;result=[]
    for i in range(text.count_chars()):
        if ctypes.cast(pdf.raw.FPDFText_GetTextObject(text,i),ctypes.c_void_p).value!=address:continue
        x,y=ctypes.c_double(),ctypes.c_double()
        assert pdf.raw.FPDFText_GetCharOrigin(text,i,ctypes.byref(x),ctypes.byref(y))
        result.append(dict(char=chr(pdf.raw.FPDFText_GetUnicode(text,i)),origin=[x.value,y.value],bounds_pt=text.get_charbox(i)))
    return result


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);base=json.loads(args.capture.read_text(encoding='utf-8'))
    rows=[];sources={};selections=[('metNote8thUp','character_e'),('kumoSwingSixteenths','first_two'),('kumoSwingTripletEighthSixteenth','after_equals')]
    for name,which in selections:
        previous=base['glyphs'][name];source=Path(previous['source']);sha=hashlib.sha256(source.read_bytes()).hexdigest()
        assert sha==base['sources'][str(source)];sources[str(source)]=sha
        doc=pdf.PdfDocument(source);page=doc[previous['page']-1];text=page.get_textpage()
        objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=objects[previous['object_index']]
        chars=object_characters(text,obj);spelling=''.join(c['char'] for c in chars)
        if which=='character_e':
            assert spelling.startswith('ek');selected=[0];comparison=[0,1]
        elif which=='first_two':
            assert spelling.startswith('ŒÊ');selected=[0,1];comparison=selected
        else:
            at=next(i for i,c in enumerate(chars) if c['char']=='=');selected=[i for i,c in enumerate(chars) if i>at and not c['char'].isspace()];comparison=selected
        assert selected
        all_commands=[];selected_commands=[];pieces=[];rejected=None
        for i,character in enumerate(chars):
            if i not in comparison:continue
            if character['char']==' ':continue
            try:commands=glyph_commands(obj,character['char'])
            except (AssertionError,ValueError) as error:rejected=str(error);break
            commands=displayed_commands(obj,commands,character['origin']);all_commands.extend(commands)
            pieces.append(dict(index=i,**character))
            if i in selected:selected_commands.extend(commands)
        choice=dict(symbol=name,mode=previous['mode'],replace=True)
        record=dict(choice=choice,source=str(source),source_sha256=sha,page=previous['page'],object_indices=[previous['object_index']],
                    source_text=obj.extract(),components=pieces,selected_indices=selected,
                    staff_space_pt=previous['nominal_space_pt'],origin_pt=chars[selected[0]]['origin'],comparison_indices=comparison)
        if rejected:
            record.update(rejected=True,reason=rejected);rows.append(record);text.close();page.close();doc.close();continue
        full=render_object(doc,page,obj,args.scale);fullbox=obj.get_bounds();boxes=[chars[i]['bounds_pt'] for i in comparison]
        box=[min(v[0] for v in boxes),min(v[1] for v in boxes),max(v[2] for v in boxes),max(v[3] for v in boxes)]
        import math
        crop=(math.floor((box[0]-fullbox[0])*args.scale),math.floor((fullbox[3]-box[3])*args.scale),
              math.ceil((box[2]-fullbox[0])*args.scale),math.ceil((fullbox[3]-box[1])*args.scale))
        original=full.crop(crop);paper=Image.new('RGBA',original.size,'white');paper.alpha_composite(original)
        original=tight(paper);all_objects=list(page.get_objects())
        for member in all_objects:assert pdf.raw.FPDFPageObj_SetIsActive(member,False)
        raw=insert_source_component(page,all_commands);a,b,c,d=box;w,h=page.get_size();pad=.1
        bm=page.render(scale=args.scale,crop=(a-pad,b-pad,w-c-pad,h-d-pad));projected=tight(bm.to_pil().copy());bm.close()
        assert pdf.raw.FPDFPage_RemoveObject(page,raw);pdf.raw.FPDFPageObj_Destroy(raw)
        delta=[x-y for x,y in zip(original.size,projected.size)];aa=np.asarray(original.convert('L'))<160;bb=np.asarray(projected.resize(original.size).convert('L'))<160
        iou=float(np.logical_and(aa,bb).sum()/np.logical_or(aa,bb).sum());passed=iou>.97 and all(abs(v)<=3 for v in delta)
        board=Image.new('RGB',(max(original.width,projected.width)+20,original.height+projected.height+70),'white');draw=ImageDraw.Draw(board)
        draw.text((5,5),'Original whole object / complete curve reconstruction: '+name,fill='black');board.paste(original,(5,25));board.paste(projected,(5,original.height+50));board.save(args.output/(name+'.png'))
        record.update(world_commands=selected_commands,verification=dict(passed=passed,delta=delta,ink_iou=iou),
                      rejected=not passed,selection=which,all_world_commands=all_commands,comparison_bounds_pt=box)
        rows.append(record);text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
        print(name,json.dumps(spelling,ensure_ascii=True),'selected',selected,'delta',delta,'IoU',round(iou,6),'passed',passed,flush=True)
    (args.output/'capture.json').write_text(json.dumps(dict(version='0.470',sources=sources,rows=rows),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--scale',type=float,default=64);run(p.parse_args())
