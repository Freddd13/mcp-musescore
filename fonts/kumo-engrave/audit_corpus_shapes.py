"""Find coverage gaps by comparing actual PDF object silhouettes.

Automatic shape matches are candidates, never a substitute for page-context
review. Unknown font names are scoped per PDF. Low scores and possible new
roles are retained for review; ordinary-text proposals remain explicit.
"""
import argparse,collections,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont
from catalog_pdf_glyphs import render_character
from source.pdf_symbol_map import GLYPHS,COMPOUNDS

ROOT=Path(__file__).resolve().parent


def normalize_code(char):
    if 0xf000<=ord(char)<=0xf0ff:return bytes([ord(char)&255]).decode('mac_roman')
    return char


def candidate(family,font):
    if font['category']=='music':return True,'named music font'
    if family=='FEF4ADEE9C2':return True,'visually reviewed control-code music font'
    keys={normalize_code(g['char']) for g in font['glyphs'].values()}
    if len(keys&set('&?œ˙Œ‰˜#'))>=2:return True,'music anchor set (provisional)'
    if keys and keys<=set('∑π≈∏∫˙ '):return True,'symbol-only subset (provisional)'
    return False,'unclassified/text proposal; not visually certified'


def fingerprint(image):
    if image.mode=='RGBA':mask=image.getchannel('A')
    else:mask=image.convert('L').point(lambda v:255-v)
    mask=mask.point(lambda v:255 if v>127 else 0);box=mask.getbbox()
    if not box:raise ValueError('No ink')
    mask=mask.crop(box);aspect=mask.width/mask.height
    return np.asarray(mask.resize((32,32)))>127,aspect


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    cat=json.loads(args.catalog.read_text(encoding='utf-8'));meta=json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))
    sm=json.loads(args.glyphnames.read_text(encoding='utf-8'));roles=collections.defaultdict(set)
    for name,aliases,mode in GLYPHS:
        for cp in aliases.split():roles[cp].add(name)
    for cp,names in COMPOUNDS.items():roles[cp].update(names)
    protos=[]
    for key,g in cat.items():
        if g['status']!='rendered':continue
        mask,aspect=fingerprint(Image.open(args.catalog.parent/g['image']).convert('RGBA'))
        protos.append(dict(name='|'.join(sorted(roles[key.split('U+')[1]])),mask=mask,aspect=aspect,source='Chaconne atlas'))
    base=ImageFont.truetype(str(ROOT/'vendor/leland/Leland.otf'),512)
    for name in meta['glyphBBoxes']:
        if name not in sm:continue
        raw=base.getmask(chr(int(sm[name]['codepoint'][2:],16)),mode='L')
        if not all(raw.size):continue
        im=Image.frombytes('L',raw.size,bytes(raw));rgba=Image.new('RGBA',im.size,'black');rgba.putalpha(im)
        try:mask,aspect=fingerprint(rgba)
        except ValueError:continue
        protos.append(dict(name=name,mask=mask,aspect=aspect,source='Leland fallback'))
    masks=np.stack([g['mask'] for g in protos]);aspects=np.array([g['aspect'] for g in protos]);areas=masks.sum(axis=(1,2))
    report=dict(schema=1,note='Automatic silhouette candidates; confirm page context and font-role collisions before marking complete.',
                rows=[],noncandidate_fonts=[],sources={},review_files=[])
    files=sorted(args.inventory.glob('A*.json'));serial=0
    for f in files:
        data=json.loads(f.read_text(encoding='utf-8'));source=Path(data['source_path']);doc=None;pages={}
        for family,font in data['fonts'].items():
            if font['category']=='text':continue
            use,reason=candidate(family,font)
            if not use:
                report['noncandidate_fonts'].append(dict(score=data['id'],font=family,keys=len(font['glyphs']),reason=reason));continue
            if doc is None:
                assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256'];doc=pdf.PdfDocument(source)
            for cp,glyph in font['glyphs'].items():
                row=dict(score=data['id'],font=family,unicode=cp,count=glyph['count'],selection=reason);errors=[]
                for sample in sorted(glyph['samples'],key=lambda s:(not s.get('single',True),-s['size_pt'])):
                    try:
                        n=sample['page']
                        if n not in pages:
                            page=doc[n-1];text=page.get_textpage();objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));pages[n]=(page,text,objects)
                        page,text,objects=pages[n];obj=objects[sample['text_object_index']]
                        im,box,origin=render_character(doc,page,text,obj,glyph['char'],8)
                        mask,aspect=fingerprint(im);intersection=np.logical_and(masks,mask).sum(axis=(1,2));union=areas+mask.sum()-intersection
                        scores=(intersection/np.maximum(union,1))*np.minimum(aspects/aspect,aspect/aspects)**.4
                        best=np.argsort(-scores)[:3]
                        row.update(page=n,object_index=sample['text_object_index'],status='matched-candidate',
                            matches=[dict(name=protos[i]['name'],source=protos[i]['source'],score=round(float(scores[i]),4)) for i in best])
                        chosen=row['matches'][0];new_role=any(name not in {v[0] for v in GLYPHS} and not name.startswith(('text:','engine:','variant:')) for name in chosen['name'].split('|'))
                        if chosen['score']<.82 or new_role:
                            serial+=1;filename='review-%04d.png'%serial;im.save(args.output/filename);row['review_image']=filename
                            report['review_files'].append(dict(image=filename,label=data['id']+' '+cp+' '+chosen['name'][:42]+' '+str(chosen['score'])))
                        break
                    except (ValueError,RuntimeError) as e:errors.append(str(e))
                else:row.update(status='unresolved',errors=errors)
                report['rows'].append(row)
        for page,text,objects in pages.values():text.close();page.close()
        if doc:
            doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256']
            report['sources'][data['id']]=data['sha256']
        print(data['id'],'candidate keys',len(report['rows']),'review',len(report['review_files']),flush=True)
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(report['review_files']),24):
        board=Image.new('RGB',(1800,1200),'white');draw=ImageDraw.Draw(board)
        for i,item in enumerate(report['review_files'][start:start+24]):
            x=i%6*300;y=i//6*300;im=Image.open(args.output/item['image']).convert('RGBA');paper=Image.new('RGBA',im.size,'white');paper.alpha_composite(im);im=paper.convert('RGB');im.thumbnail((240,230))
            board.paste(im,(x+(300-im.width)//2,y+45));draw.text((x+5,y+5),item['label'][:30],font=label,fill='black');draw.text((x+5,y+25),item['label'][30:],font=label,fill='black')
        board.save(args.output/('review-sheet-%02d.png'%(start//24+1)))
    (args.output/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary=dict(candidate_keys=len(report['rows']),sources=len(report['sources']),review=len(report['review_files']),
                 unresolved=sum(v['status']=='unresolved' for v in report['rows']),remaining_font_groups=len(report['noncandidate_fonts']))
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(summary)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'))
    run(p.parse_args())
