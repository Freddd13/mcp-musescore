"""Compare final music-font ink to isolated original PDF path components.

Source objects are temporarily activated/deactivated in memory only. Compound
accidentals use reviewed component bounds. Periodic runs use the same physical
clip interval as the cubic construction. No source PDF is written.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageChops,ImageDraw,ImageFont
from source.path_geometry import contours


def insert_source_component(page,commands):
    """Temporary page object from untransformed original contour commands."""
    first=commands[0][1][0];raw=pdf.raw.FPDFPageObj_CreateNewPath(*first);assert raw
    for i,(op,points) in enumerate(commands):
        if op=='moveTo':
            if i:assert pdf.raw.FPDFPath_MoveTo(raw,*points[0])
        elif op=='lineTo':assert pdf.raw.FPDFPath_LineTo(raw,*points[0])
        elif op=='curveTo':assert pdf.raw.FPDFPath_BezierTo(raw,*(v for p in points for v in p))
        elif op=='closePath':assert pdf.raw.FPDFPath_Close(raw)
    assert pdf.raw.FPDFPageObj_SetFillColor(raw,0,0,0,255)
    assert pdf.raw.FPDFPath_SetDrawMode(raw,pdf.raw.FPDF_FILLMODE_WINDING,False)
    pdf.raw.FPDFPage_InsertObject(page,raw)
    return raw


def tight(image):
    image=image.convert('RGB');box=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
    assert box,'Empty glyph';return image.crop(box)


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);data=json.loads(args.capture.read_text(encoding='utf-8'))
    study=data['vector_study'];source=Path(study['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==study['sha256']
    paths=json.loads(args.paths.read_text(encoding='utf-8'));assert paths['sha256']==study['sha256']
    by_key={(v['page'],v['object_index']):v for v in paths['paths']}
    doc=pdf.PdfDocument(source);pages={};fonts={};results=[]
    for row in study['rows']:
        name=row['symbol'];n=row['page']
        if n not in pages:
            page=doc[n-1];objects=list(page.get_objects())
            for obj in objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
            pages[n]=(page,objects)
        page,objects=pages[n];indices=row.get('object_indices',[row.get('object_index')])
        temporary=None
        if row.get('component'):
            parts=contours(by_key[(n,row['object_index'])]['commands'])
            commands=[c for i in row['source_contour_indices'] for c in parts[i]]
            temporary=insert_source_component(page,commands)
        else:
            for index in indices:assert pdf.raw.FPDFPageObj_SetIsActive(objects[index],True)
        a,b,c,d=row.get('source_clip_bounds_pt',row['source_bounds_pt']);pad=0 if row.get('source_clip_bounds_pt') else .04
        a-=pad;b-=pad;c+=pad;d+=pad;w,h=page.get_size()
        bitmap=page.render(scale=args.scale,crop=(a,b,w-c,h-d));original=bitmap.to_pil().copy().convert('RGB');bitmap.close()
        for index in indices:assert pdf.raw.FPDFPageObj_SetIsActive(objects[index],False)
        if temporary:
            assert pdf.raw.FPDFPage_RemoveObject(page,temporary)
            pdf.raw.FPDFPageObj_Destroy(temporary)
        if row.get('rotate_clockwise'):original=original.transpose(Image.Transpose.ROTATE_270)
        if row.get('reflect_y'):original=original.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        original=tight(original)
        size=round(4*row['staff_space_pt']*row['render_scale']*args.scale)
        if size not in fonts:fonts[size]=ImageFont.truetype(str(args.font),size)
        mask=fonts[size].getmask(chr(data['glyphs'][name]['codepoint']),mode='L');alpha=Image.frombytes('L',mask.size,bytes(mask))
        glyph=Image.new('RGBA',alpha.size,'black');glyph.putalpha(alpha);paper=Image.new('RGBA',alpha.size,'white');paper.alpha_composite(glyph);converted=tight(paper)
        delta=[original.width-converted.width,original.height-converted.height]
        # The periodic body intentionally quantizes its advance to an integer
        # font unit. Account for that recorded x scale before checking raster
        # bounds; do not mistake it for conversion drift.
        period_ratio=(data['glyphs'][name]['advance']/(row['source_period_pt']/row['staff_space_pt']*250)) if row.get('source_period_pt') else 1
        expected_size=[round(original.width*period_ratio),original.height]
        compensated_delta=[a-b for a,b in zip(expected_size,converted.size)]
        aligned=converted.resize(original.size);a0=np.asarray(original.convert('L'))<160;b0=np.asarray(aligned.convert('L'))<160
        iou=float(np.logical_and(a0,b0).sum()/np.logical_or(a0,b0).sum())
        filename=name+'.png';board=Image.new('RGB',(max(original.width,converted.width)+40,original.height+converted.height+100),'white')
        draw=ImageDraw.Draw(board);draw.text((10,5),'Actual PDF / '+name,fill='black');board.paste(original,(15,30))
        draw.text((10,original.height+50),'Final OTF / original curves',fill='black');board.paste(converted,(15,original.height+75));board.save(args.output/filename)
        results.append(dict(symbol=name,source_size=original.size,font_size=converted.size,delta=delta,ink_iou=iou,image=filename,
            period_scale_ratio=period_ratio,compensated_delta=compensated_delta,
            passed=all(abs(v)<=3 for v in compensated_delta) and iou>.94))
        print(name,'delta',delta,'IoU',round(iou,5),flush=True)
    for page,objects in pages.values():page.close()
    doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==study['sha256']
    report=dict(source=str(source),source_sha256=study['sha256'],source_unchanged=True,font=str(args.font),
        font_sha256=hashlib.sha256(args.font.read_bytes()).hexdigest(),capture_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest(),rows=results)
    (args.output/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    failed=[r for r in results if not r['passed']];assert not failed,[(r['symbol'],r['delta'],r['ink_iou']) for r in failed]
    print('All',len(results),'source-path comparisons passed; source hash unchanged.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--font',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--paths',type=Path,required=True)
    p.add_argument('--scale',type=float,default=64);run(p.parse_args())
