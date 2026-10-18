"""Staff lookup and cubic-preserving clipping for local page-path studies."""


def nearest_grid(item,grids):
    a,b,c,d=item['bounds_pt'];x=(a+c)/2;y=(b+d)/2
    same=[g for g in grids if g['page']==item['page'] and g['x'][0]-20<x<g['x'][1]+20]
    assert same,('No measured grid',item['page'],item['object_index'])
    return min(same,key=lambda g:min(abs(y-v) for v in g['line_centres_pt']))


def contours(commands):
    result=[];active=[]
    for op,points in commands:
        if op=='moveTo' and active:
            if active[-1][0]!='closePath':active.append(('closePath',[]))
            result.append(active);active=[]
        active.append((op,[tuple(p) for p in points]))
        if op=='closePath':result.append(active);active=[]
    if active:
        active.append(('closePath',[]));result.append(active)
    return result


def clip_cubics(commands,axis,value,keep_above):
    """Clip closed cubic contours to one half-plane without raster tracing.

    Split at every real cubic/plane intersection, retain inside fragments,
    and connect exits to entries on the clipping plane. Multiple source
    contours keep their winding, including overlaps and counter-contours.
    """
    from fontTools.misc.bezierTools import solveCubic,splitCubicAtT
    output=[]
    for contour in contours(commands):
        start=last=None;segments=[]
        for op,points in contour:
            if op=='moveTo':start=last=points[0]
            elif op in ('lineTo','curveTo'):
                segments.append((op,[last]+points));last=points[-1]
            elif op=='closePath' and last!=start:
                segments.append(('lineTo',[last,start]))
        kept=[]
        for op,points in segments:
            if op=='lineTo':
                a,b=points;delta=b[axis]-a[axis]
                cuts=[(value-a[axis])/delta] if delta and min(a[axis],b[axis])<value<max(a[axis],b[axis]) else []
                ts=[0]+cuts+[1];parts=[]
                for lo,hi in zip(ts,ts[1:]):
                    parts.append([tuple(a[j]+(b[j]-a[j])*t for j in (0,1)) for t in (lo,hi)])
            else:
                p0,p1,p2,p3=[p[axis] for p in points]
                roots=solveCubic(-p0+3*p1-3*p2+p3,3*p0-6*p1+3*p2,-3*p0+3*p1,p0-value)
                cuts=sorted(set(t for t in roots if 1e-9<t<1-1e-9))
                parts=splitCubicAtT(*points,*cuts) if cuts else [points]
            for part in parts:
                middle=(part[0][axis]+part[-1][axis])/2 if op=='lineTo' else sum(a*p[axis] for a,p in zip((1,3,3,1),part))/8
                within=(middle>=value-1e-8) if keep_above else (middle<=value+1e-8)
                if within:kept.append((op,part))
        if not kept:continue
        output.append(('moveTo',[kept[0][1][0]]));last=kept[0][1][0]
        for op,points in kept:
            if max(abs(a-b) for a,b in zip(last,points[0]))>1e-8:output.append(('lineTo',[points[0]]))
            output.append((op,points[1:]));last=points[-1]
        output.append(('closePath',[]))
    return output
