"""Read filled page paths from an outlined score; no font streams or PDF writes.

Geometry stays local. This inventory does not assign note/rest meanings to
paths: beams, letters, slurs and symbols coexist and must be distinguished.
"""
import argparse,collections,ctypes,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from inventory_pdf_symbols import staff_spaces


def path_commands(obj):
    matrix=obj.get_matrix();commands=[];curve=[]
    for i in range(pdf.raw.FPDFPath_CountSegments(obj)):
        seg=pdf.raw.FPDFPath_GetPathSegment(obj,i);kind=pdf.raw.FPDFPathSegment_GetType(seg)
        x,y=ctypes.c_float(),ctypes.c_float()
        assert pdf.raw.FPDFPathSegment_GetPoint(seg,ctypes.byref(x),ctypes.byref(y))
        point=[matrix.a*x.value+matrix.c*y.value+matrix.e,matrix.b*x.value+matrix.d*y.value+matrix.f]
        if kind==pdf.raw.FPDF_SEGMENT_MOVETO:
            assert not curve;commands.append(['moveTo',[point]])
        elif kind==pdf.raw.FPDF_SEGMENT_LINETO:
            assert not curve;commands.append(['lineTo',[point]])
        elif kind==pdf.raw.FPDF_SEGMENT_BEZIERTO:
            curve.append(point)
            if len(curve)==3:commands.append(['curveTo',curve]);curve=[]
        else:raise ValueError('Unsupported segment type')
        if pdf.raw.FPDFPathSegment_GetClose(seg):
            assert not curve;commands.append(['closePath',[]])
    assert not curve
    return commands


def grouped_staff_spaces(objects):
    groups=collections.defaultdict(list)
    for obj in objects:
        if obj.type!=pdf.raw.FPDF_PAGEOBJ_PATH:continue
        previous=None
        for op,points in path_commands(obj):
            if op=='lineTo' and previous:
                a,b=previous,points[0]
                if abs(a[1]-b[1])<.05 and abs(a[0]-b[0])>150:
                    groups[(round(min(a[0],b[0])),round(max(a[0],b[0])))].append((a[1]+b[1])/2)
            previous=points[-1] if points else None
    gaps=[]
    for values in groups.values():
        clusters=[]
        for y in sorted(set(values)):
            if not clusters or y-clusters[-1][-1]>1.2:clusters.append([y])
            else:clusters[-1].append(y)
        ys=[sum(v)/len(v) for v in clusters]
        gaps.extend(round(b-a,3) for a,b in zip(ys,ys[1:]) if 2.5<b-a<8)
    return [dict(space_pt=v,support=n) for v,n in collections.Counter(gaps).most_common(5)]


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);before=hashlib.sha256(args.source.read_bytes()).hexdigest()
    doc=pdf.PdfDocument(args.source);data=dict(source=str(args.source.resolve()),sha256=before,pages=[],paths=[],ignored=collections.Counter())
    for n in range(len(doc)):
        page=doc[n];objects=list(page.get_objects());spaces=staff_spaces(page) or grouped_staff_spaces(objects)
        data['pages'].append(dict(page=n+1,size=page.get_size(),staff_spaces=spaces))
        assert spaces,'Measure the physical staff spacing before capturing paths'
        for index,obj in enumerate(objects):
            if obj.type!=pdf.raw.FPDF_PAGEOBJ_PATH:data['ignored']['non-path']+=1;continue
            assert obj.level==0,'Nested form transformations require separate handling'
            fill,stroke=ctypes.c_int(),ctypes.c_int()
            assert pdf.raw.FPDFPath_GetDrawMode(obj,ctypes.byref(fill),ctypes.byref(stroke))
            if not fill.value or stroke.value:data['ignored']['unfilled-or-stroked']+=1;continue
            rgba=[ctypes.c_uint() for _ in range(4)]
            assert pdf.raw.FPDFPageObj_GetFillColor(obj,*(ctypes.byref(v) for v in rgba))
            color=[v.value for v in rgba]
            if color[3]==0 or sum(color[:3])>600:data['ignored']['white-or-transparent']+=1;continue
            commands=path_commands(obj)
            # CFF closes fill contours implicitly. Keep explicit close markers
            # here; glyph construction handles any open fill subpaths.
            data['paths'].append(dict(page=n+1,object_index=index,bounds_pt=obj.get_bounds(),
                matrix=obj.get_matrix().get(),fill_mode=fill.value,color=color,
                staff_space_pt=spaces[0]['space_pt'],commands=commands))
        page.close()
    doc.close();assert hashlib.sha256(args.source.read_bytes()).hexdigest()==before
    (args.output/'paths.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Filled paths',len(data['paths']),'draw modes',dict(collections.Counter(v['fill_mode'] for v in data['paths'])),
          'ignored',dict(data['ignored']),'source hash unchanged')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);run(p.parse_args())
