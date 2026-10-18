"""Propose outlined-PDF path matches; keep words/lines and ambiguities visible."""
import argparse,collections,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_corpus_shapes import fingerprint
from source.pdf_symbol_map import GLYPHS,COMPOUNDS


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    index=json.loads((args.atlas/'index.json').read_text(encoding='utf-8'));cat=json.loads(args.catalog.read_text(encoding='utf-8'))
    roles=collections.defaultdict(set)
    for name,aliases,mode in GLYPHS:
        for cp in aliases.split():roles[cp].add(name)
    for cp,names in COMPOUNDS.items():roles[cp].update(names)
    prototypes=[]
    for key,g in cat.items():
        if g['status']!='rendered':continue
        mask,aspect=fingerprint(Image.open(args.catalog.parent/g['image']).convert('RGBA'))
        prototypes.append(dict(key=key,roles=sorted(roles[key.split('U+')[1]]),mask=mask,aspect=aspect))
    masks=np.stack([g['mask'] for g in prototypes]);aspects=np.array([g['aspect'] for g in prototypes]);areas=masks.sum(axis=(1,2))
    fonts={};groups={};failures=[]
    for item in index['items']:
        b=item['bounds_units'];extent=max(b[2]-b[0],b[3]-b[1]);size=512
        while extent*size/1000>1800:size//=2
        error=None
        while size>=1:
            if size not in fonts:fonts[size]=ImageFont.truetype(str(args.atlas/'path-inventory.otf'),size)
            try:raw=fonts[size].getmask(chr(item['unicode']),mode='L');break
            except OSError as e:error=str(e);size//=2
        else:
            failures.append(dict(index=item['index'],page=item['page'],object_index=item['object_index'],error=error));continue
        if not all(raw.size):continue
        im=Image.frombytes('L',raw.size,bytes(raw));rgba=Image.new('RGBA',im.size,'black');rgba.putalpha(im)
        try:mask,aspect=fingerprint(rgba)
        except ValueError:continue
        signature=(mask.tobytes(),round(aspect,3))
        if signature in groups:groups[signature]['occurrences'].append(item);continue
        intersection=np.logical_and(masks,mask).sum(axis=(1,2));union=areas+mask.sum()-intersection
        scores=intersection/np.maximum(union,1)*np.minimum(aspects/aspect,aspect/aspects)**.4;best=np.argsort(-scores)[:3]
        row=dict(id=len(groups),occurrences=[item],matches=[dict(key=prototypes[i]['key'],roles=prototypes[i]['roles'],score=round(float(scores[i]),4)) for i in best])
        filename='path-%04d.png'%row['id'];rgba.save(args.output/filename);row['image']=filename;groups[signature]=row
    rows=sorted(groups.values(),key=lambda g:(-g['matches'][0]['score'],-len(g['occurrences'])))
    for start in range(0,len(rows),24):
        board=Image.new('RGB',(1800,1440),'white');draw=ImageDraw.Draw(board);label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
        for i,g in enumerate(rows[start:start+24]):
            x=i%6*300;y=i//6*360;m=g['matches'][0];s=g['occurrences'][0]
            title='#%d p%d obj%d n%d'%(g['id'],s['page'],s['object_index'],len(g['occurrences']))
            draw.text((x+8,y+7),title,font=label,fill='black');draw.text((x+8,y+32),m['roles'][0] if m['roles'] else '?',font=label,fill='black');draw.text((x+8,y+57),str(m['score'])+' '+m['key'],font=label,fill='black')
            im=Image.open(args.output/g['image']);paper=Image.new('RGBA',im.size,'white');paper.alpha_composite(im);im=paper.convert('RGB');im.thumbnail((250,245));board.paste(im,(x+(300-im.width)//2,y+90))
        board.save(args.output/('sheet-%02d.png'%(start//24+1)))
    report=dict(source=index['source'],sha256=index['sha256'],paths=len(index['items']),unique_groups=len(rows),
                note='Shape proposals only. Even-odd path fill and musical context require verification.',groups=rows,failures=failures)
    (args.output/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Paths',len(index['items']),'unique raster/aspect groups',len(rows),'score >= .9',sum(g['matches'][0]['score']>=.9 for g in rows),'unrendered',len(failures))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--atlas',type=Path,required=True)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
