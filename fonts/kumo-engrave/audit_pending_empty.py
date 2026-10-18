"""Exhaustively render font groups whose catalogue samples had no ink.

Checks every matching text object, not just the first sample or Unicode text.
Source files are read-only and SHA256-checked before/after.
"""
import argparse,hashlib,json,re
from pathlib import Path
import pypdfium2 as pdf
from catalog_pending_fonts import render_object


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    catalog=json.loads(args.catalog.read_text(encoding='utf-8'));rows=[]
    pending=[r for r in catalog['groups'] if not any(s['status']=='ink' for s in r['samples'])]
    for row in pending:
        inv=json.loads((args.inventory/(row['score']+'.json')).read_text(encoding='utf-8'))
        path=Path(inv['source_path']);before=hashlib.sha256(path.read_bytes()).hexdigest();assert before==inv['sha256']
        doc=pdf.PdfDocument(path);objects=[]
        for number in range(1,len(doc)+1):
            page=doc[number-1];text=page.get_textpage()
            for index,obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)):
                name=re.sub(r'^[A-Z]{6}\+','',obj.get_font().get_base_name())
                if name!=row['font']:continue
                item=dict(page=number,object_index=index,text=obj.extract())
                try:
                    im=render_object(doc,page,obj,12);name=row['id']+'-p%d-o%d.png'%(number,index)
                    im.save(args.output/name);item.update(status='ink',image=name)
                except ValueError as error:item.update(status='no-rendered-ink',reason=str(error))
                objects.append(item)
            text.close();page.close()
        doc.close();assert hashlib.sha256(path.read_bytes()).hexdigest()==before
        assert len(objects)==row['objects'],(row['id'],len(objects),row['objects'])
        rows.append(dict(id=row['id'],score=row['score'],font=row['font'],sha256=before,objects=objects,
                         visible_objects=sum(v['status']=='ink' for v in objects)))
    (args.output/'audit.json').write_text(json.dumps(dict(groups=rows,source_hashes_unchanged=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Groups',len(rows),'objects',sum(len(r['objects']) for r in rows),'visible',sum(r['visible_objects'] for r in rows))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--catalog',type=Path,required=True)
    p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
