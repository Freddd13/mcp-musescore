"""Expand visual sampling by context, including pages beyond the opening."""
import hashlib,json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent/'dist/reference-expanded'
ROOT.mkdir(parents=True, exist_ok=True)
data=json.loads(Path('docs/engraving/expanded_cases.json').read_text(encoding='utf-8'))
targets={'jazz':[1,2,3,4],'fantasy':[1,4,8],'waltz':[1,7],'mixed':[1,3,5],'kick':[1,5,7],'ghibli':[3,14],'ballad':[2,6],'medley':[40,145]}
report=[];thumbs=[]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for item in data['sources']:
    key=item['id']
    if key not in targets:continue
    file=Path(item['path']);before=hashlib.sha256(file.read_bytes()).hexdigest()
    assert before==item['sha256']
    doc=pdfium.PdfDocument(str(file))
    for page in targets[key]:
        pg=doc[page-1];image=pg.render(scale=3).to_pil().convert('RGB');pg.close()
        image.save(ROOT/('%s-%d.png'%(key,page)))
        image.thumbnail((470,665))
        tile=Image.new('RGB',(490,700),'white');tile.paste(image,(10,30));ImageDraw.Draw(tile).text((10,5),'%s page %d'%(key,page),font=font,fill='black');thumbs.append(tile)
    doc.close();assert hashlib.sha256(file.read_bytes()).hexdigest()==before
    report.append(dict(id=key,path=str(file),sha256=before,pages_review_candidates=targets[key],font_names=item['fonts']))
    print(key,targets[key],flush=True)
for start in range(0,len(thumbs),8):
    selected=thumbs[start:start+8];board=Image.new('RGB',(1960,1400),'white')
    for i,tile in enumerate(selected):board.paste(tile,((i%4)*490,(i//4)*700))
    board.save(ROOT/('contact-%d.png'%(start//8+1)))
(ROOT/'sources.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
