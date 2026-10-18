"""Select context-reviewed alternate instances and remaining direct characters."""
import argparse,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from catalog_pdf_glyphs import render_character

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    old=json.loads(args.capture.read_text(encoding='utf-8'))
    inventories=[json.loads(p.read_text(encoding='utf-8')) for p in (args.study/'corpus-v2').glob('A*.json')]
    by_source={r['source_path']:r for r in inventories}
    chaconne=json.loads((args.study/'chaconne-catalog-v2/catalog.json').read_text(encoding='utf-8'))
    cid=json.loads((args.study/'cid1-catalog-v2/catalog.json').read_text(encoding='utf-8'))
    choices=[('articAccentStaccatoBelow','Chaconne:U+00A1',chaconne,'top_zero'),
             ('coda','Chaconne:U+00A0',chaconne,'raw'),
             ('kumoSwingDotted8Sixteenth','Chaconne:U+0131',chaconne,'met_baseline'),
             ('dynamicSforzando1','CIDFont+F1:U+F053',cid,'raw'),
             ('ottavaAlta','CIDFont+F1:U+F0C3',cid,'raw')]
    contexts={};spec=dict(version='0.470',glyphs=[],derived=[])
    for name,key,cat,mode in choices:
        assert not old['glyphs'][name].get('commands')
        contexts[name]=cat[key]
        spec['glyphs'].append(dict(group=name,symbol=name,mode=mode,replace=True,calibration='nominal',reject_retains_previous=True))
    for name,char in [('ottava','\u00e2'),('noteheadParenthesisLeft','('),('noteheadParenthesisRight',')')]:
        row=old['glyphs'][name];source=Path(row['source']);inv=by_source[str(source)]
        assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256'];doc=pdf.PdfDocument(source)
        page=doc[row['page']-1];text=page.get_textpage();objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=objects[row['object_index']]
        image,box,origin=render_character(doc,page,text,obj,char,4)
        contexts[name]=dict(char=char,bounds_pt=box,origin_pt=origin,sample=dict(source=str(source),sha256=inv['sha256'],score=inv['id'],
                                page=row['page'],text_object_index=row['object_index']))
        spec['glyphs'].append(dict(group=name,symbol=name,mode=row['mode'],replace=True,reject_retains_previous=True))
        text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==inv['sha256']
    (args.output/'catalog.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (args.output/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Remaining direct/alternate candidates',len(spec['glyphs']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--study',type=Path,default=ROOT/'dist');p.add_argument('--output',type=Path,required=True);run(p.parse_args())
