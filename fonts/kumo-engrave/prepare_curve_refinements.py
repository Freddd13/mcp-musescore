"""Select original character instances for remaining local raster outlines.

Existing provenance determines the selected object; this is not a global PDF
encoding map. Generated catalogs/captures remain private. Ambiguous API curves
are explicitly rejected so the previous reviewed glyph remains in the build.
"""
import argparse,json,hashlib
from pathlib import Path
import pypdfium2 as pdf
from catalog_pdf_glyphs import render_character

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    old=json.loads(args.capture.read_text(encoding='utf-8'));cat=json.loads((args.study/'chaconne-catalog-v2/catalog.json').read_text(encoding='utf-8'))
    spec=dict(version='0.460',glyphs=[],derived=[]);contexts={}
    for name,row in old['glyphs'].items():
        key=row.get('source_key','')
        if row.get('commands') or not key.startswith('Chaconne:'):continue
        if not row.get('page') or row.get('object_index') is None:continue
        sample=cat[key]['sample'];assert sample['source']==row['source'] and sample['page']==row['page'] and sample['text_object_index']==row['object_index'],name
        if name=='metNote8thUp':continue # Known mixed e+k character-box contamination; keep corrected prior shape.
        contexts[name]=cat[key]
        spec['glyphs'].append(dict(group=name,symbol=name,mode=row['mode'],replace=True,calibration='nominal',reject_retains_previous=True))
    contexts['DOWN']=cat['Chaconne:U+00D4']
    spec['glyphs'].append(dict(group='DOWN',symbol='flagInternalDown',mode='flag_down'))
    spec['derived'].append(dict(group='DOWN',symbol='flag32ndDown',text_objects=[514,515],mode='flag_down'))
    inv=json.loads((args.study/'corpus-v2/A031.json').read_text(encoding='utf-8'));source=Path(inv['source_path'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256'];doc=pdf.PdfDocument(source);page=doc[5];text=page.get_textpage()
    objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=objects[18]
    assert obj.extract().strip()=='^';image,box,origin=render_character(doc,page,text,obj,'^',4)
    contexts['MTEN']=dict(char='^',bounds_pt=box,origin_pt=origin,sample=dict(source=str(source),sha256=inv['sha256'],score='A031',page=6,text_object_index=18))
    spec['glyphs'].append(dict(group='MTEN',symbol='reviewMarcatoComponent',mode='bottom_zero',capture_only=True))
    spec['derived'].extend([dict(group='MTEN',symbol='articMarcatoTenutoAbove',text_objects=[18,19],mode='bottom_zero'),
                            dict(symbol='articMarcatoTenutoBelow',**{'from':'articMarcatoTenutoAbove'},reflect_y=True)])
    text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']
    (args.output/'catalog.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (args.output/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Prior glyph candidates',sum(v.get('replace',False) for v in spec['glyphs']),'new roles 4')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--study',type=Path,default=ROOT/'dist');p.add_argument('--output',type=Path,required=True);run(p.parse_args())
