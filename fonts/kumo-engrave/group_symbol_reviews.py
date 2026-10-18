"""Group every retained coverage-review image for visual role review.

Grouping is geometric only. Circular marks or identical digits can have several
musical roles; member coordinates and proposed roles remain available and no
group is certified automatically. No reference PDF needs reopening here.
"""
import argparse,collections,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_corpus_shapes import fingerprint


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    audit=json.loads((args.audit/'audit.json').read_text(encoding='utf-8'))
    groups=[];masks=[];aspects=[];areas=[]
    for index,row in enumerate(audit['rows']):
        if not row.get('review_image'):continue
        mask,aspect=fingerprint(Image.open(args.audit/row['review_image']).convert('RGBA'))
        best=None;score=0
        if groups:
            mm=np.stack(masks);intersection=np.logical_and(mm,mask).sum(axis=(1,2));union=np.asarray(areas)+mask.sum()-intersection
            similarity=intersection/np.maximum(union,1)
            similarity*=np.minimum(np.asarray(aspects)/aspect,aspect/np.asarray(aspects))**.4
            at=int(np.argmax(similarity));score=float(similarity[at])
            if score>=args.minimum:best=groups[at]
        member=dict(audit_row=index,**row)
        if best is None:
            best=dict(id='G%03d'%(len(groups)+1),representative=row['review_image'],members=[],minimum_similarity=1)
            groups.append(best);masks.append(mask);aspects.append(aspect);areas.append(mask.sum())
        else:best['minimum_similarity']=min(best['minimum_similarity'],score)
        best['members'].append(member)
    for group in groups:
        group['proposals']=dict(collections.Counter(m['matches'][0]['name'] for m in group['members']))
        group['scores']=sorted({m['score'] for m in group['members']})
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(groups),24):
        board=Image.new('RGB',(1800,1560),'white');draw=ImageDraw.Draw(board)
        for i,group in enumerate(groups[start:start+24]):
            x=i%6*300;y=i//6*390;m=group['members'][0]
            draw.text((x+5,y+5),group['id']+' n'+str(len(group['members']))+' '+m['score']+' '+m['unicode'],font=font,fill='black')
            label=' / '.join(group['proposals'])
            for j in range(3):draw.text((x+5,y+28+19*j),label[j*31:(j+1)*31],font=font,fill='black')
            image=Image.open(args.audit/group['representative']).convert('RGBA');paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image);image=paper.convert('RGB')
            image.thumbnail((260,250));board.paste(image,(x+(300-image.width)//2,y+100))
            draw.text((x+5,y+365),'sources '+str(len(group['scores'])),font=font,fill='black')
        board.save(args.output/('groups-%02d.png'%(start//24+1)))
    result=dict(note='All retained review rows represented; geometry grouping is not semantic certification.',
        threshold=args.minimum,review_rows=sum(len(g['members']) for g in groups),groups=groups)
    assert result['review_rows']==len(audit['review_files'])
    (args.output/'groups.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Retained rows',result['review_rows'],'groups',len(groups),'contact sheets',(len(groups)+23)//24)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--minimum',type=float,default=.88);run(p.parse_args())
