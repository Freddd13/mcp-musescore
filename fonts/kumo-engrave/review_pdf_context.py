"""Read-only page context for atlas samples; PDF crop is left,bottom,right,top."""
import argparse,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont


def run(args):
    catalog=json.loads(args.catalog.read_text(encoding='utf-8'))
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
    rows=(len(args.keys)+1)//2
    board=Image.new('RGB',(1900,rows*500),'white');draw=ImageDraw.Draw(board)
    for i,key in enumerate(args.keys):
        glyph=catalog[key];sample=glyph['sample'];source=Path(sample['source'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==sample['sha256']
        doc=pdf.PdfDocument(source);page=doc[sample['page']-1];w,h=page.get_size()
        a,b,c,d=glyph['bounds_pt'];a=max(0,a-38);c=min(w,c+38);b=max(0,b-24);d=min(h,d+24)
        bitmap=page.render(scale=7,crop=(a,b,w-c,h-d))
        image=bitmap.to_pil().copy();bitmap.close();image.thumbnail((900,420))
        x=i%2*950;y=i//2*500
        draw.text((x+8,y+10),key+' '+sample['score']+' p'+str(sample['page']),font=label,fill='black')
        board.paste(image,(x,y+45));page.close();doc.close()
    board.save(args.output)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('keys',nargs='+');run(p.parse_args())
