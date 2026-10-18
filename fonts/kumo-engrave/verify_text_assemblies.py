"""Compare mixed-text source ink with final OTF contours at fixed physical scale.

Only translation restores the selected character's original position. No fitting
or resizing hides scale errors; unselected comparison characters stay original.
Source PDFs are changed in memory only and their hashes are checked afterwards.
"""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw
from capture_text_assemblies import object_characters
from source.pdf_glyph_geometry import glyph_commands,displayed_commands
from verify_vector_font import insert_source_component,tight
from catalog_pending_fonts import render_object


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'));export=json.loads(args.curves.read_text(encoding='utf-8'))
    assert export['capture_sha256']==hashlib.sha256(args.capture.read_bytes()).hexdigest()
    assert export['font_sha256']==hashlib.sha256(args.font.read_bytes()).hexdigest()
    final={r['symbol']:r for r in export['rows']};results=[]
    for row in data['rows']:
        if row.get('rejected'):continue
        name=row['choice']['symbol'];shape=final[name];source=Path(row['source']);sha=hashlib.sha256(source.read_bytes()).hexdigest()
        assert sha==row['source_sha256'];doc=pdf.PdfDocument(source);page=doc[row['page']-1];text=page.get_textpage()
        objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=objects[row['object_indices'][0]]
        assert obj.extract()==row['source_text'];chars=object_characters(text,obj)
        full=render_object(doc,page,obj,args.scale);fb=obj.get_bounds();a,b,c,d=row['comparison_bounds_pt']
        crop=(math.floor((a-fb[0])*args.scale),math.floor((fb[3]-d)*args.scale),
              math.ceil((c-fb[0])*args.scale),math.ceil((fb[3]-b)*args.scale))
        original=full.crop(crop);paper=Image.new('RGBA',original.size,'white');paper.alpha_composite(original);original=tight(paper)
        factor=row['staff_space_pt']/250;sb=shape['source_selected_bounds_pt'];ob=shape['bounds']
        dx=sb[0]-ob[0]*factor;dy=sb[1]-ob[1]*factor
        commands=[[op,[[x*factor+dx,y*factor+dy] for x,y in pts]] for op,pts in shape['commands']]
        for i in row['comparison_indices']:
            if i in row['selected_indices'] or chars[i]['char'].isspace():continue
            commands.extend(displayed_commands(obj,glyph_commands(obj,chars[i]['char']),chars[i]['origin']))
        for member in page.get_objects():assert pdf.raw.FPDFPageObj_SetIsActive(member,False)
        temp=insert_source_component(page,commands);w,h=page.get_size();pad=.1
        bitmap=page.render(scale=args.scale,crop=(a-pad,b-pad,w-c-pad,h-d-pad));converted=tight(bitmap.to_pil().copy());bitmap.close()
        assert pdf.raw.FPDFPage_RemoveObject(page,temp);pdf.raw.FPDFPageObj_Destroy(temp)
        delta=[x-y for x,y in zip(original.size,converted.size)];aa=np.asarray(original.convert('L'))<160;bb=np.asarray(converted.resize(original.size).convert('L'))<160
        iou=float(np.logical_and(aa,bb).sum()/np.logical_or(aa,bb).sum())
        shape_delta=[(ob[2]-ob[0])*factor-(sb[2]-sb[0]),(ob[3]-ob[1])*factor-(sb[3]-sb[1])]
        passed=iou>.97 and all(abs(v)<=3 for v in delta) and all(abs(v)<.001 for v in shape_delta)
        board=Image.new('RGB',(max(original.width,converted.width)+20,original.height+converted.height+70),'white')
        ImageDraw.Draw(board).text((5,5),'Actual PDF / final OTF + unchanged neighbours: '+name,fill='black')
        board.paste(original,(5,25));board.paste(converted,(5,original.height+50));board.save(args.output/(name+'.png'))
        results.append(dict(symbol=name,passed=passed,delta=delta,ink_iou=iou,physical_size_delta_pt=shape_delta,source=str(source),source_sha256=sha))
        print(name,'delta',delta,'IoU',round(iou,6),'passed',passed,flush=True)
        text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
    (args.output/'verification.json').write_text(json.dumps(dict(font_sha256=export['font_sha256'],rows=results),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert all(r['passed'] for r in results)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('capture','curves','font','output'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--scale',type=float,default=64);run(p.parse_args())
