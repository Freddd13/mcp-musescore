"""Resumable inventory of actually used text glyphs across the supplied scores.

Reads PDF page objects and font names, never font programs. Checkpoints and
sample locations stay under the ignored study directory. Named music fonts,
generic/CID fonts and ordinary text fonts remain distinct until reviewed.
"""
import argparse,collections,concurrent.futures,ctypes,hashlib,json,math,re,time
from pathlib import Path
import pypdfium2 as pdf

SCHEMA=3
ROOT=Path(__file__).resolve().parent


def category(name):
    if re.search(r'Chaconne|Pavane|Maestro|Engraver|Petrucci|Bravura|Leland|Finale|Opus|Sonata|November|Sebastian',name,re.I):return 'music'
    if re.search(r'CIDFont|^CID|^F\d+$|unknown|Identity|^FEF[0-9A-F]+$|^[0-9A-F]{8,}$',name,re.I):return 'unclassified'
    return 'text'


def staff_spaces(page):
    groups=collections.defaultdict(list)
    for obj in page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_PATH]):
        left,bottom,right,top=obj.get_bounds()
        if right-left>150 and 0<=top-bottom<1.2:
            groups[(round(left),round(right))].append((bottom+top)/2)
    gaps=[]
    for values in groups.values():
        values=sorted(set(round(v,3) for v in values))
        gaps.extend(b-a for a,b in zip(values,values[1:]) if 2.5<b-a<8)
    hist=collections.Counter(round(v,2) for v in gaps)
    # Retain alternatives: small staves/rounding must not become a hidden
    # assumption of one universal staff size for the whole corpus.
    return [{'space_pt':v,'support':n} for v,n in hist.most_common(5)]


def scan_one(task):
    entry,output=task;path=Path(entry['source_path']);dest=Path(output)/(entry['id']+'.json')
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    if dest.exists():
        cached=json.loads(dest.read_text(encoding='utf-8'))
        if cached.get('schema')==SCHEMA and cached.get('sha256')==before and cached.get('status')=='complete':
            return entry['id'],'cached',cached['pages']
        raise ValueError('Use a new output directory; incompatible/source-changed evidence must not be overwritten: '+str(dest))
    doc=pdf.PdfDocument(path);fonts={};page_rows=[];objects=0;source_chars=generated_chars=unowned_chars=0;unowned_samples=[]
    for page_index in range(len(doc)):
        page=doc[page_index];text=page.get_textpage();font_cache={};spaces=staff_spaces(page)
        text_objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text))
        owners={ctypes.cast(obj.raw,ctypes.c_void_p).value:index for index,obj in enumerate(text_objects)}
        characters=collections.defaultdict(list);page_generated=page_source=page_unowned=0
        for char_index in range(text.count_chars()):
            generated=pdf.raw.FPDFText_IsGenerated(text,char_index)
            assert generated in (0,1)
            if generated:
                page_generated+=1
                continue
            cp=pdf.raw.FPDFText_GetUnicode(text,char_index)
            error=pdf.raw.FPDFText_HasUnicodeMapError(text,char_index)
            assert error in (0,1)
            owner=pdf.raw.FPDFText_GetTextObject(text,char_index)
            index=owners.get(ctypes.cast(owner,ctypes.c_void_p).value)
            if index is None:
                page_unowned+=1
                if len(unowned_samples)<24:
                    unowned_samples.append(dict(page=page_index+1,char_index=char_index,codepoint=cp,
                                                unicode_mapping_error=bool(error),bounds_pt=text.get_charbox(char_index)))
                continue
            page_source+=1
            characters[index].append(dict(index=char_index,codepoint=cp,unicode_mapping_error=bool(error)))
        bbox=page.get_bbox()
        page_rows.append(dict(page=page_index+1,size_pt=page.get_size(),staff_spaces=spaces,bbox_pt=bbox,
                              rotation=page.get_rotation(),owned_source_characters=page_source,
                              generated_characters=page_generated,unowned_source_characters=page_unowned))
        source_chars+=page_source;generated_chars+=page_generated;unowned_chars+=page_unowned
        for index,obj in enumerate(text_objects):
            objects+=1
            raw_font=pdf.raw.FPDFTextObj_GetFont(obj)
            address=ctypes.cast(raw_font,ctypes.c_void_p).value
            if address not in font_cache:
                raw_name=obj.get_font().get_base_name()
                font_cache[address]=(raw_name,re.sub(r'^[A-Z]{6}\+','',raw_name))
            raw_name,name=font_cache[address]
            item=fonts.setdefault(name,dict(category=category(name),raw_names=[],objects=0,glyphs={}))
            if raw_name not in item['raw_names']:item['raw_names'].append(raw_name)
            item['objects']+=1
            value=obj.extract()
            actual=characters[index]
            by_code=collections.defaultdict(list)
            for char in actual:by_code[char['codepoint']].append(char)
            a,b,c,d=obj.get_bounds()
            on_page=c>bbox[0] and a<bbox[2] and d>bbox[1] and b<bbox[3]
            for cp,occurrences in by_code.items():
                key='U+%04X'%cp
                glyph=item['glyphs'].setdefault(key,dict(char=chr(cp),count=0,single_objects=0,
                    unicode_mapping_error_occurrences=0,samples=[]))
                glyph['count']+=len(occurrences)
                glyph['unicode_mapping_error_occurrences']+=sum(v['unicode_mapping_error'] for v in occurrences)
                single=len(actual)==1
                if single:glyph['single_objects']+=1
                # Full provenance of a few distinct source sizes. Later capture
                # chooses a normal-size occurrence after staff-scale review.
                if item['category']=='text' and len(glyph['samples'])>=1:continue
                matrix=obj.get_matrix();size=math.hypot(matrix.a,matrix.b)*obj.get_font_size()
                sample=dict(page=page_index+1,text_object_index=index,font=raw_name,
                            size_pt=round(size,5),matrix=matrix.get(),bounds_pt=obj.get_bounds(),level=obj.level,
                            single=single,object_text=value,source_char_indices=[v['index'] for v in occurrences],
                            source_character_count=len(actual),intersects_page_bbox=on_page)
                samples=glyph['samples']
                duplicate=any(abs(s['size_pt']-size)<.03 and s.get('single')==single and s['font']==raw_name
                              and s['intersects_page_bbox']==on_page for s in samples)
                if not duplicate or not samples:
                    samples.append(sample);samples.sort(key=lambda s:(not s['intersects_page_bbox'],not s['single'],-s['size_pt']))
                    del samples[6:]
        text.close();page.close()
    pages=len(doc);doc.close()
    assert hashlib.sha256(path.read_bytes()).hexdigest()==before,'Source changed while reading: '+entry['id']
    result=dict(schema=SCHEMA,status='complete',id=entry['id'],source_path=str(path),sha256=before,
                pages=pages,text_objects=objects,fonts=fonts,page_geometry=page_rows,
                owned_source_characters=source_chars,generated_characters=generated_chars,
                unowned_source_characters=unowned_chars,unowned_character_samples=unowned_samples,
                source_unchanged=True,font_program_extracted=False)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return entry['id'],'scanned',pages


