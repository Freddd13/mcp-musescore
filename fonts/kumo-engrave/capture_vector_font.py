"""Adapt reviewed PDF page curves to the local score font; retain cubic paths.

Requires fontTools. No PDF/font program is saved or modified. Shape scale is
uniform and follows measured staff geometry; source tempo scaling and baseline
adaptation are explicit. References and generated font outlines stay local.
"""
import argparse,copy,hashlib,json,math
from pathlib import Path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from source.contours import sample_contours,area
from source.path_geometry import nearest_grid,contours,clip_cubics

ROOT=Path(__file__).resolve().parent


def recording(commands):
    pen=RecordingPen()
    for op,points in commands:getattr(pen,op)(*[tuple(p) for p in points])
    return pen


def exact_bounds(commands):
    pen=BoundsPen(None,ignoreSinglePoints=True);recording(commands).replay(pen);assert pen.bounds
    return list(pen.bounds)


def transform(commands,func):
    return [(op,[[round(v,6) for v in func(x,y)] for x,y in points]) for op,points in commands]


def apply_geometry(item,commands,**fields):
    box=exact_bounds(commands);loops=sample_contours(recording(commands),steps=96)
    loops=sorted((v for v in loops if len(v)>2),key=lambda v:-abs(area(v)))
    assert loops
    item.update(commands=commands,outlines=loops,bounds=box,advance=int(math.ceil(box[2])),repeat=None,**fields)


def component(commands,which):
    parts=contours(commands);boxes=[exact_bounds(v) for v in parts]
    left=min(range(len(parts)),key=lambda i:boxes[i][0]);right=max(range(len(parts)),key=lambda i:boxes[i][2])
    assert left!=right
    selected=[left] if which=='left' else [right] if which=='right' else [i for i in range(len(parts)) if i not in (left,right)]
    assert selected
    return [c for i in selected for c in parts[i]],selected


