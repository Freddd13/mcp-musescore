"""Read-only staff-grid measurements and context panels for path candidates."""
import argparse,collections,hashlib,json
from pathlib import Path
import pypdfium2 as pdf
from PIL import Image,ImageDraw,ImageFont
from source.path_geometry import nearest_grid


def staff_grids(paths):
    rectangles=collections.defaultdict(list)
    for item in paths:
        points=[];curved=False
        for op,values in item['commands']+[('closePath',[])]:
            if op=='moveTo':points=list(values);curved=False
            elif op=='lineTo':points.extend(values)
            elif op=='curveTo':curved=True
            elif op=='closePath':
                if points and not curved:
                    xs=[p[0] for p in points];ys=[p[1] for p in points]
                    a,b,c,d=min(xs),min(ys),max(xs),max(ys)
                    if c-a>150 and 0<d-b<.5:
                        rectangles[(item['page'],round(a,1),round(c,1))].append((b+d)/2)
                points=[]
    grids=[]
    for (page,left,right),values in rectangles.items():
        runs=[]
        for value in sorted(set(round(v,5) for v in values)):
            if not runs or value-runs[-1][-1]>8:runs.append([])
            runs[-1].append(value)
        for ys in runs:
            if len(ys)!=5:continue
            gaps=[b-a for a,b in zip(ys,ys[1:])]
            if min(gaps)<2.5 or max(gaps)-min(gaps)>.3:continue
            # Use all five line centres, not the most frequent quantized gap.
            mean=sum(ys)/5;step=sum((i-2)*(y-mean) for i,y in enumerate(ys))/10
            grids.append(dict(page=page,x=[left,right],line_centres_pt=ys,space_pt=step,
                              fitted_bottom_pt=mean-2*step,max_residual_pt=max(abs(y-(mean+(i-2)*step)) for i,y in enumerate(ys))))
    return grids


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);data=json.loads(args.paths.read_text(encoding='utf-8'))
    grids=staff_grids(data['paths']);assert grids
    print('Five-line staff grids',len(grids),'spaces',dict(collections.Counter(round(g['space_pt'],3) for g in grids)))
    (args.output/'staff-grids.json').write_text(json.dumps(grids,indent=2)+'\n',encoding='utf-8')
    if not args.selection:return
    selection=json.loads(args.selection.read_text(encoding='utf-8'));rows=selection['rows']
    by_key={(p['page'],p['object_index']):p for p in data['paths']};source=Path(data['source'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256'];doc=pdf.PdfDocument(source)
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);result=[]
    for start in range(0,len(rows),12):
        board=Image.new('RGB',(1800,1600),'white');draw=ImageDraw.Draw(board)
        for i,row in enumerate(rows[start:start+12]):
            item=by_key[(row['page'],row['object_index'])];page=doc[item['page']-1];w,h=page.get_size()
            a,b,c,d=item['bounds_pt'];a=max(0,a-28);b=max(0,b-21);c=min(w,c+28);d=min(h,d+21)
            bitmap=page.render(scale=5,crop=(a,b,w-c,h-d));image=bitmap.to_pil().copy().convert('RGB');bitmap.close()
            image.thumbnail((580,330));x=i%3*600;y=i//3*400;board.paste(image,(x,y+55))
            draw.text((x+5,y+5),row['role_candidate']+' p%d obj%d'%(row['page'],row['object_index']),font=label,fill='black')
            g=nearest_grid(item,grids);draw.text((x+5,y+28),'staff %.4f pt'%g['space_pt'],font=label,fill='black')
            result.append(dict(**row,grid=g));page.close()
        board.save(args.output/('contexts-%02d.png'%(start//12+1)))
    doc.close();assert hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256']
    (args.output/'contexts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--paths',type=Path,required=True)
    p.add_argument('--selection',type=Path);p.add_argument('--output',type=Path,required=True);run(p.parse_args())
