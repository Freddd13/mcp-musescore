"""Collapse outlined-page atlas duplicates and recover skipped native paths.

Recovery renders actual PDF objects in memory, not the diagnostic atlas font
that overflowed. Counts account for every input path. These are silhouette
groups for visual review, never automatic musical-role certification.
"""
import argparse,collections,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont,ImageOps
from audit_corpus_shapes import fingerprint


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    atlas=json.loads((args.review/'review.json').read_text(encoding='utf-8'));paths=json.loads(args.paths.read_text(encoding='utf-8'))
    assert atlas['sha256']==paths['sha256'];source=Path(paths['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==paths['sha256']
    rows=[];represented=set()
    for group in atlas['groups']:
        rows.append(dict(image=args.review/group['image'],members=group['occurrences'],proposals=group['matches']))
        represented.update((v['page'],v['object_index']) for v in group['occurrences'])
    missing=[r for r in paths['paths'] if (r['page'],r['object_index']) not in represented]
    recovered=[];empty=[];doc=pdf.PdfDocument(source);pages={}
    for item in missing:
        n=item['page']
        if n not in pages:
            page=doc[n-1];objects=list(page.get_objects())
            for obj in objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
            pages[n]=(page,objects)
        page,objects=pages[n];obj=objects[item['object_index']];assert obj.type==pdf.raw.FPDF_PAGEOBJ_PATH
        assert pdf.raw.FPDFPageObj_SetIsActive(obj,True)
        a,b,c,d=item['bounds_pt'];w,h=page.get_size();a=max(0,a-.1);b=max(0,b-.1);c=min(w,c+.1);d=min(h,d+.1)
        scale=min(32,1200/max(c-a,d-b));bm=page.render(scale=scale,crop=(a,b,w-c,h-d))
        image=bm.to_pil().copy().convert('RGB');bm.close();assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
        filename='recovered-p%d-%d.png'%(n,item['object_index']);image.save(args.output/filename)
        member=dict(page=n,object_index=item['object_index'],bounds_pt=item['bounds_pt'],recovered_from_actual_pdf=True)
        try:fingerprint(image)
        except ValueError:
            low,high=image.convert('L').getextrema();member['original_luma_range']=[low,high]
            if low==high:
                empty.append(member);continue
            # A low-contrast antialiased line is visible ink, not an empty path.
            # Keep its actual render; stretch only the separate review thumbnail.
            image=ImageOps.autocontrast(image);fingerprint(image)
            filename='review-contrast-p%d-%d.png'%(n,item['object_index']);image.save(args.output/filename)
            member['review_contrast_stretched']=True
        rows.append(dict(image=args.output/filename,members=[member],proposals=[]));recovered.append(member)
    for page,objects in pages.values():page.close()
    doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==paths['sha256']
    groups=[];masks=[];aspects=[];areas=[]
    for row in sorted(rows,key=lambda r:-len(r['members'])):
        image=Image.open(row['image'])
        # Diagnostic glyph images are black with alpha; recovered pages are opaque.
        mask,aspect=fingerprint(image.convert('RGBA') if image.mode=='RGBA' else image.convert('RGB'))
        best=None;score=0
        if groups:
            mm=np.stack(masks);intersection=np.logical_and(mm,mask).sum(axis=(1,2));union=np.asarray(areas)+mask.sum()-intersection
            scores=intersection/np.maximum(union,1)*np.minimum(np.asarray(aspects)/aspect,aspect/np.asarray(aspects))**.4
            at=int(np.argmax(scores));score=float(scores[at])
            if score>=args.minimum:best=groups[at]
        if best is None:
            best=dict(id='P%03d'%(len(groups)+1),image=str(row['image'].resolve()),members=[],proposals=[],minimum_similarity=1)
            groups.append(best);masks.append(mask);aspects.append(aspect);areas.append(mask.sum())
        else:best['minimum_similarity']=min(best['minimum_similarity'],score)
        best['members'].extend(row['members']);best['proposals'].extend(row['proposals'][:1])
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for start in range(0,len(groups),36):
        board=Image.new('RGB',(1800,1800),'white');draw=ImageDraw.Draw(board)
        for i,g in enumerate(groups[start:start+36]):
            x=i%6*300;y=i//6*300;v=g['members'][0]
            draw.text((x+4,y+5),'%s n%d p%d o%d'%(g['id'],len(g['members']),v['page'],v['object_index']),font=font,fill='black')
            labels=collections.Counter('/'.join(p['roles']) or '?' for p in g['proposals'])
            draw.text((x+4,y+27),labels.most_common(1)[0][0][:30] if labels else 'Recovered actual PDF',font=font,fill='black')
            im=Image.open(g['image']).convert('RGBA');paper=Image.new('RGBA',im.size,'white');paper.alpha_composite(im);im=paper.convert('RGB');im.thumbnail((265,235));board.paste(im,(x+(300-im.width)//2,y+58))
        board.save(args.output/('groups-%02d.png'%(start//36+1)))
    count=sum(len(g['members']) for g in groups);assert count+len(empty)==len(paths['paths'])
    output=dict(note='Every source path accounted; grouping/proposals do not certify roles.',source=str(source),sha256=paths['sha256'],
                input_paths=len(paths['paths']),represented_paths=count,recovered_paths=len(recovered),
                no_visible_ink_at_recorded_scale=empty,groups=groups)
    (args.output/'groups.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Paths',len(paths['paths']),'rendered',count,'recovered',len(recovered),'no visible ink at recorded scale',len(empty),'groups',len(groups),'sheets',math.ceil(len(groups)/36))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--review',type=Path,required=True);p.add_argument('--paths',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--minimum',type=float,default=.88);run(p.parse_args())
