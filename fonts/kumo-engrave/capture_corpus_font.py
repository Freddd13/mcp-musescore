"""Capture a local SMuFL study from catalogued user PDF objects, never FontFile.

Requires bundled Python. Source geometry is converted to 250 units/sp using
nominal font size/4, with explicit legacy baseline conversions. The seven prior
physically calibrated Sincerely shapes can be retained using --head-study.
"""
import argparse,collections,ctypes,hashlib,json,math
from pathlib import Path
import numpy as np
import pypdfium2 as pdf
from catalog_pdf_glyphs import render_character
from capture_pdf_reference import trace_pixels
from source.pdf_symbol_map import GLYPHS,COMPOUNDS,EMPTY,observed_codes


def box_of(loops):
    xs=[p[0] for v in loops for p in v];ys=[p[1] for v in loops for p in v]
    return [min(xs),min(ys),max(xs),max(ys)]


def clip_polygon(points,axis,value,keep_above):
    result=[]
    for a,b in zip(points[-1:]+points[:-1],points):
        inside_a=(a[axis]>=value) if keep_above else (a[axis]<=value)
        inside_b=(b[axis]>=value) if keep_above else (b[axis]<=value)
        if inside_a!=inside_b:
            t=(value-a[axis])/(b[axis]-a[axis]);result.append([a[j]+t*(b[j]-a[j]) for j in (0,1)])
        if inside_b:result.append(b)
    return result


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    cat=json.loads(args.catalog.read_text(encoding='utf-8'))
    sm=json.loads(args.glyphnames.read_text(encoding='utf-8'))
    unmapped=[k for k in cat if k.split('U+')[1] not in observed_codes()]
    assert not unmapped,unmapped
    result=dict(schema=1,mode='Local raster-derived corpus study; no source font program',
                scale=args.scale,sources={},glyphs={},compounds=COMPOUNDS,empty=sorted(EMPTY))
    old=json.loads(args.head_study.read_text(encoding='utf-8')) if args.head_study else None
    if old:
        assert hashlib.sha256(Path(old['source']).read_bytes()).hexdigest()==old['sha256'],'Prior calibration source changed'
        result['sources'][old['source']]=old['sha256']
    docs={};pages={};rasters={}
    for symbol,aliases,mode in GLYPHS:
        key='Chaconne:U+'+aliases.split()[0];item=cat[key];sample=item['sample']
        path=sample['source'];result['sources'][path]=sample['sha256']
        if path not in docs:
            assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sample['sha256']
            docs[path]=pdf.PdfDocument(path)
        doc=docs[path];pagekey=(path,sample['page'])
        if pagekey not in pages:
            page=doc[sample['page']-1];text=page.get_textpage()
            pages[pagekey]=(page,text,list(page.get_objects(filter=[pdf.raw.FPDF_PAGEOBJ_TEXT],textpage=text)))
        page,text,objects=pages[pagekey];obj=objects[sample['text_object_index']]
        if key not in rasters:
            im,box,origin=render_character(doc,page,text,obj,item['char'],args.scale)
            im.save(args.output/('source-'+aliases.split()[0]+'.png'))
            unit=250/item['nominal_space_pt'];mask=np.asarray(im.getchannel('A'))>127
            loops=trace_pixels(mask)
            outlines=[[[round((box[0]-origin[0]+x/args.scale)*unit,6),
                         round((box[3]-origin[1]-y/args.scale)*unit,6)] for x,y in loop] for loop in loops]
            rasters[key]=(outlines,box,origin)
        outlines,box,origin=rasters[key]
        outlines=[[[x,y] for x,y in loop] for loop in outlines]
        b=box_of(outlines);dx=dy=0;advance=None;notes=[];repeat=None
        if symbol=='metNote8thUp':
            # A085 p4 uses "ek": the next dot is inside e's declared charbox
            # because its flag overhangs the advance. Reject the separate dot
            # component, verified in the source page context; keep the note.
            dots=[v for v in outlines if box_of([v])[0]>325 and box_of([v])[3]<250]
            assert len(dots)==1,'Recheck the source overlap before changing capture'
            outlines=[v for v in outlines if v is not dots[0]];b=box_of(outlines)
            notes.append('Removed adjacent k dot from overlapping PDF character box (A085 p4 ek)')
        if mode=='center_y':dy=-(b[1]+b[3])/2
        elif mode=='center_xy':dx=-(b[0]+b[2])/2;dy=-(b[1]+b[3])/2
        elif mode=='bottom_zero':dy=-b[1]
        elif mode=='top_zero':dy=-b[3]
        elif mode=='flag_up':dy=10-b[3]
        elif mode=='flag_down':dy=-10-b[1]
        elif mode=='met_baseline':dy=-172-b[1]
        elif mode in ('arpeggio_rotate','repeat_wave'):
            # Measure source repetition from adjacent, same-baseline objects.
            groups=collections.defaultdict(list);vertical=mode=='arpeggio_rotate'
            for other in objects:
                if other.extract()!=item['char'] or other.get_font().get_base_name()!=sample['font']:continue
                m=other.get_matrix();groups[round(m.e if vertical else m.f,2)].append(m.f if vertical else m.e)
            # Trill repeats can be characters inside one text object.
            if not vertical:
                for i in range(text.count_chars()):
                    if pdf.raw.FPDFText_GetUnicode(text,i)!=ord(item['char']):continue
                    x,y=ctypes.c_double(),ctypes.c_double()
                    if pdf.raw.FPDFText_GetCharOrigin(text,i,ctypes.byref(x),ctypes.byref(y)):
                        groups[round(y.value,2)].append(x.value)
            gaps=[]
            for positions in groups.values():
                p=sorted(set(positions))
                gaps.extend((b-a)/item['nominal_space_pt'] for a,b in zip(p,p[1:]) if .5<(b-a)/item['nominal_space_pt']<1.6)
            if not gaps:raise ValueError('No observed repetition for '+symbol)
            count=collections.Counter(round(v,3) for v in gaps);repeat=count.most_common(1)[0][0]*250
            if vertical:
                # Two-cycle source glyph: keep an interior period plus overlap.
                # Crop only repeat overlap, never fit or replace the silhouette.
                lo=b[1]+(b[3]-b[1]-repeat)/2-15;hi=lo+repeat+30
                outlines=[clip_polygon(clip_polygon(v,1,lo,True),1,hi,False) for v in outlines]
                outlines=[v for v in outlines if len(v)>2]
                outlines=[[[y-lo,b[2]-x] for x,y in v] for v in outlines]
            else:
                # Horizontal trill segment already matches the engine direction.
                outlines=[[[x-b[0],y-b[1]] for x,y in v] for v in outlines]
            advance=int(round(repeat));notes.append('Measured repeat, overlap clipping requires native seam review')
        outlines=[[[x+dx,y+dy] for x,y in v] for v in outlines]
        calibration='nominal font size / 4'
        if old and symbol in old['glyphs']:
            outlines=old['glyphs'][symbol]['outlines'];calibration='prior physical source staff calibration'
            notes.append('Retains seven-glyph 0.401 study geometry')
        b=box_of(outlines)
        if advance is None:advance=int(math.ceil(b[2]))
        result['glyphs'][symbol]=dict(codepoint=int(sm[symbol]['codepoint'][2:],16),
            source_key=key,source=path,page=sample['page'],object_index=sample['text_object_index'],
            aliases=aliases.split(),mode=mode,calibration=calibration,nominal_space_pt=item['nominal_space_pt'],
            outlines=outlines,bounds=b,advance=advance,repeat=repeat,notes=notes)
        if old and symbol in old['glyphs']:
            result['glyphs'][symbol]['physical_calibration_source']=dict(source=old['source'],sha256=old['sha256'],
                page=old['glyphs'][symbol]['page'],bounds_pt=old['glyphs'][symbol]['bounds_pt'],
                origin_pt=old['glyphs'][symbol]['origin_pt'],staff_space_pt=old['staff_space_pt'])
    for path,expected in result['sources'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
    for page,text,objects in pages.values():text.close();page.close()
    for doc in docs.values():doc.close()
    (args.output/'capture.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Captured',len(result['glyphs']),'semantic glyphs; all catalog keys classified; source hashes unchanged.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'))
    p.add_argument('--head-study',type=Path);p.add_argument('--scale',type=float,default=128)
    run(p.parse_args())
