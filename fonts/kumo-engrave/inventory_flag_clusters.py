"""Locate actual composed 32nd/64th flags around observed internal flag pieces.

Characters are only location hints, not semantic certification. Preserve every
cluster's coordinates, font and source hash for subsequent page review. PDFs
are read only; differently encoded/mixed text is reported rather than guessed.
"""
import argparse,hashlib,json,math,re
from pathlib import Path
import pypdfium2 as pdf
from audit_corpus_shapes import normalize_code

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);result=[];sources={};mixed=[]
    allowed={'K','r','j','\u00d4','R','J'}
    for name in args.scores:
        inv=json.loads((args.inventory/(name+'.json')).read_text(encoding='utf-8'));source=Path(inv['source_path'])
        sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha==inv['sha256'];sources[name]=dict(path=str(source),sha256=sha)
        doc=pdf.PdfDocument(source)
        for n in range(len(doc)):
            page=doc[n];text=page.get_textpage();rows=[]
            for index,obj in enumerate(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)):
                raw=obj.extract().strip();family=re.sub(r'^[A-Z]{6}\+','',obj.get_font().get_base_name())
                if family not in ('Chaconne','CIDFont+F1'):continue
                chars=''.join(normalize_code(c) for c in raw)
                if not chars or not any(c in allowed for c in chars):continue
                if len(chars)!=1:
                    mixed.append(dict(score=name,page=n+1,object_index=index,text=raw));continue
                if chars not in allowed:continue
                m=obj.get_matrix();size=math.hypot(m.a,m.b)*obj.get_font_size()
                rows.append(dict(object_index=index,text=raw,normalized=chars,font=family,matrix=m.get(),size_pt=size,bounds_pt=obj.get_bounds()))
            used=set()
            for item in rows:
                if item['normalized'] not in ('K','\u00d4'):continue
                ix=item['object_index']
                if ix in used:continue
                x,y=item['matrix'][4:6];size=item['size_pt']
                cluster=[v for v in rows if abs(v['matrix'][4]-x)<.05*size and abs(v['matrix'][5]-y)<.75*size and abs(v['size_pt']/size-1)<.02]
                used.update(v['object_index'] for v in cluster)
                result.append(dict(score=name,page=n+1,internal_object=ix,members=cluster,
                                   source=str(source),source_sha256=sha))
            text.close();page.close()
        doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
        print(name,'clusters',sum(v['score']==name for v in result),flush=True)
    report=dict(note='Source clusters for review, not automatic role certification',sources=sources,clusters=result,mixed=mixed)
    (args.output/'clusters.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for row in result:print(row['score'],'p',row['page'],json.dumps([(v['object_index'],v['normalized'],[round(v['matrix'][i],3) for i in (4,5)]) for v in row['members']],ensure_ascii=True))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v2')
    p.add_argument('--output',type=Path,required=True);p.add_argument('scores',nargs='+');run(p.parse_args())
