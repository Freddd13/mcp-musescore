"""Capture periodic interiors of actual PDF wave runs, preserving Text baseline.

Neighbouring wave glyphs in the reference already overlap. Capture their union
in memory, then select one interior period plus overlap, instead of cropping
one glyph whose end caps may differ. Source PDFs are never saved.
"""
import argparse,copy,ctypes,hashlib,json,math,statistics
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from capture_corpus_font import box_of,clip_polygon
from capture_pdf_reference import trace_pixels


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'))
    catalog=json.loads(args.catalog.read_text(encoding='utf-8'));report=[]
    for symbol,code,vertical in [('wiggleTrill','005F',False),('wiggleArpeggiatoUp','0067',True)]:
        item=catalog['Chaconne:U+'+code];sample=item['sample'];source=Path(sample['source'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==sample['sha256']
        doc=pdf.PdfDocument(source);page=doc[sample['page']-1];text=page.get_textpage()
        text_objects=list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text));obj=text_objects[sample['text_object_index']]
        m=obj.get_matrix();sp=item['nominal_space_pt'];selected=[];origins=[]
        address=lambda o:ctypes.cast(o.raw,ctypes.c_void_p).value
        if vertical:
            for other in text_objects:
                matrix=other.get_matrix()
                if (other.extract()==item['char'] and other.get_font().get_base_name()==sample['font']
                    and abs(matrix.e-m.e)<.01 and abs(matrix.a-m.a)<.01):
                    selected.append(other);origins.append(matrix.f)
            # A page can have separate columns/runs at the same x. Restrict
            # to the connected run containing the selected source object.
            pairs=sorted(zip(origins,selected),key=lambda p:p[0]);runs=[]
            for origin,other in pairs:
                if not runs or origin-runs[-1][-1][0]>1.5*sp:runs.append([])
                runs[-1].append((origin,other))
            group=next(r for r in runs if any(address(o)==address(obj) for _,o in r))
            origins=[v for v,_ in group];selected=[v for _,v in group]
            assert len(origins)>=3,'Need an interior of a source run'
        else:
            selected=[obj]
            for i in range(text.count_chars()):
                if pdf.raw.FPDFText_GetUnicode(text,i)!=ord(item['char']):continue
                if ctypes.cast(pdf.raw.FPDFText_GetTextObject(text,i),ctypes.c_void_p).value!=address(obj):continue
                x,y=ctypes.c_double(),ctypes.c_double()
                assert pdf.raw.FPDFText_GetCharOrigin(text,i,ctypes.byref(x),ctypes.byref(y))
                origins.append(x.value)
            assert len(origins)>=5
        origins=sorted(set(origins));period=statistics.median(b-a for a,b in zip(origins,origins[1:]))
        assert .7<period/sp<1.4,(symbol,period/sp)
        # Interior phase follows the original glyph origins. Arpeggio g has
        # a two-cycle silhouette, so select the middle cycle of its union.
        start=origins[len(origins)//2]+(.5*period if vertical else 0)
        lo=start-.06*sp;hi=start+period+.06*sp
        boxes=[v.get_bounds() for v in selected]
        a=min(v[0] for v in boxes)-.1;b=min(v[1] for v in boxes)-.1
        c=max(v[2] for v in boxes)+.1;d=max(v[3] for v in boxes)+.1
        if vertical:b=max(b,lo-.1);d=min(d,hi+.1)
        else:a=max(a,lo-.1);c=min(c,hi+.1)
        active={address(o) for o in selected}
        all_objects=list(page.get_objects())
        for other in all_objects:assert pdf.raw.FPDFPageObj_SetIsActive(other,address(other) in active)
        w,h=page.get_size();bitmap=page.render(scale=args.scale,crop=(a,b,w-c,h-d))
        image=bitmap.to_pil().copy().convert('RGB');bitmap.close();image.save(args.output/(symbol+'-source-union.png'))
        loops=trace_pixels(np.asarray(image.convert('L'))<127)
        outlines=[[[a+x/args.scale,d-y/args.scale] for x,y in loop] for loop in loops]
        axis=1 if vertical else 0
        outlines=[clip_polygon(clip_polygon(v,axis,lo,True),axis,hi,False) for v in outlines]
        outlines=[v for v in outlines if len(v)>2]
        advance=round(period/sp*250);xscale=advance/period
        if vertical:
            right=max(x for v in outlines for x,y in v)
            outlines=[[[round((y-start)*xscale,6),round((right-x)*250/sp,6)] for x,y in v] for v in outlines]
        else:
            outlines=[[[round((x-start)*xscale,6),round((y-m.f)*250/sp,6)] for x,y in v] for v in outlines]
        old=data['glyphs'][symbol];old.update(outlines=outlines,bounds=box_of(outlines),advance=advance,repeat=advance,
            mode='periodic_source_union',source=str(source),page=sample['page'],object_index=sample['text_object_index'],
            calibration='source nominal font size / 4; period from actual glyph origins',
            notes=['Interior source-wave union, retained Text baseline; integer advance with recorded minimal period quantization'])
        if vertical:
            other=copy.deepcopy(old);other['codepoint']=data['glyphs']['wiggleArpeggiatoDown']['codepoint'];data['glyphs']['wiggleArpeggiatoDown']=other
        report.append(dict(symbol=symbol,page=sample['page'],source=str(source),sha256=sample['sha256'],
            source_objects=len(selected),source_period_pt=period,source_period_sp=period/sp,advance=advance,
            source_render_bounds_pt=[a,b,c,d],source_clip_axis=axis,source_clip_interval_pt=[lo,hi],
            nominal_space_pt=sp,bitmap_scale=args.scale,
            period_scale_ratio=advance/(period/sp*250),bounds_sp=[v/250 for v in old['bounds']]))
        text.close();page.close();doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==sample['sha256']
    data['version']='0.430';data['wave_study']=report
    for source,sha in data['sources'].items():assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==sha
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for row in report:print(row['symbol'],'source objects',row['source_objects'],'period sp',row['source_period_sp'],'bounds sp',row['bounds_sp'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--scale',type=float,default=128);run(p.parse_args())
