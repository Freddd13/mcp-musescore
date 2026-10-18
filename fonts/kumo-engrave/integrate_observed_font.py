"""Integrate reviewed character/page curves and explicit derived variants.

Requires fontTools. Geometry remains local; source/derivation decisions live in
source/observed_roles.json. Brace x compression compensates the native two-staff
3.625 multiplier, while its 4-sp height matches the host's 100-unit brace box.
"""
import argparse,copy,hashlib,json,math
from pathlib import Path
from capture_vector_font import apply_geometry,exact_bounds,transform
from source.path_geometry import contours,nearest_grid
from source.symbol_names import load_symbol_names

ROOT=Path(__file__).resolve().parent


def normalize(commands,mode):
    b=exact_bounds(commands);dx=-b[0];dy=0
    if mode=='center_y':dy=-(b[1]+b[3])/2
    elif mode=='center_xy':dx=-(b[0]+b[2])/2;dy=-(b[1]+b[3])/2
    elif mode=='bottom_zero':dy=-b[1]
    elif mode=='top_zero':dy=-b[3]
    elif mode=='flag_up':dy=10-b[3]
    elif mode=='flag_down':dy=-10-b[1]
    elif mode=='met_baseline':dy=-172-b[1]
    elif mode=='head':dy=-(b[1]+b[3])/2
    return transform(commands,lambda x,y:(x+dx,y+dy))


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads(args.base.read_text(encoding='utf-8'));raw=json.loads(args.observed.read_text(encoding='utf-8'))
    spec=json.loads(args.spec.read_text(encoding='utf-8'));sm=load_symbol_names(args.glyphnames)
    paths=json.loads(args.paths.read_text(encoding='utf-8'));grids=json.loads(args.grids.read_text(encoding='utf-8'))
    meta=json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))
    by_key={(v['page'],v['object_index']):v for v in paths['paths']};rows=[]
    data['sources'].update(raw['sources']);data['sources'][paths['source']]=paths['sha256']
    def install(name,commands,**provenance):
        replacing=provenance.pop('replacing',False)
        assert (name in data['glyphs'])==replacing,name
        previous=copy.deepcopy(data['glyphs'].get(name))
        cp=previous['codepoint'] if previous else int(sm[name]['codepoint'][2:],16)
        item=dict(codepoint=cp,smufl=name in sm,usage=previous.get('usage','standard') if previous else 'standard',**provenance)
        apply_geometry(item,commands);data['glyphs'][name]=item
        if previous:item['previous_shape_reference']=dict(source_key=previous.get('source_key'),bounds=previous['bounds'],mode=previous['mode'])
        rows.append(dict(symbol=name,bounds_sp=[v/250 for v in item['bounds']],cubic_segments=sum(op=='curveTo' for op,pts in commands),**provenance))
    for row in raw['rows']:
        choice=row['choice'];name=choice['symbol'];unit=250/row['staff_space_pt']
        if row.get('rejected') or choice.get('capture_only'):continue
        if 'world_commands' in row:
            origin=row['origin_pt'];commands=transform(row['world_commands'],lambda x,y:((x-origin[0])*unit,(y-origin[1])*unit))
        elif 'commands' in row:
            m=row['matrix'];factor=math.hypot(m[0],m[1])*row['font_size']*unit
            if choice.get('calibration')=='nominal':factor=1000
            commands=transform(row['commands'],lambda x,y:(x*factor,y*factor))
        else:
            commands=[]
            for loop in row['raster_outlines']:
                commands.extend([['moveTo',[loop[0]]]]+[['lineTo',[p]] for p in loop[1:]]+[['closePath',[]]])
        commands=normalize(commands,choice['mode'])
        if choice.get('replace'):
            old=data['glyphs'][name];b=exact_bounds(commands)
            commands=transform(commands,lambda x,y:(x+old['bounds'][0]-b[0],y))
        install(name,commands,source=row['source'],source_sha256=row['source_sha256'],page=row['page'],
                source_key=choice.get('group'),object_indices=row.get('object_indices',[row.get('object_index')]),
                mode='displayed_curve_assembly' if 'world_commands' in row else 'observed_render_fallback' if 'raster_outlines' in row else 'observed_character_curves',
                route=choice.get('route','native music/Text symbol'),staff_space_pt=row['staff_space_pt'],replacing=choice.get('replace',False))
        if name=='wiggleGlissando':
            period=round(row['source_advance']*math.hypot(row['matrix'][0],row['matrix'][1])*unit)
            assert period>0;data['glyphs'][name].update(advance=period,repeat=period)
    for derived in spec['derived']:
        if not derived.get('reflect_y'):continue
        parent=data['glyphs'][derived['from']]
        install(derived['symbol'],transform(parent['commands'],lambda x,y:(x,-y)),mode='reflected_matching_articulation',
                source=parent['source'],source_sha256=parent['source_sha256'],page=parent['page'],derived_from=derived['from'])
    for choice in spec.get('page_components',[]):
        parent=data['glyphs'][choice['parent']];parts=contours(parent['commands'])
        commands=[c for i in choice['contours'] for c in parts[i]];b=exact_bounds(commands)
        install(choice['symbol'],transform(commands,lambda x,y:(x-b[0],y)),mode='existing_page_curve_component',
                source=paths['source'],source_sha256=paths['sha256'],page=choice['page'],object_index=choice['object_index'],
                contour_indices=choice['contours'],derived_from=choice['parent'])
    if spec.get('repeat_dot'):
        choice=spec['repeat_dot'];member=by_key[(choice['page'],choice['object_index'])];grid=nearest_grid(member,grids)
        unit=250/grid['space_pt'];commands=normalize(transform(member['commands'],lambda x,y:(x*unit,y*unit)),'center_y')
        install('repeatDot',commands,mode='repeat_barline_page_curves',source=paths['source'],source_sha256=paths['sha256'],
                page=choice['page'],object_index=choice['object_index'],staff_space_pt=grid['space_pt'])
    if spec.get('brace'):
        choice=spec['brace'];members=[by_key[(choice['page'],i)] for i in choice['objects']]
        commands=[c for v in members for c in v['commands']];b=exact_bounds(commands);grid=nearest_grid(members[0],grids)
        reference_width=(b[2]-b[0])*250/grid['space_pt']/choice['two_staff_magnification']
        old=meta['glyphBBoxes']['brace'];old_width=old['bBoxNE'][0]-old['bBoxSW'][0]
        for name in choice['variants']:
            v=meta['glyphBBoxes'][name];ratio=(v['bBoxNE'][0]-v['bBoxSW'][0])/old_width
            shaped=transform(commands,lambda x,y:((x-b[0])*reference_width*ratio/(b[2]-b[0]),(y-b[1])*choice['nominal_height_units']/(b[3]-b[1])))
            install(name,shaped,mode='native_brace_coordinate_adaptation',source=paths['source'],source_sha256=paths['sha256'],
                    page=choice['page'],object_indices=choice['objects'],staff_space_pt=grid['space_pt'],source_bounds_pt=b,
                    two_staff_magnification=choice['two_staff_magnification'],baseline_width_ratio=ratio,
                    notes=['One observed two-half brace; size variants derived with Leland width ratios, not four separately recovered source designs'])
    for path,sha in data['sources'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
    if data.get('observed_study'):data.setdefault('observed_study_history',[]).append(data['observed_study'])
    data.update(version=spec['version'],observed_study=dict(spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest(),
                raw_capture_sha256=hashlib.sha256(args.observed.read_bytes()).hexdigest(),rows=rows))
    (args.output/'capture.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (args.output/'report.json').write_text(json.dumps(data['observed_study'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Integrated',len(rows),'total',len(data['glyphs']),'source hashes unchanged')
    for row in rows:print(row['symbol'],row['cubic_segments'],[round(v,3) for v in row['bounds_sp']])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--observed',type=Path,required=True)
    p.add_argument('--paths',type=Path,default=ROOT/'dist/A064-paths-03/paths.json');p.add_argument('--grids',type=Path,default=ROOT/'dist/vector-context-059/staff-grids.json')
    p.add_argument('--spec',type=Path,default=ROOT/'source/observed_roles.json');p.add_argument('--output',type=Path,required=True)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'));run(p.parse_args())
