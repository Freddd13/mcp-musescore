"""Local glyph-shape study of a user-supplied Chaconne score PDF.

Only existing PDF text objects are raster-rendered. No FontFile stream is read
or saved. Local contour data is intentionally outside distributable profiles;
it is a feasibility probe, not a reconstruction of the original font program.
Requires the bundled Python (Pillow, numpy, pypdfium2).
"""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from PIL import Image

ROOT=Path(__file__).resolve().parent
SYMBOLS={
    '\u0153':('black','noteheadBlack',0xe0a4),
    '\u02d9':('half','noteheadHalf',0xe0a3),
    'w':('whole','noteheadWhole',0xe0a2),
    '&':('g-clef','gClef',0xe050),
    '?':('f-clef','fClef',0xe062),
    '\u0152':('quarter-rest','restQuarter',0xe4e5),
    '\u2030':('8th-rest','rest8th',0xe4e6),
}


def trace_pixels(mask):
    """Pixel-edge loops, retaining curve asymmetry instead of fitting an oval."""
    edges={}
    def edge(a,b):edges.setdefault(a,[]).append(b)
    up=mask & ~np.pad(mask[:-1,:],((1,0),(0,0)))
    down=mask & ~np.pad(mask[1:,:],((0,1),(0,0)))
    left=mask & ~np.pad(mask[:,:-1],((0,0),(1,0)))
    right=mask & ~np.pad(mask[:,1:],((0,0),(0,1)))
    for y,x in np.argwhere(up):edge((int(x),int(y)),(int(x+1),int(y)))
    for y,x in np.argwhere(right):edge((int(x+1),int(y)),(int(x+1),int(y+1)))
    for y,x in np.argwhere(down):edge((int(x+1),int(y+1)),(int(x),int(y+1)))
    for y,x in np.argwhere(left):edge((int(x),int(y+1)),(int(x),int(y)))
    loops=[]
    while edges:
        start=next(iter(edges));point=start;previous=None;points=[]
        while True:
            points.append(point);options=edges[point]
            if len(options)>1 and previous:
                dx=point[0]-previous[0];dy=point[1]-previous[1]
                def order(q):
                    vx=q[0]-point[0];vy=q[1]-point[1]
                    cross=dx*vy-dy*vx;dot=dx*vx+dy*vy
                    return 0 if cross>0 else 1 if dot>0 else 2 if cross<0 else 3
                nxt=min(options,key=order)
            else:nxt=options[0]
            options.remove(nxt)
            if not options:del edges[point]
            previous,point=point,nxt
            if point==start:break
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1]))/2
        if abs(area)>4:
            # Remove only exactly collinear vertices. This is not curve fitting.
            points=[b for a,b,c in zip(points[-1:]+points[:-1],points,points[1:]+points[:1])
                    if (b[0]-a[0])*(c[1]-b[1])!=(b[1]-a[1])*(c[0]-b[0])]
            loops.append((area,points))
    return [p for a,p in sorted(loops,key=lambda v:abs(v[0]),reverse=True)]


def run(args):
    if args.scale<=0 or args.staff_space<=0 or args.pages<=0:
        raise ValueError('Scale, measured staff space and page count must be positive')
    if not args.source.is_file():raise ValueError('Supply a local score PDF')
    if args.output.exists():raise ValueError('Use a new study directory')
    args.output.mkdir(parents=True)
    before=hashlib.sha256(args.source.read_bytes()).hexdigest()
    doc=pdf.PdfDocument(args.source);pages=[];chosen={}
    for n in range(min(args.pages,len(doc))):
        page=doc[n];text=page.get_textpage();pages.append((page,text))
        for obj in page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text):
            char=obj.extract().strip()
            if char not in SYMBOLS or 'Chaconne' not in obj.get_font().get_base_name():continue
            matrix=obj.get_matrix()
            if abs(matrix.b)>1e-6 or abs(matrix.c)>1e-6:continue
            size=math.hypot(matrix.a,matrix.b)*obj.get_font_size()
            name,symbol,cp=SYMBOLS[char]
            # Prefer full-sized clefs, rather than a preceding change-clef.
            if name not in chosen or size>chosen[name][0]+.01:chosen[name]=(size,obj,page,n)
    if set(chosen)!=set(v[0] for v in SYMBOLS.values()):
        raise ValueError('Seven expected source symbols were not found; review source mapping')
    result=dict(source=str(args.source.resolve()),sha256=before,staff_space_pt=args.staff_space,
                bitmap_scale=args.scale,mode='Local raster-contour feasibility proof; not the original font',glyphs={})
    for char,(name,symbol,cp) in SYMBOLS.items():
        size,obj,page,n=chosen[name]
        raw=pdf.raw.FPDFTextObj_GetRenderedBitmap(doc,page,obj,args.scale)
        if not raw:raise RuntimeError('Text-object rasterization failed')
        bitmap=pdf.PdfBitmap.from_raw(raw);image=bitmap.to_pil().copy()
        # This API creates a caller-owned bitmap. All pixels were copied above.
        bitmap.warn_on_close=False
        bitmap.close()
        alpha=image.getchannel('A') if image.mode=='RGBA' else Image.eval(image.convert('L'),lambda x:255-x)
        loops=trace_pixels(np.asarray(alpha)>127)
        box=obj.get_bounds();matrix=obj.get_matrix();unit=250/args.staff_space
        outlines=[[[round((box[0]-matrix.e+x/args.scale)*unit,5),
                     round((box[3]-matrix.f-y/args.scale)*unit,5)] for x,y in loop] for loop in loops]
        raster=f'{name}-{args.scale:g}.png'
        image.save(args.output/raster)
        result['glyphs'][symbol]=dict(codepoint=cp,outlines=outlines,page=n+1,
            font_name=obj.get_font().get_base_name(),bounds_pt=box,origin_pt=[matrix.e,matrix.f],
            render_size_pt=size,raster=raster)
    assert hashlib.sha256(args.source.read_bytes()).hexdigest()==before,'Source changed during study'
    (args.output/'private-contour-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for page,text in pages:text.close();page.close()
    doc.close()
    print('Seven source objects rendered; original hash unchanged; no font program saved.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--staff-space',type=float,required=True,help='Measured source staff-space in PDF points')
    p.add_argument('--pages',type=int,default=3);p.add_argument('--scale',type=float,default=128)
    run(p.parse_args())