def summarize(output,entries):
    merged={};families={};complete=[];pages=0;source_chars=generated_chars=unowned_chars=0
    for entry in entries:
        path=output/(entry['id']+'.json')
        if not path.exists():continue
        data=json.loads(path.read_text(encoding='utf-8'))
        if data.get('status')!='complete':continue
        complete.append(entry['id']);pages+=data['pages']
        source_chars+=data['owned_source_characters'];generated_chars+=data['generated_characters'];unowned_chars+=data['unowned_source_characters']
        for name,font in data['fonts'].items():
            family=families.setdefault(name,dict(category=font['category'],files=[],objects=0))
            family['files'].append(entry['id']);family['objects']+=font['objects']
            # Named music fonts can also have different encodings in each PDF.
            scope=entry['id']+':'+name
            for cp,glyph in font['glyphs'].items():
                key=scope+':'+cp
                row=merged.setdefault(key,dict(font=name,category=font['category'],char=glyph['char'],unicode=cp,count=0,single_objects=0,files=[],samples=[]))
                row['count']+=glyph['count'];row['single_objects']+=glyph['single_objects'];row['files'].append(entry['id'])
                if font['category']!='text':
                    for sample in glyph['samples']:
                        row['samples'].append(dict(score=entry['id'],**sample))
                    # Save locations in several scores, not hundreds of copies
                    # of the same shape. Per-file checkpoints retain the rest.
                    row['samples']=sorted(row['samples'],key=lambda s:(not s.get('single',True),-s['size_pt'],s['score'],s['page']))[:24]
    report=dict(schema=SCHEMA,expected_scores=len(entries),completed_scores=len(complete),completed_ids=complete,
                completed_pages=pages,inventory_complete=len(complete)==len(entries),families=families,glyphs=merged,
                owned_source_characters=source_chars,generated_characters=generated_chars,unowned_source_characters=unowned_chars,
                note='Actual source characters, including control/space/U+0000 codes; PDFium-generated characters excluded. All keys scoped per PDF. Font-name categories remain provisional, not visual identification or SMuFL mapping.')
    (output/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(completed_scores=len(complete),pages=pages,font_families=len(families),
                         music_keys=sum(x['category']=='music' for x in merged.values()),
                         unclassified_keys=sum(x['category']=='unclassified' for x in merged.values())),ensure_ascii=True),flush=True)


def run(args):
    args.output.mkdir(parents=True,exist_ok=True)
    for checkpoint in args.output.glob('A*.json'):
        cached=json.loads(checkpoint.read_text(encoding='utf-8'))
        if cached.get('schema')!=SCHEMA:
            raise ValueError('Use a new output directory; historical inventory is preserved: '+str(checkpoint))
    old=json.loads(args.catalog.read_text(encoding='utf-8'))
    ids={x['relative_path']:x['id'] for x in old['scores']}
    files=sorted(args.source.rglob('*.pdf'),key=lambda p:str(p.relative_to(args.source)).casefold())
    entries=[]
    for i,path in enumerate(files):
        relative=str(path.relative_to(args.source))
        entries.append(dict(id=ids.get(relative,'N%03d'%(i+1)),source_path=str(path.resolve())))
    tasks=entries[:args.limit] if args.limit else entries
    (args.output/'sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for index,result in enumerate(pool.map(scan_one,[(entry,str(args.output)) for entry in tasks])):
            print('%d/%d %s %s %d pages'%(index+1,len(tasks),*result),flush=True)
    summarize(args.output,entries)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--catalog',type=Path,default=ROOT/'../../docs/engraving/corpus/inventory.json')
    p.add_argument('--workers',type=int,default=2);p.add_argument('--limit',type=int)
    run(p.parse_args())
