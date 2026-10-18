"""Compare original outlined PDF paths and the diagnostic CFF rendering.

Other page objects are temporarily inactive in memory only. No PDF is saved.
This verifies geometry conversion, not automatic musical-role identification.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont,ImageChops
from source.pdf_symbol_map import GLYPHS


def tight(im):
    im=im.convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
    if not box:raise ValueError('Empty path rendering')
    return im.crop(box)


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    atlas=json.loads((args.atlas/'index.json').read_text(encoding='utf-8'));review=json.loads(args.review.read_text(encoding='utf-8'))
    source=Path(atlas['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==atlas['sha256']
    selected={};allowed={g[0] for g in GLYPHS}
    for g in review['groups']:
        m=g['matches'][0]
        # Rectangles and circular dots have ambiguous musical roles. Select
        # curving candidates for the conversion check; keep role as provisional.
        if m['score']<.90 or len(m['roles'])!=1 or m['roles'][0] not in allowed:continue
        role=m['roles'][0];s=g['occurrences'][0]
        if not s['curves'] or role in selected:continue
        selected[role]=s
    doc=pdf.PdfDocument(source);pages={};font=ImageFont.truetype(str(args.atlas/'path-inventory.otf'),512);rows=[]
    for role,item in selected.items():
        n=item['page']
        if n not in pages:
            page=doc[n-1];objects=list(page.get_objects())
            for obj in objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
            pages[n]=(page,objects)
        page,objects=pages[n];obj=objects[item['object_index']];assert pdf.raw.FPDFPageObj_SetIsActive(obj,True)
        a,b,c,d=item['bounds_pt'];w,h=page.get_size();a=max(0,a-1);b=max(0,b-1);c=min(w,c+1);d=min(h,d+1)
        scale=128/item['calibration']['staff_space_pt'];bitmap=page.render(scale=scale,crop=(a,b,w-c,h-d))
        original=tight(bitmap.to_pil().copy());bitmap.close();assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
        mask=font.getmask(chr(item['unicode']),mode='L');alpha=Image.frombytes('L',mask.size,bytes(mask));glyph=Image.new('RGBA',alpha.size,'black');glyph.putalpha(alpha)
        paper=Image.new('RGBA',alpha.size,'white');paper.alpha_composite(glyph);converted=tight(paper)
        delta=[original.width-converted.width,original.height-converted.height]
        # Different rasterizers can differ by a boundary pixel. A same-size
        # comparison is still recorded, rather than claiming byte identity.
        aligned=converted.resize(original.size);a0=np.asarray(original.convert('L'))<160;b0=np.asarray(aligned.convert('L'))<160
        iou=float(np.logical_and(a0,b0).sum()/np.logical_or(a0,b0).sum())
        filename='path-%s.png'%role;board=Image.new('RGB',(max(original.width,converted.width)+30,original.height+converted.height+90),'white')
        draw=ImageDraw.Draw(board);draw.text((5,3),'PDF path / '+role,fill='black');board.paste(original,(10,25));draw.text((5,original.height+35),'CFF cubic conversion',fill='black');board.paste(converted,(10,original.height+60));board.save(args.output/filename)
        rows.append(dict(role_candidate=role,page=n,object_index=item['object_index'],curves=item['curves'],
            fill_mode=item['fill_mode'],original_size=original.size,converted_size=converted.size,boundary_delta=delta,shape_iou=iou,image=filename))
    for page,objects in pages.values():page.close()
    doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==atlas['sha256']
    (args.output/'verification.json').write_text(json.dumps(dict(source=str(source),sha256=atlas['sha256'],rows=rows,source_unchanged=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Original path/CFF comparisons',len(rows),'IoU range',min(v['shape_iou'] for v in rows),max(v['shape_iou'] for v in rows),'original hash unchanged')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--atlas',type=Path,required=True)
    p.add_argument('--review',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
