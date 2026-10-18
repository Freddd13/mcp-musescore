"""Compare actual PDF rasters and the seven-glyph local proof at fixed sp scale."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont


def run(args):
    root=args.study;data=json.loads((root/'private-contour-probe.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(Path(data['source']).read_bytes()).hexdigest()==data['sha256']
    board=Image.new('RGB',(2400,1950),'white');draw=ImageDraw.Draw(board)
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',27)
    font=ImageFont.truetype(str(args.font),800)
    draw.text((20,20),'Actual Sincerely PDF: individual objects rendered without the staff/stems',font=label,fill='black')
    draw.text((20,940),'Local contour feasibility study: rendered from the proof OTF',font=label,fill='black')
    for i,name in enumerate(['noteheadBlack','noteheadHalf','noteheadWhole','restQuarter','rest8th']):
        glyph=data['glyphs'][name];x=i*480
        draw.text((x+12,85),name,font=label,fill='black')
        image=Image.open(root/glyph['raster']).convert('RGBA')
        paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image)
        image=paper.convert('RGB');k=200/(data['staff_space_pt']*data['bitmap_scale'])
        image=image.resize((round(image.width*k),round(image.height*k)))
        left=(glyph['bounds_pt'][0]-glyph['origin_pt'][0])*200/data['staff_space_pt']
        top=(glyph['bounds_pt'][3]-glyph['origin_pt'][1])*200/data['staff_space_pt']
        board.paste(image,(round(x+55+left),round(560-top)))
        draw.text((x+55,1480),chr(glyph['codepoint']),font=font,fill='black',anchor='ls')
    draw.text((20,1875),'Both rows: 200 pixels per staff space. Seven glyphs only; raster contour proof, not a complete font.',font=label,fill='black')
    board.save(root/'actual-vs-private-study.png')
    print('Source/proof comparison at the same staff-space scale; source hash checked.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study',type=Path,required=True);p.add_argument('--font',type=Path,required=True)
    run(p.parse_args())
