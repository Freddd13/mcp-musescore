"""Suggest existing reviewed shape groups for actual-resource representatives.

The generated links and scores are review aids. Human approval is recorded
separately; neither similarity nor same Unicode certifies a musical purpose.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image,ImageDraw,ImageFont
from catalog_corpus_keys import POPCOUNT,signature
from source.reviewed_corpus_keys import CATALOG_SHA,roles

ROOT=Path(__file__).resolve().parent
RESOURCE_SHA='1cb99cba0955391ff1f4d962a34b35d2132e7cd4e519577153d4b3f811dad2d6'


def run(args):
    assert hashlib.sha256(args.resources.read_bytes()).hexdigest()==RESOURCE_SHA
    assert hashlib.sha256(args.baseline.read_bytes()).hexdigest()==CATALOG_SHA
    data=json.loads(args.resources.read_text(encoding='utf-8'))
    baseline=json.loads(args.baseline.read_text(encoding='utf-8'))
    args.output.mkdir(parents=True,exist_ok=False)
    rows={r['id']:r for r in data['rows']};old_rows={r['id']:r for r in baseline['rows']}
    old=[]
    for group in baseline['groups']:
        row=old_rows[group['representative']]
        old.append((group,signature(Image.open(args.baseline.parent/row['image'])),row))
    masks=np.stack([s[0] for g,s,r in old]);areas=np.array([s[1] for g,s,r in old]);aspects=np.array([s[2] for g,s,r in old])
    decisions=roles();proposals=[]
    for group in data['groups']:
        row=rows[group['representative']]
        mask,area,aspect=signature(Image.open(args.resources.parent/row['image']))
        overlap=POPCOUNT[np.bitwise_and(masks,mask)].sum(axis=1)
        scores=overlap/np.maximum(areas+area-overlap,1)*np.minimum(aspects/aspect,aspect/aspects)**.4
        indices=np.argsort(-scores)[:3]
        matches=[dict(group=old[int(i)][0]['id'],score=float(scores[int(i)]),
                      symbols=decisions[old[int(i)][0]['id']],image=old[int(i)][2]['image']) for i in indices]
        proposals.append(dict(group=group['id'],representative=row['id'],resource=row['resource'],
                              font=row['font'],raw_name=row['raw_name'],unicode=row['unicode'],
                              image=row['image'],sample=row['sample'],matches=matches))
    low=[p for p in proposals if p['matches'][0]['score']<.96]
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for start in range(0,len(low),12):
        board=Image.new('RGB',(1800,1560),'white');draw=ImageDraw.Draw(board)
        for i,row in enumerate(low[start:start+12]):
            x,y=i%3*600,i//3*390;best=row['matches'][0]
            draw.text((x+5,y+5),'%s -> %s %.3f'%(row['group'],best['group'],best['score']),font=label,fill='black')
            draw.text((x+5,y+29),row['resource']+' '+row['unicode'],font=label,fill='black')
            draw.text((x+5,y+53),' '.join(best['symbols'])[:54],font=label,fill='black')
            for j,path in enumerate((args.resources.parent/row['image'],args.baseline.parent/best['image'])):
                im=Image.open(path).convert('RGB');im.thumbnail((270,270));board.paste(im,(x+j*300+10,y+92))
        board.save(args.output/('differences-%02d.png'%(start//12+1)))
    result=dict(resources_sha256=RESOURCE_SHA,baseline_sha256=CATALOG_SHA,proposals=proposals,
                representatives=len(proposals),low_similarity_groups=len(low),semantic_roles_certified=False)
    (args.output/'matches.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Resource representatives',len(proposals),'below .96 similarity',len(low))
    for p in low:print(p['group'],p['resource'],p['unicode'],p['matches'][0]['group'],round(p['matches'][0]['score'],4),' '.join(p['matches'][0]['symbols']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--resources',type=Path,default=ROOT/'dist/font-resources-194/resources.json')
    p.add_argument('--baseline',type=Path,default=ROOT/'dist/all-candidate-keys-186/catalog.json')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
