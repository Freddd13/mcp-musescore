"""Geometry checks for the authored cubic notehead contours, without raster fit."""
def sample_contours(recording, steps=64):
    result=[];points=[];last=None
    for op,args in recording.value:
        if op=='moveTo':
            points=[args[0]];last=args[0]
        elif op=='lineTo':points.append(args[0]);last=args[0]
        elif op=='curveTo':
            a,b,c=args;p=last
            for i in range(1,steps+1):
                t=i/steps;s=1-t
                points.append(tuple(s**3*p[j]+3*s*s*t*a[j]+3*s*t*t*b[j]+t**3*c[j] for j in (0,1)))
            last=c
        elif op=='closePath':
            result.append(points);points=[]
        else:raise ValueError(op)
    return result


def vertical_edges(points,x):
    hits=[]
    for a,b in zip(points,points[1:]+points[:1]):
        if min(a[0],b[0])<=x<=max(a[0],b[0]) and a[0]!=b[0]:
            hits.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
    assert len(hits)>=2,(x,hits)
    return min(hits),max(hits)


def inside(points,p):
    x,y=p;crossings=0
    for a,b in zip(points,points[1:]+points[:1]):
        if (a[1]>y)!=(b[1]>y):
            edge=a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1])
            if edge>x:crossings+=1
    return crossings%2==1


def area(points):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1]))/2


def filled_intervals(loops,x):
    """Vertical ink spans using nonzero winding, so overlaps stay filled."""
    hits=[]
    for points in loops:
        for a,b in zip(points,points[1:]+points[:1]):
            if min(a[0],b[0])<=x<max(a[0],b[0]):hits.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
    def winding(p):
        xx,y=p;total=0
        for points in loops:
            for a,b in zip(points,points[1:]+points[:1]):
                cross=(b[0]-a[0])*(y-a[1])-(xx-a[0])*(b[1]-a[1])
                if a[1]<=y<b[1] and cross>0:total+=1
                elif b[1]<=y<a[1] and cross<0:total-=1
        return total
    ys=sorted(set(hits));spans=[]
    for lo,hi in zip(ys,ys[1:]):
        if hi-lo>1e-8 and winding((x,(lo+hi)/2)):
            if spans and abs(spans[-1][1]-lo)<1e-8:spans[-1]=(spans[-1][0],hi)
            else:spans.append((lo,hi))
    assert spans,('No ink at x',x)
    return spans
