"""Compare repeated-wave source interiors with the installed-format OTF ink."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageChops,ImageDraw,ImageFont


def tight(image):
    image=image.convert('RGB');b=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
    assert b;return image.crop(b)


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads((args.capture/'capture.json').read_text(encoding='utf-8'));rows=[]
    for row in data['wave_study']:
        name=row['symbol'];image=Image.open(args.capture/(name+'-source-union.png')).convert('RGB')
        a,b,c,d=row['source_render_bounds_pt'];lo,hi=row['source_clip_interval_pt'];s=row['bitmap_scale']
        if row['source_clip_axis']==0:
            image=image.crop((round((lo-a)*s),0,round((hi-a)*s),image.height))
        else:
            image=image.crop((0,round((d-hi)*s),image.width,round((d-lo)*s))).transpose(Image.Transpose.ROTATE_270)
        original=tight(image);item=data['glyphs'][name]
        font=ImageFont.truetype(str(args.font),round(4*row['nominal_space_pt']*s))
        mask=font.getmask(chr(item['codepoint']),mode='L');alpha=Image.frombytes('L',mask.size,bytes(mask))
        rendered=Image.new('RGBA',alpha.size,'black');rendered.putalpha(alpha)
        paper=Image.new('RGBA',alpha.size,'white');paper.alpha_composite(rendered);converted=tight(paper)
        assert abs(original.width-converted.width)<=3 and abs(original.height-converted.height)<=3,(name,original.size,converted.size)
        aligned=converted.resize(original.size);ma=np.asarray(original.convert('L'))<160;mb=np.asarray(aligned.convert('L'))<160
        iou=float(np.logical_and(ma,mb).sum()/np.logical_or(ma,mb).sum());assert iou>.94,(name,iou)
        board=Image.new('RGB',(max(original.width,converted.width)+40,original.height+converted.height+100),'white')
        draw=ImageDraw.Draw(board);draw.text((10,5),'Source periodic interior / '+name,fill='black');board.paste(original,(15,30))
        draw.text((10,original.height+50),'Built OTF',fill='black');board.paste(converted,(15,original.height+75));board.save(args.output/(name+'.png'))
        rows.append(dict(symbol=name,source_size=original.size,font_size=converted.size,ink_iou=iou,source_period_sp=row['source_period_sp']))
    result=dict(font=str(args.font),font_sha256=hashlib.sha256(args.font.read_bytes()).hexdigest(),
        capture_sha256=hashlib.sha256((args.capture/'capture.json').read_bytes()).hexdigest(),rows=rows)
    (args.output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(rows))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--font',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
