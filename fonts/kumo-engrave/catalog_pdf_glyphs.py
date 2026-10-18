"""Raster atlas of observed glyphs, including characters inside mixed strings.

The images and sampled geometry are local study data. No PDF or FontFile is
saved. Atlas cells are fitted for identification; capture metadata retains the
actual source bounds, baseline and measured staff size for later font work.
"""
import argparse,ctypes,hashlib,json,math
from pathlib import Path
import pypdfium2 as pdf
from PIL import Image,ImageChops,ImageDraw,ImageFont


def char_location(text,obj,char):
    address=ctypes.cast(obj.raw,ctypes.c_void_p).value
    for i in range(text.count_chars()):
        if pdf.raw.FPDFText_GetUnicode(text,i)!=ord(char):continue
        owner=pdf.raw.FPDFText_GetTextObject(text,i)
        if ctypes.cast(owner,ctypes.c_void_p).value!=address:continue
        x,y=ctypes.c_double(),ctypes.c_double()
        if not pdf.raw.FPDFText_GetCharOrigin(text,i,ctypes.byref(x),ctypes.byref(y)):continue
        return text.get_charbox(i),[x.value,y.value]
    raise ValueError('No matching source character in compound object')


def render_character(doc,page,text,obj,char,scale):
    raw=pdf.raw.FPDFTextObj_GetRenderedBitmap(doc,page,obj,scale)
    if not raw:raise ValueError('Empty/unrenderable text object')
    bitmap=pdf.PdfBitmap.from_raw(raw);image=bitmap.to_pil().copy();bitmap.warn_on_close=False;bitmap.close()
    box=list(obj.get_bounds());matrix=obj.get_matrix();origin=[matrix.e,matrix.f]
    if obj.extract().strip()!=char:
        box2,origin=char_location(text,obj,char)
        crop=[math.floor((box2[0]-box[0])*scale),math.floor((box[3]-box2[3])*scale),
              math.ceil((box2[2]-box[0])*scale),math.ceil((box[3]-box2[1])*scale)]
        if crop[0]<-2 or crop[1]<-2 or crop[2]>image.width+2 or crop[3]>image.height+2:
            raise ValueError('Character/page-object coordinate mismatch')
        image=image.crop(tuple(crop));box=list(box2)
    image=image.convert('RGBA')
    if not image.getchannel('A').getbbox():raise ValueError('No ink')
    return image,box,origin


def run(args):
    args.output.mkdir(parents=True,exist_ok=True)
    files=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(args.inventory.glob('A*.json'))]
    choices={}
    preferred=['Sincerely','Idol','IRIS OUT','Shirushi']
    for data in files:
        for family,font in data['fonts'].items():
            if family!=args.family:continue
            for cp,glyph in font['glyphs'].items():
                key=family+':'+cp
                row=choices.setdefault(key,dict(font=family,unicode=cp,char=glyph['char'],count=0,candidates=[]))
                row['count']+=glyph['count']
                rank=next((i for i,name in enumerate(preferred) if Path(data['source_path']).name.startswith(name)),9)
                for sample in glyph['samples']:
                    page=data['page_geometry'][sample['page']-1]
                    spaces=page['staff_spaces'];sp=spaces[0]['space_pt'] if spaces else sample['size_pt']/4
                    row['candidates'].append(dict(score=data['id'],source=data['source_path'],sha256=data['sha256'],
                         staff_space_pt=sp,staff_measured=bool(spaces),rank=[rank,not sample.get('single',True),abs(sample['size_pt']/sp-4),data['id']],**sample))
    manifest={};documents={};pages={}
    for index,(key,row) in enumerate(sorted(choices.items())):
        filename='glyph-%s.png'%row['unicode'][2:];errors=[]
        for sample in sorted(row['candidates'],key=lambda s:s['rank'])[:12]:
            try:
                path=sample['source']
                if path not in documents:documents[path]=pdf.PdfDocument(path)
                doc=documents[path];pagekey=(path,sample['page'])
                if pagekey not in pages:
                    page=doc[sample['page']-1];text=page.get_textpage()
                    objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text))
                    pages[pagekey]=(page,text,objects)
                page,text,objects=pages[pagekey];obj=objects[sample['text_object_index']]
                image,box,origin=render_character(doc,page,text,obj,row['char'],args.scale)
                image.save(args.output/filename)
                manifest[key]=dict(font=row['font'],unicode=row['unicode'],char=row['char'],count=row['count'],
                     status='rendered',image=filename,sample=sample,bounds_pt=box,origin_pt=origin,
                     bitmap_scale=args.scale,pixel_size=image.size,nominal_space_pt=sample['size_pt']/4)
                break
            except (ValueError,RuntimeError) as error:errors.append(str(error))
        else:manifest[key]=dict(font=row['font'],unicode=row['unicode'],char=row['char'],count=row['count'],status='unresolved',errors=errors)
    for path,doc in documents.items():
        expected=next(d['sha256'] for d in files if d['source_path']==path)
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
    for page,text,objects in pages.values():text.close();page.close()
    for doc in documents.values():doc.close()
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
    entries=list(manifest.values())
    for start in range(0,len(entries),24):
        board=Image.new('RGB',(2400,2000),'white');draw=ImageDraw.Draw(board)
        for i,item in enumerate(entries[start:start+24]):
            x=i%6*400;y=i//6*500
            draw.text((x+12,y+15),item['unicode']+'  count '+str(item['count']),font=label,fill='black')
            if item['status']=='rendered':
                image=Image.open(args.output/item['image']).convert('RGBA');paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image);image=paper.convert('RGB')
                box=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
                if box:image=image.crop(box)
                image.thumbnail((330,365));board.paste(image,(x+(400-image.width)//2,y+75+(365-image.height)//2))
                draw.text((x+12,y+465),item['sample']['score']+' p'+str(item['sample']['page']),font=label,fill='black')
            else:draw.text((x+12,y+200),'UNRESOLVED',font=label,fill='red')
        board.save(args.output/('atlas-%02d.png'%(start//24+1)))
    (args.output/'catalog.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Catalog:',len(manifest),'rendered:',sum(x['status']=='rendered' for x in manifest.values()),'unresolved:',sum(x['status']!='rendered' for x in manifest.values()))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--family',default='Chaconne');p.add_argument('--scale',type=float,default=48)
    run(p.parse_args())
