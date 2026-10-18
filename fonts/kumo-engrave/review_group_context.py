"""Read-only page contexts for reviewed silhouette-group members."""
import argparse,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from catalog_pdf_glyphs import render_character
from review_pdf_context import run as render_context


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    groups={g['id']:g for g in json.loads(args.groups.read_text(encoding='utf-8'))['groups']}
    catalog={};docs={};pages={};inventories={}
    for name in args.ids:
        row=groups[name]['members'][0];score=row['score']
        if score not in inventories:inventories[score]=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        inv=inventories[score];source=inv['source_path']
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==inv['sha256']
        if source not in docs:docs[source]=pdf.PdfDocument(source)
        doc=docs[source];key=(source,row['page'])
        if key not in pages:
            page=doc[row['page']-1];text=page.get_textpage();pages[key]=(page,text,list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)))
        page,text,objects=pages[key];obj=objects[row['object_index']]
        char=inv['fonts'][row['font']]['glyphs'][row['unicode']]['char']
        image,bounds,origin=render_character(doc,page,text,obj,char,4)
        catalog[name]=dict(char=char,bounds_pt=bounds,origin_pt=origin,font=row['font'],object_text=obj.extract(),
            sample=dict(source=source,sha256=inv['sha256'],score=score,page=row['page'],text_object_index=row['object_index']))
        print(name,row['score'],row['font'],row['unicode'],'p',row['page'],'object',row['object_index'],json.dumps(obj.extract(),ensure_ascii=True))
    for page,text,objects in pages.values():text.close();page.close()
    for doc in docs.values():doc.close()
    path=args.output/'catalog.json';path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    names=list(catalog)
    for start in range(0,len(names),8):render_context(argparse.Namespace(catalog=path,output=args.output/('contexts-%02d.png'%(start//8+1)),keys=names[start:start+8]))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--groups',type=Path,required=True)
    p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('ids',nargs='+');run(p.parse_args())
