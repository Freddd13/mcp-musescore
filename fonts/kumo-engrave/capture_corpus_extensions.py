"""Add reviewed observed symbols/composites to the local font capture.

Text-object coordinates and page staff measurements are kept distinct. Private
Unicode composites remain explicitly labelled rather than masquerading as
standard SMuFL symbols. PDFs are read only; no FontFile is saved.
"""
import argparse,ctypes,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from capture_pdf_reference import trace_pixels
from capture_corpus_font import box_of
from catalog_pdf_glyphs import render_character
from catalog_pending_fonts import render_object
from source.contours import area

ROOT=Path(__file__).resolve().parent


def render_segment(doc,page,text,obj,which,scale):
    address=ctypes.cast(obj.raw,ctypes.c_void_p).value;characters=[]
    for i in range(text.count_chars()):
        if ctypes.cast(pdf.raw.FPDFText_GetTextObject(text,i),ctypes.c_void_p).value!=address:continue
        x,y=ctypes.c_double(),ctypes.c_double()
        if not pdf.raw.FPDFText_GetCharOrigin(text,i,ctypes.byref(x),ctypes.byref(y)):continue
        characters.append(dict(char=chr(pdf.raw.FPDFText_GetUnicode(text,i)),box=text.get_charbox(i),origin=[x.value,y.value]))
    if which=='first_two':
        assert ''.join(c['char'] for c in characters[:2])=='ŒÊ','Recheck A003 swing encoding'
        chosen=characters[:2]
    else:
        at=next(i for i,c in enumerate(characters) if c['char']=='=')
        chosen=[c for c in characters[at+1:] if not c['char'].isspace()]
    assert chosen
    bounds=[min(c['box'][0] for c in chosen),min(c['box'][1] for c in chosen),max(c['box'][2] for c in chosen),max(c['box'][3] for c in chosen)]
    original=list(obj.get_bounds());image=render_object(doc,page,obj,scale)
    crop=(math.floor((bounds[0]-original[0])*scale),math.floor((original[3]-bounds[3])*scale),
          math.ceil((bounds[2]-original[0])*scale),math.ceil((original[3]-bounds[1])*scale))
    return image.crop(crop),bounds,chosen[0]['origin']


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.base_capture.read_text(encoding='utf-8'));specs=json.loads(args.specs.read_text(encoding='utf-8'))
    sm=json.loads(args.glyphnames.read_text(encoding='utf-8'))
    cats={name:json.loads((args.study/folder/'catalog.json').read_text(encoding='utf-8')) for name,folder in [('chaconne','chaconne-catalog-v2'),('cid','cid1-catalog-v2')]}
    pending={g['id']:g for g in json.loads((args.study/'pending-fonts-01/catalog.json').read_text(encoding='utf-8'))['groups']}
    docs={};pages={};files={};added=[]
    for spec in specs['glyphs']:
        if 'catalog' in spec:
            item=cats[spec['catalog']][spec['key']];sample=item['sample'];score=sample['score'];char=item['char']
            index=sample['text_object_index'];page_number=sample['page']
        else:
            item=pending[spec['pending']];sample=item['samples'][0];score=item['score'];char=spec.get('character')
            index=sample['object_index'];page_number=sample['page']
        if score not in files:files[score]=json.loads((args.study/'corpus-v2'/(score+'.json')).read_text(encoding='utf-8'))
        source=files[score]['source_path'];expected=files[score]['sha256'];data['sources'][source]=expected
        if source not in docs:
            assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==expected;docs[source]=pdf.PdfDocument(source)
        doc=docs[source];key=(source,page_number)
        if key not in pages:
            page=doc[page_number-1];text=page.get_textpage();pages[key]=(page,text,list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)))
        page,text,objects=pages[key];obj=objects[index];matrix=obj.get_matrix()
        assert abs(matrix.b)<1e-6 and abs(matrix.c)<1e-6,'Rotation requires explicit adaptation'
        size=math.hypot(matrix.a,matrix.b)*obj.get_font_size();nominal=size/4
        if spec.get('segment'):
            image,bounds,origin=render_segment(doc,page,text,obj,spec['segment'],args.scale)
        else:image,bounds,origin=render_character(doc,page,text,obj,char,args.scale)
        image.save(args.output/(spec['symbol']+'.png'))
        spaces=files[score]['page_geometry'][page_number-1]['staff_spaces']
        space=spaces[0]['space_pt'] if spec.get('calibration')=='staff' else nominal
        assert space>0
        outlines=[[[round((bounds[0]-origin[0]+x/args.scale)*250/space,6),
                     round((bounds[3]-origin[1]-y/args.scale)*250/space,6)] for x,y in loop]
                  for loop in trace_pixels(np.asarray(image.getchannel('A'))>127)]
        b=box_of(outlines);mode=spec['mode'];dy=0
        if mode=='bottom_zero':dy=-b[1]
        elif mode=='center_y':dy=-(b[1]+b[3])/2
        elif mode=='met_baseline':dy=-172-b[1]
        elif mode=='flag_down':dy=-10-b[1]
        outlines=[[[x,y+dy] for x,y in v] for v in outlines];b=box_of(outlines)
        symbol=spec['symbol'];assert symbol not in data['glyphs']
        cp=int(spec['codepoint'],16) if 'codepoint' in spec else int(sm[symbol]['codepoint'][2:],16)
        assert cp not in {g['codepoint'] for g in data['glyphs'].values()}
        data['glyphs'][symbol]=dict(codepoint=cp,outlines=outlines,bounds=b,advance=int(math.ceil(b[2])),repeat=None,
            source=source,source_sha256=expected,page=page_number,object_index=index,source_text=obj.extract(),
            source_key=spec.get('key',spec.get('pending')),mode=mode,calibration=spec.get('calibration','nominal'),
            nominal_space_pt=nominal,used_space_pt=space,smufl=symbol in sm,usage=spec.get('usage','standard' if symbol in sm else 'explicit Unicode in music Text'),
            notes=['Reviewed source object or character span; not a font-program extraction'])
        added.append(symbol)
    # Keep whole/half-rest bodies consistent when MuseScore requests a built-in
    # leger-line form. Retain Leland's side extensions and line thickness.
    meta=json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))
    for symbol in specs['derived']:
        source_symbol='restWhole' if 'Whole' in symbol else 'restHalf';body=data['glyphs'][source_symbol];b=body['bounds']
        old=meta['glyphBBoxes'][source_symbol];ledger=meta['glyphBBoxes'][symbol]
        x0=b[0]+(ledger['bBoxSW'][0]-old['bBoxSW'][0])*250;x1=b[2]+(ledger['bBoxNE'][0]-old['bBoxNE'][0])*250
        half=abs(ledger['bBoxNE'][1] if 'Whole' in symbol else ledger['bBoxSW'][1])*250
        assert 0<half<50,(symbol,half)
        line=[[x0,-half],[x0,half],[x1,half],[x1,-half]]
        if area(line)*area(body['outlines'][0])<0:line.reverse()
        outlines=body['outlines']+[line]
        data['glyphs'][symbol]=dict(codepoint=int(sm[symbol]['codepoint'][2:],16),outlines=outlines,bounds=box_of(outlines),advance=body['advance'],repeat=None,
            mode='derived',smufl=True,source_key=source_symbol+' + baseline leger line metrics',
            notes=['Observed rest body; Leland side extensions/line thickness, ordinary rest advance retained'])
        added.append(symbol)
    for path,expected in data['sources'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
    for page,text,objects in pages.values():text.close();page.close()
    for doc in docs.values():doc.close()
    data.update(version=specs['version'],extension_spec_sha256=hashlib.sha256(args.specs.read_bytes()).hexdigest(),extension_symbols=added)
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Reviewed extensions',len(added),'total',len(data['glyphs']),'all source hashes unchanged')
    for name in added:print(name,'bounds sp',[round(v/250,4) for v in data['glyphs'][name]['bounds']])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base-capture',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--study',type=Path,default=ROOT/'dist')
    p.add_argument('--specs',type=Path,default=ROOT/'source/corpus_extensions.json');p.add_argument('--scale',type=float,default=128)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'))
    run(p.parse_args())
