"""Small 0.3 native comparisons plus optional raster-only official shape review.

Reference crops are for local review, never distributed in the font archive.
Only the shape board equalizes glyph heights; native staff crops never rescale
variants individually. Requires Pillow and, with --reference, pypdfium2.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
from review_proofs import opaque

ROOT=Path(__file__).resolve().parent


def run(args):
    proof=args.proofs.resolve();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    native=json.loads((proof/'native-report.json').read_text(encoding='utf-8'))
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    variants=[('leland-control','Leland - renamed control'),('piano','Kumo Piano 0.2 shapes - rejected'),('ex','Kumo Piano EX 0.3')]
    # Same native PNG pixel coordinates and physical scale for all variants.
    for name,box in [('native-heads',(70,235,1430,550)),
                     ('native-rests',(80,640,1430,900)),
                     ('native-flags',(80,1300,1430,1590))]:
        rows=[]
        for key,title in variants:
            crop=opaque(proof/('fixture-'+key+'-1.png')).crop(box)
            row=Image.new('RGB',(crop.width*2,crop.height*2+55),'white')
            row.paste(crop.resize((crop.width*2,crop.height*2)),(0,55))
            ImageDraw.Draw(row).text((12,12),title,font=label,fill='black');rows.append(row)
        board=Image.new('RGB',(rows[0].width,sum(r.height for r in rows)),'white');y=0
        for row in rows:board.paste(row,(0,y));y+=row.height
        board.save(out/(name+'.png'))
    # Full pages are provided separately; do not compare mismatched user bars
    # just because font changes left them at similar page coordinates.
    for key,title in variants:
        opaque(proof/('fixture-'+key+'-1.png')).save(out/('full-'+key+'.png'))
    report=dict(host=native['host'],host_sha256=native['host_sha256'],text='Leland Text',
                native_report=str(proof/'native-report.json'),originals=native['originals'],
                registration_and_style_only_copies=True,fonts_match_native_proofs=True,
                physical_print=False,aesthetic_approval=False,control_pixel_identical=None)
    assert native['text_mode']=='fixed'
    assert all(v['text']=='Leland Text' for v in native['proofs'].values())
    for key,_ in variants:
        assert native['proofs']['fixture-'+key]['pages']==1
        family=native['proofs']['fixture-'+key]['symbol']
        for suffix in ('',' Text'):
            name=family+suffix
            assert (args.fonts/key/name/(name+'.otf')).read_bytes()==(proof/'ScoreFonts'/name/(name+'.otf')).read_bytes()
    a,b=opaque(proof/'fixture-leland-1.png'),opaque(proof/'fixture-leland-control-1.png')
    assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None
    report['control_pixel_identical']=True
    for source,h in native['originals'].items():assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==h
    report['originals_unchanged_during_run']=True
    if args.reference:
        import pypdfium2 as pdf
        d=pdf.PdfDocument(args.reference)
        board=Image.new('RGB',(1800,1000),'white');draw=ImageDraw.Draw(board)
        font_path=args.fonts/'ex/Kumo Piano EX/Kumo Piano EX.otf'
        font=ImageFont.truetype(str(font_path),600)
        items=[(9,11,'Black',0xe0a4),(9,10,'Half',0xe0a3),(9,9,'Whole',0xe0a2),(25,9,'Quarter rest',0xe4e5)]
        for i,(page,row,title,cp) in enumerate(items):
            p=d[page-1];w,h=p.get_size();top=36+row*44
            im=p.render(scale=24,crop=(201,h-(top+44),w-217,top)).to_pil().convert('RGB')
            # Table lines lie near the top/bottom of the symbol cell.
            im=im.crop((0,100,im.width,im.height-35));bb=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox();im=im.crop(bb)
            height=160 if i<3 else 300
            im=im.resize((round(im.width*height/im.height),height));x=i*450
            board.paste(im,(x+(450-im.width)//2,120));draw.text((x+30,30),title,font=label,fill='black')
            tile=Image.new('RGB',(700,900),'white')
            ImageDraw.Draw(tile).text((100,600),chr(cp),font=font,fill='black',anchor='ls')
            bb=ImageChops.difference(tile,Image.new('RGB',tile.size,'white')).getbbox();tile=tile.crop(bb)
            tile=tile.resize((round(tile.width*height/tile.height),height));board.paste(tile,(x+(450-tile.width)//2,620))
        draw.text((20,450),'Top: official Chaconne Ex raster. Bottom: Kumo EX. Equal heights for SHAPE only; native scale is shown separately.',font=label,fill='black')
        board.save(out/'reference-vs-ex-shapes.png')
        report['reference']=dict(path=str(args.reference),sha256=hashlib.sha256(args.reference.read_bytes()).hexdigest(),pages=[9,25],raster_only=True)
    (out/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Native comparisons, font bytes, control pixels and source hashes verified:',out)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--proofs',type=Path,required=True);p.add_argument('--fonts',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--reference',type=Path)
    run(p.parse_args())