def line_fit(values):
    mean=sum(values)/len(values);mid=(len(values)-1)/2
    return sum((i-mid)*(v-mean) for i,v in enumerate(values))/sum((i-mid)**2 for i in range(len(values)))


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.capture.read_text(encoding='utf-8'));paths=json.loads(args.paths.read_text(encoding='utf-8'))
    spec=json.loads(args.spec.read_text(encoding='utf-8'));grids=json.loads(args.grids.read_text())
    assert paths['sha256']==spec['source_sha256'];source=Path(paths['source'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==paths['sha256']
    data['sources'][str(source)]=paths['sha256']
    by_key={(v['page'],v['object_index']):v for v in paths['paths']};rows=[]
    pair=spec['trill_pair'];tr=by_key[(pair['page'],pair['start'])]
    tr_grid=nearest_grid(tr,grids);tr_unit=250/tr_grid['space_pt']
    # An arbitrary source Text origin is unavailable after outlining. Keep the
    # established tr baseline, then preserve the source tr/wave relationship.
    tr_origin=exact_bounds(tr['commands'])[1]-data['glyphs']['ornamentTrill']['bounds'][1]/tr_unit
    for choice in spec['glyphs']:
        name=choice['symbol'];item=by_key[(choice['page'],choice['object_index'])];g=nearest_grid(item,grids)
        commands=item['commands']
        selected_contours=None
        if choice.get('component'):commands,selected_contours=component(commands,choice['component'])
        b=exact_bounds(commands);old=copy.deepcopy(data['glyphs'][name]);unit=250/g['space_pt']/choice['render_scale']
        dx=old['bounds'][0]-b[0]*unit;mode=choice['baseline']
        if mode=='center_y':dy=(old['bounds'][1]+old['bounds'][3])/2-(b[1]+b[3])*unit/2
        elif mode=='align_top':dy=old['bounds'][3]-b[3]*unit
        elif mode=='g_staff_line':dy=-g['line_centres_pt'][1]*unit
        elif mode=='f_staff_line':dy=-g['line_centres_pt'][3]*unit
        elif mode=='paired_trill':dy=-tr_origin*unit
        else:dy=old['bounds'][1]-b[1]*unit
        commands=transform(commands,lambda x,y:(x*unit+dx,y*unit+dy))
        target=data['glyphs'][name]
        target['previous_shape_reference']=dict(source=old.get('source'),source_key=old.get('source_key'),bounds=old['bounds'])
        for field in ('physical_calibration_source','aliases','source_text','nominal_space_pt','used_space_pt'):target.pop(field,None)
        apply_geometry(target,commands,mode='source_page_curves',source=str(source),source_sha256=paths['sha256'],
            page=choice['page'],object_index=choice['object_index'],source_key='A064:p%d:path%d'%(choice['page'],choice['object_index']),
            calibration=dict(staff_space_pt=g['space_pt'],render_scale=choice['render_scale'],baseline=mode),
            notes=['Retained original page cubic/line geometry, uniform scale; stated SMuFL baseline adaptation'])
        if name=='ornamentTrill':
            first=by_key[(pair['page'],pair['waves'][0])]
            desired=old['bounds'][0]+(exact_bounds(first['commands'])[0]-b[0])*unit
            target['advance']=round(desired-data['glyphs']['wiggleTrill']['bounds'][0])
        if name=='wiggleTrill':
            positions=[exact_bounds(by_key[(pair['page'],i)]['commands'])[0] for i in pair['waves']]
            target['advance']=round(line_fit(positions)*unit);target['repeat']=target['advance']
        rows.append(dict(symbol=name,page=choice['page'],object_index=choice['object_index'],component=choice.get('component'),
            source_bounds_pt=b,source_contour_indices=selected_contours,
            staff_space_pt=g['space_pt'],render_scale=choice['render_scale'],baseline=mode,
            bounds_sp=[v/250 for v in target['bounds']],previous_bounds_sp=[v/250 for v in old['bounds']],
            cubic_segments=sum(op=='curveTo' for op,pts in commands)))
    # Preserve the actual overlapping source-g run as several same-winding
    # contours, then clip an interior period without flattening the curves.
    arp=spec['arpeggio'];members=[by_key[(arp['page'],i)] for i in arp['objects']]
    members.sort(key=lambda v:exact_bounds(v['commands'])[1]);g=nearest_grid(members[len(members)//2],grids)
    positions=[exact_bounds(v['commands'])[1] for v in members];period=line_fit(positions)
    start=positions[len(positions)//2]+period*.5;lo=start-.06*g['space_pt'];hi=start+period+.06*g['space_pt']
    commands=[cmd for member in members for cmd in member['commands']]
    commands=clip_cubics(clip_cubics(commands,1,lo,True),1,hi,False);b=exact_bounds(commands)
    advance=round(period/g['space_pt']*250)
    commands=transform(commands,lambda x,y:((y-start)*advance/period,(b[2]-x)*250/g['space_pt']))
    for name in ('wiggleArpeggiatoUp','wiggleArpeggiatoDown'):
        apply_geometry(data['glyphs'][name],copy.deepcopy(commands),mode='source_page_curve_union',source=str(source),source_sha256=paths['sha256'],
            page=arp['page'],object_indices=arp['objects'],source_key='A064:overlapping-arpeggio-paths',calibration=dict(staff_space_pt=g['space_pt'],source_period_pt=period),
            notes=['Overlapping source page contours, cubic-preserving half-plane clip, integer advance'])
        data['glyphs'][name].update(advance=advance,repeat=advance)
        rows.append(dict(symbol=name,page=arp['page'],object_indices=arp['objects'],staff_space_pt=g['space_pt'],source_period_pt=period,
            source_bounds_pt=b,source_clip_bounds_pt=[b[0],lo,b[2],hi],rotate_clockwise=True,render_scale=1,
            bounds_sp=[v/250 for v in data['glyphs'][name]['bounds']],cubic_segments=sum(op=='curveTo' for op,pts in commands)))
    for derived in spec['derived']:
        target=data['glyphs'][derived['symbol']];parent=data['glyphs'][derived['from_symbol']]
        commands=transform(parent['commands'],lambda x,y:(x,-y))
        apply_geometry(target,commands,mode='reflected_page_curves',source_key='derived:'+derived['from_symbol'],
            source=parent['source'],source_sha256=parent['source_sha256'],page=parent['page'],object_index=parent['object_index'],
            notes=['Reflected reviewed upper fermata to maintain the observed matching lower form'])
        parent_row=next(r for r in rows if r['symbol']==derived['from_symbol'])
        rows.append(dict(symbol=derived['symbol'],derived_from=derived['from_symbol'],page=parent_row['page'],object_index=parent_row['object_index'],
            staff_space_pt=parent_row['staff_space_pt'],source_bounds_pt=parent_row['source_bounds_pt'],render_scale=1,reflect_y=True,
            bounds_sp=[v/250 for v in target['bounds']],cubic_segments=sum(op=='curveTo' for op,pts in commands)))
    assert hashlib.sha256(source.read_bytes()).hexdigest()==paths['sha256']
    data.update(version=spec['version'],vector_study=dict(source=str(source),sha256=paths['sha256'],spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest(),rows=rows))
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (args.output/'report.json').write_text(json.dumps(data['vector_study'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for row in rows:print(row['symbol'],'curves',row['cubic_segments'],'bounds sp',[round(v,3) for v in row['bounds_sp']])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True)
    p.add_argument('--paths',type=Path,required=True);p.add_argument('--grids',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--spec',type=Path,default=ROOT/'source/vector_roles.json');run(p.parse_args())
