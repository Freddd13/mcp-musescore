"""Compare final OTF ink to original displayed characters and source assemblies.

The expected physical scale comes from each declared calibration, not resizing
the glyph to conceal size errors. Tight-resize is used only for raster IoU;
independent unresized dimensions must also agree within three pixels.
"""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont
from catalog_pdf_glyphs import render_character
from verify_vector_font import tight


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'));raw=json.loads(args.observed.read_text(encoding='utf-8'))
    catalog=json.loads(args.catalog.read_text(encoding='utf-8'));spec=json.loads(args.spec.read_text(encoding='utf-8'));results=[];sources={}
    candidates=[r for r in raw['rows'] if not r.get('rejected') and not r['choice'].get('capture_only')]
    for r in list(candidates):
        for derived in spec['derived']:
            if derived.get('reflect_y') and derived['from']==r['choice']['symbol']:
                candidates.append(dict(r,choice=derived,reflect_y=True))
    for row in candidates:
        choice=row['choice'];name=choice['symbol'];source=Path(row['source']);sha=hashlib.sha256(source.read_bytes()).hexdigest()
        assert sha==row['source_sha256'];sources[str(source)]=sha
        doc=pdf.PdfDocument(source);page=doc[row['page']-1];text=page.get_textpage()
        objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text))
        if row.get('world_commands'):
            members=[objects[i] for i in row['object_indices']]
            all_objects=list(page.get_objects())
            for obj in all_objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
            boxes=[]
            for obj in members:
                assert obj.level==0;assert pdf.raw.FPDFPageObj_SetIsActive(obj,True);boxes.append(obj.get_bounds())
            a=min(b[0] for b in boxes)-.1;b=min(b[1] for b in boxes)-.1;c=max(b[2] for b in boxes)+.1;d=max(b[3] for b in boxes)+.1
            w,h=page.get_size();bitmap=page.render(scale=args.scale,crop=(a,b,w-c,h-d));original=tight(bitmap.to_pil().copy());bitmap.close()
        else:
            context=catalog[choice['group']];sample=context['sample']
            assert context['char']==row['char'] and sample['source']==str(source)
            assert sample['page']==row['page'] and sample['text_object_index']==row['object_index']
            obj=objects[row['object_index']];image,box,origin=render_character(doc,page,text,obj,row['char'],args.scale)
            paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image);original=tight(paper)
        if row.get('reflect_y'):original=original.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if choice.get('calibration')=='nominal':
            matrix=row['matrix'];size=math.hypot(matrix[0],matrix[1])*row['font_size']*args.scale
        else:size=4*row['staff_space_pt']*args.scale
        font=ImageFont.truetype(str(args.font),round(size));mask=font.getmask(chr(data['glyphs'][name]['codepoint']),mode='L')
        alpha=Image.frombytes('L',mask.size,bytes(mask));image=Image.new('RGBA',alpha.size,'black');image.putalpha(alpha)
        paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image);converted=tight(paper)
        delta=[a-b for a,b in zip(original.size,converted.size)]
        a0=np.asarray(original.convert('L'))<160;b0=np.asarray(converted.resize(original.size).convert('L'))<160
        iou=float(np.logical_and(a0,b0).sum()/np.logical_or(a0,b0).sum());passed=iou>.94 and all(abs(v)<=3 for v in delta)
        board=Image.new('RGB',(original.width+converted.width+50,max(original.height,converted.height)+40),'white')
        ImageDraw.Draw(board).text((5,5),'Actual PDF / final OTF: '+name,fill='black');board.paste(original,(5,30));board.paste(converted,(original.width+25,30));board.save(args.output/(name+'.png'))
        results.append(dict(symbol=name,source_size=original.size,font_size=converted.size,delta=delta,ink_iou=iou,passed=passed))
        print(name,'delta',delta,'IoU',round(iou,5),flush=True)
        text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
    report=dict(font_sha256=hashlib.sha256(args.font.read_bytes()).hexdigest(),capture_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest(),
                source_hashes_unchanged=sources,rows=results)
    (args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    assert all(r['passed'] for r in results),[(r['symbol'],r['delta'],r['ink_iou']) for r in results if not r['passed']]
    print('All',len(results),'original source / final OTF comparisons passed')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('capture','observed','catalog','spec','font','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--scale',type=float,default=64);run(p.parse_args())
