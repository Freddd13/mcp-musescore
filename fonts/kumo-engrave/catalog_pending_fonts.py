"""Read-only visual catalogue of per-PDF font groups omitted by anchor heuristics.

Full existing text objects are rendered so musical composites are not mistaken
for body text by Unicode names. The catalogue is local reference material.
"""
import argparse,hashlib,json,re
from pathlib import Path
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont,ImageChops


def render_object(doc,page,obj,scale):
    raw=pdf.raw.FPDFTextObj_GetRenderedBitmap(doc,page,obj,scale)
    if not raw:raise ValueError('No rendered bitmap')
    bitmap=pdf.PdfBitmap.from_raw(raw);image=bitmap.to_pil().copy();bitmap.warn_on_close=False;bitmap.close()
    image=image.convert('RGBA')
    if not image.getchannel('A').getbbox():raise ValueError('No ink')
    return image


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    audit=json.loads(args.audit.read_text(encoding='utf-8'));entries=audit['noncandidate_fonts'];files={};docs={};pages={};result=[]
    for serial,entry in enumerate(entries,1):
        score=entry['score']
        if score not in files:files[score]=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        data=files[score];font=data['fonts'][entry['font']];samples={}
        for glyph in font['glyphs'].values():
            for s in glyph['samples']:
                key=(s['page'],s['text_object_index']);samples.setdefault(key,dict(**s,count=glyph['count']))
        ordered=sorted(samples.values(),key=lambda s:(not any(ord(c)>127 for c in s['object_text']),-min(len(s['object_text']),12),-s['count']))
        chosen=[];texts=set()
        for sample in ordered:
            if sample['object_text'] in texts:continue
            chosen.append(sample);texts.add(sample['object_text'])
            if len(chosen)==3:break
        if score not in docs:
            assert hashlib.sha256(Path(data['source_path']).read_bytes()).hexdigest()==data['sha256']
            docs[score]=pdf.PdfDocument(data['source_path'])
        doc=docs[score]
        def get_page(n):
            key=(score,n)
            if key not in pages:
                page=doc[n-1];text=page.get_textpage();pages[key]=(page,text,list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)))
            return pages[key]
        if not chosen:
            for n in range(1,len(doc)+1):
                page,text,objects=get_page(n)
                for i,obj in enumerate(objects):
                    raw_name=obj.get_font().get_base_name();name=re.sub(r'^[A-Z]{6}\+','',raw_name)
                    if name==entry['font']:
                        chosen.append(dict(page=n,text_object_index=i,object_text=obj.extract()));break
                if chosen:break
        row=dict(id='H%03d'%serial,score=score,font=entry['font'],keys=sorted(font['glyphs']),objects=font['objects'],samples=[])
        for i,sample in enumerate(chosen):
            page,text,objects=get_page(sample['page']);obj=objects[sample['text_object_index']]
            record=dict(page=sample['page'],object_index=sample['text_object_index'],text=sample['object_text'],bounds_pt=obj.get_bounds())
            try:
                image=render_object(doc,page,obj,12);name=row['id']+'-%d.png'%i;image.save(args.output/name);record.update(status='ink',image=name)
            except ValueError as error:record.update(status='unrendered',error=str(error))
            row['samples'].append(record)
        result.append(row)
    for score,doc in docs.items():assert hashlib.sha256(Path(files[score]['source_path']).read_bytes()).hexdigest()==files[score]['sha256']
    for page,text,objects in pages.values():text.close();page.close()
    for doc in docs.values():doc.close()
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for start in range(0,len(result),24):
        board=Image.new('RGB',(1800,2040),'white');draw=ImageDraw.Draw(board)
        for i,row in enumerate(result[start:start+24]):
            x=i%4*450;y=i//4*340
            draw.text((x+8,y+8),row['id']+' '+row['score']+' '+row['font'][:25],font=label,fill='black')
            draw.text((x+8,y+32),'keys '+str(len(row['keys']))+' objects '+str(row['objects']),font=label,fill='black')
            for j,s in enumerate(row['samples']):
                if s['status']!='ink':draw.text((x+8,y+65+j*90),'NO INK / '+s.get('error',''),font=label,fill='red');continue
                im=Image.open(args.output/s['image']);paper=Image.new('RGBA',im.size,'white');paper.alpha_composite(im);im=paper.convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
                if box:im=im.crop(box)
                im.thumbnail((420,75));board.paste(im,(x+12,y+65+j*90))
        board.save(args.output/('sheet-%02d.png'%(start//24+1)))
    (args.output/'catalog.json').write_text(json.dumps(dict(groups=result,source_hashes={k:v['sha256'] for k,v in files.items()},note='Rendered full objects for visual classification; no source PDF or font program saved.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Pending font groups',len(result),'sampled objects',sum(len(r['samples']) for r in result),'sources',len(docs),'all hashes unchanged')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--audit',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
