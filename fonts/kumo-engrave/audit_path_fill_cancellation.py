"""Verify reversed-edge cancellation of the ten previously blank A064 paths.

Reads source objects again and renders them without writing the PDF. Bezier
edges are compared with their exact reversed controls, not just signed area:
zero signed area alone would not establish zero filled ink.
"""
import argparse,collections,ctypes,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from PIL import ImageOps
from capture_pdf_paths import path_commands

PATHS_SHA='ac4be06dcb041ae648e6709d23babb07e941d6fb46963004f4fe0f58740c52f3'
GROUPS_SHA='c7ea3e7b2424bce1b9ca36fcb1dfc7ab48bb7d981ffbd9809fbd92d30d29ee87'


def edge_counter(commands):
    result=collections.Counter();position=start=None
    def add(points):
        # PDFium's stored float coordinates match exactly for these reversals;
        # rounding could incorrectly collapse a genuinely thin filled contour.
        points=tuple(tuple(point) for point in points)
        if len(set(points))>1:result[points]+=1
    for op,points in commands:
        if op=='moveTo':position=start=points[0]
        elif op=='lineTo':add([position,points[0]]);position=points[0]
        elif op=='curveTo':add([position]+points);position=points[-1]
        elif op=='closePath':add([position,start]);position=start
        else:raise ValueError(op)
    return result


def cancels(commands):
    edges=edge_counter(commands)
    return bool(edges) and edges==collections.Counter({tuple(reversed(k)):n for k,n in edges.items()})


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    for path,sha in [(args.paths,PATHS_SHA),(args.groups,GROUPS_SHA)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
    data=json.loads(args.paths.read_text(encoding='utf-8'));groups=json.loads(args.groups.read_text(encoding='utf-8'))
    source=Path(data['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256']
    by_key={(r['page'],r['object_index']):r for r in data['paths']}
    expected={(r['page'],r['object_index']) for r in groups['no_visible_ink_at_recorded_scale']}
    detected={(r['page'],r['object_index']) for r in data['paths'] if cancels(r['commands'])}
    assert detected==expected,(detected-expected,expected-detected)
    doc=pdf.PdfDocument(source);rows=[];controls=[]
    for number in sorted({p for p,o in expected}):
        page=doc[number-1];objects=list(page.get_objects())
        for obj in objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
        # Also inspect a visibly filled regular slur from the same source page.
        candidates=[r for r in data['paths'] if r['page']==number and sum(op=='curveTo' for op,pts in r['commands'])>=2
            and (r['page'],r['object_index']) not in expected and r['bounds_pt'][2]-r['bounds_pt'][0]>30]
        control=next(r for r in candidates if not cancels(r['commands']))
        selected=[by_key[key] for key in sorted(expected) if key[0]==number]+[control]
        for item in selected:
            obj=objects[item['object_index']];assert obj.type==pdf.raw.FPDF_PAGEOBJ_PATH and obj.level==0
            assert path_commands(obj)==item['commands'],'Cached geometry changed'
            fill,stroke=ctypes.c_int(),ctypes.c_int()
            assert pdf.raw.FPDFPath_GetDrawMode(obj,ctypes.byref(fill),ctypes.byref(stroke))
            assert fill.value==item['fill_mode'] and not stroke.value
            is_cancelled=(number,item['object_index']) in expected
            a,b,c,d=item['bounds_pt'];w,h=page.get_size();pad=1
            assert pdf.raw.FPDFPageObj_SetIsActive(obj,True)
            extrema=[]
            for scale in (4,16):
                bitmap=page.render(scale=scale,crop=(a-pad,b-pad,w-c-pad,h-d-pad))
                im=bitmap.to_pil().copy().convert('RGB');bitmap.close()
                # Pixel extrema on white paper, independent of alpha modes.
                low,high=ImageOps.grayscale(im).getextrema();extrema.append(dict(scale=scale,luma=[low,high]))
                assert (low==255)==is_cancelled,(number,item['object_index'],scale,low)
            assert pdf.raw.FPDFPageObj_SetIsActive(obj,False)
            edges=edge_counter(item['commands'])
            row=dict(page=number,object_index=item['object_index'],fill_mode=fill.value,stroke=False,
                reversed_edges_cancel=is_cancelled,nondegenerate_edges=sum(edges.values()),renders=extrema)
            (rows if is_cancelled else controls).append(row)
        for obj in objects:assert pdf.raw.FPDFPageObj_SetIsActive(obj,True)
        page.close()
    doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256']
    report=dict(source=str(source),sha256=data['sha256'],all_7299_paths_scanned=True,
        exact_stored_coordinates=True,coordinate_comparison_rounding_pt=0,
        matching_cancelled_paths=rows,noncancelling_render_controls=controls,
        conclusion='Ten unstroked fill paths retrace every line/cubic edge in reverse; their fill cancels. They are not missing font glyphs.',source_unchanged=True)
    (args.output/'cancellation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('All',len(data['paths']),'paths scanned;',len(rows),'reverse-cancelled, rendered blank at 4x/16x;',len(controls),'visible controls passed')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    root=Path(__file__).resolve().parent/'dist'
    p.add_argument('--paths',type=Path,default=root/'A064-paths-03/paths.json')
    p.add_argument('--groups',type=Path,default=root/'path-groups-089/groups.json')
    p.add_argument('--output',type=Path,required=True);run(p.parse_args())
