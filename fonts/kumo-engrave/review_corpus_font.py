"""White-paper previews and native dynamics-shaping comparisons."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
import numpy as np
from source.pdf_symbol_map import LIGATURES


def opaque(path):
    image=Image.open(path).convert('RGBA');paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image)
    return paper.convert('RGB')


def run(args):
    for path in args.proofs.glob('*-[0-9].png'):
        opaque(path).save(path.with_name(path.stem+'-white.png'))
    dynamics=args.proofs/'dynamics-shaping-1.png'
    if dynamics.exists():
        image=opaque(dynamics);gray=np.asarray(image.convert('L'));scale=200/25.4
        # Authored Text offsets are mm. Native glyph rows are separated by
        # 18 mm; compare left/right shapes at native scale after tight crop.
        ink=(gray[:,int(10*scale):int(60*scale)]<160).any(axis=1)
        runs=[]
        for y in np.flatnonzero(ink):
            if not runs or y-runs[-1][-1]>12:runs.append([int(y)])
            else:runs[-1].append(int(y))
        assert len(runs)>=len(LIGATURES),'Native dynamics page is empty or missing rows'
        rows=[]
        for (target,parts),run in zip(LIGATURES,runs[:len(LIGATURES)]):
            y0,y1=run[0]-3,run[-1]+4
            a=image.crop((int(10*scale),y0,int(60*scale),y1))
            b=image.crop((int(90*scale),y0,int(140*scale),y1))
            aa=ImageChops.difference(a,Image.new('RGB',a.size,'white')).getbbox()
            bb=ImageChops.difference(b,Image.new('RGB',b.size,'white')).getbbox()
            assert aa and bb,target
            a=a.crop(aa).convert('L');b=b.crop(bb).convert('L')
            assert abs(a.width-b.width)<=1 and abs(a.height-b.height)<=1,(target,a.size,b.size)
            b=b.resize(a.size);ma=np.asarray(a)<160;mb=np.asarray(b)<160
            iou=float(np.logical_and(ma,mb).sum()/np.logical_or(ma,mb).sum())
            assert iou>.90,(target,iou)
            rows.append(dict(target=target,shape_iou=iou,left=a.size,right=b.size))
        (args.proofs/'dynamics-pixel-check.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    # Page content is positioned by actual native output, not separately fit
    # for different font candidates.
    if not (args.proofs/'palette-control-1.png').exists():return
    images=[opaque(args.proofs/('palette-'+v+'-1.png')) for v in ['control','study']]
    board=Image.new('RGB',(images[0].width,1200),'white');label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    for i,(image,title) in enumerate(zip(images,['Leland renamed control','Observed PDF shapes / local Study'])):
        board.paste(image.crop((0,200,image.width,750)),(0,i*600+50))
        ImageDraw.Draw(board).text((20,i*600+10),title,font=label,fill='black')
    board.save(args.proofs/'native-first-systems.png')
    print('White-paper native previews written; no reference/source PDFs changed.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--proofs',type=Path,required=True)
    run(p.parse_args())
