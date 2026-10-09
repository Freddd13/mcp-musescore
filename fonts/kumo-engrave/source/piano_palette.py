"""Independent vector studies after observation of printed piano scores.

Coordinates are design decisions in 250 units/staff-space, not PDF contours.
Ribbons sample authored cubic centerlines; polygons are normalized CCW so
overlapping strokes fill without cancellation. No embedded fonts are read.
"""
import math


def polygon(pen, points):
    area = sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points, points[1:]+points[:1]))
    if area < 0:
        points = list(reversed(points))
    pen.moveTo(points[0])
    for point in points[1:]:
        pen.lineTo(point)
    pen.closePath()


def disk(pen, x, y, rx, ry=None, shear=0):
    ry = rx if ry is None else ry
    k = .5522847498307936
    def p(a,b):
        return (x+rx*a, y+ry*b+shear*rx*a)
    pen.moveTo(p(1,0))
    for points in [((1,k),(k,1),(0,1)),((-k,1),(-1,k),(-1,0)),
                   ((-1,-k),(-k,-1),(0,-1)),((k,-1),(1,-k),(1,0))]:
        pen.curveTo(*(p(*q) for q in points))
    pen.closePath()


def ribbon(pen, start, segments):
    """Cubic centerline with start/end thickness; 48 samples per segment."""
    points, widths = [], []
    p0 = start
    for c1,c2,end,w0,w1 in segments:
        for i in range(49):
            if points and i == 0:
                continue
            t = i/48
            s = 1-t
            points.append(tuple(s*s*s*p0[j]+3*s*s*t*c1[j]+3*s*t*t*c2[j]+t*t*t*end[j] for j in [0,1]))
            widths.append(w0+(w1-w0)*(3*t*t-2*t*t*t))
        p0 = end
    left,right = [],[]
    for i,(x,y) in enumerate(points):
        a,b = points[max(0,i-1)],points[min(len(points)-1,i+1)]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        nx,ny=-dy/length*widths[i]/2,dx/length*widths[i]/2
        left.append((x+nx,y+ny)); right.append((x-nx,y-ny))
    polygon(pen,left+right[::-1])


def flat(pen, shift=0):
    # Thin ascender, bowed shoulder, sharp lower return; counter is open.
    polygon(pen,[(shift+7,-150),(shift+7,428),(shift+35,433),(shift+35,-123)])
    ribbon(pen,(shift+24,-142),[
        ((shift+66,-116),(shift+195,-14),(shift+170,80),30,56),
        ((shift+149,156),(shift+57,105),(shift+28,56),56,19)])


def rest_short(pen,count):
    # Each additional hook is a quarter-space-stepped diagonal branch.
    top = 178 if count < 3 else 428
    end = -235 if count < 2 else (-493 if count < 4 else -735)
    maxx = 250+(count-1)*63
    ribbon(pen,(maxx-7,top),[((maxx-53,top-95),(maxx-105,end+80),(maxx-130,end),24,22)])
    for i in range(count):
        y = top-65-i*250
        x = maxx-147-i*58
        disk(pen,x,y,48,52,-.08)
        ribbon(pen,(x-18,y-5),[((x+35,y-87),(x+90,y-64),(maxx-7-i*61,top-i*250),24,19)])


def draw(spec, advance):
    from fontTools.pens.recordingPen import RecordingPen
    pen=RecordingPen()
    kind=spec['drawing']
    if kind == 'gClef':
        # Tail through upper loop, then broad outer spiral and fine inner curl.
        ribbon(pen,(312,-605),[
            ((350,-340),(310,297),(273,590),31,30),
            ((239,920),(334,1150),(415,1100),30,52),
            ((518,960),(246,498),(112,268),52,62),
            ((-80,-44),(42,-321),(326,-290),62,42),
            ((620,-267),(680,62),(455,140),42,97),
            ((253,211),(165,-1),(270,-98),97,22),
            ((316,-145),(386,-108),(408,-43),22,16)])
        ribbon(pen,(312,-605),[((276,-750),(72,-698),(122,-580),31,20)])
        disk(pen,148,-598,67,72)
    elif kind == 'fClef':
        disk(pen,93,85,91,90)
        ribbon(pen,(102,143),[
            ((299,330),(496,198),(400,-65),35,99),
            ((344,-275),(177,-461),(4,-530),99,13)])
        disk(pen,586,124,41); disk(pen,586,-124,41)
    elif kind == 'restQuarter':
        # Angular upper zigzag, narrow waist, lower hooked terminal.
        pen.moveTo((94,390))
        pen.curveTo((121,354),(155,319),(186,286))
        pen.lineTo((109,157)); pen.lineTo((214,4))
        pen.curveTo((151,39),(85,36),(72,-27))
        pen.curveTo((32,-125),(94,-264),(165,-337))
        pen.lineTo((149,-358))
        pen.curveTo((27,-244),(-26,-77),(25,0))
        pen.curveTo((46,45),(87,65),(115,61))
        pen.lineTo((32,177)); pen.lineTo((126,309))
        pen.lineTo((73,375)); pen.closePath()
    elif kind == 'shortRest':
        rest_short(pen,spec['count'])
    elif kind == 'blockRest':
        y=110 if spec['half'] else -110
        polygon(pen,[(0,0),(318,0),(318,y),(0,y)])
    elif kind == 'sharp':
        for x in [62,168]:
            polygon(pen,[(x-11,-332),(x+11,-318),(x+11,334),(x-11,320)])
        for y in [-137,128]:
            polygon(pen,[(0,y-49),(238,y+11),(238,y+88),(0,y+28)])
    elif kind == 'natural':
        polygon(pen,[(0,-129),(25,-121),(25,376),(0,382)])
        polygon(pen,[(136,-378),(161,-384),(161,123),(136,115)])
        for y in [-128,97]:
            polygon(pen,[(0,y-12),(161,y+28),(161,y+83),(0,y+43)])
    elif kind == 'flat':
        flat(pen)
    elif kind == 'doubleFlat':
        flat(pen); flat(pen,225)
    elif kind == 'doubleSharp':
        polygon(pen,[(0,-121),(73,-121),(126,-31),(179,-121),(252,-121),(252,-55),
                     (163,3),(252,63),(252,129),(180,129),(126,38),(73,129),(0,129),
                     (0,62),(88,3),(0,-55)])
    elif kind == 'arpeggio':
        # Engine rotates and repeats horizontal glyphs by advance. Endpoints
        # meet at x=advance; equal position AND tangent prevent seam notches.
        arrow=spec.get('arrow',False)
        period=220 if arrow else advance
        length=advance-85 if arrow else advance
        height=50
        points=[]
        for i in range(129):
            x=length*i/128
            y=65+height*math.sin(2*math.pi*x/period)
            slope=height*2*math.pi/period*math.cos(2*math.pi*x/period)
            norm=math.hypot(1,slope)
            points.append(((x-slope*15/norm,y+15/norm),(x+slope*15/norm,y-15/norm)))
        polygon(pen,[p[0] for p in points]+[p[1] for p in points[::-1]])
        if arrow:
            endpoint=65+height*math.sin(2*math.pi*length/period)
            ribbon(pen,(length,endpoint),[((length+16,endpoint),(advance-55,65),(advance-27,65),30,23)])
            polygon(pen,[(advance-120,-55),(advance,65),(advance-120,185),(advance-88,65)])
    elif kind == 'flag':
        pen.moveTo((0,10))
        pen.curveTo((15,-137),(195,-171),(234,-350))
        pen.curveTo((263,-511),(166,-650),(128,-747))
        pen.lineTo((111,-742))
        pen.curveTo((165,-592),(258,-401),(163,-285))
        pen.curveTo((96,-221),(8,-190),(0,-169)); pen.closePath()
        if spec.get('count',1)>1:
            ribbon(pen,(12,-182),[((90,-316),(243,-313),(192,-524),84,14)])
        if spec.get('down'):
            transformed=RecordingPen()
            for op,args in pen.value:
                getattr(transformed,op)(*(tuple((x,-y) for x,y in args)))
            pen=transformed
    elif kind == 'dot':
        radius=min(45,advance*.45)
        disk(pen,advance/2,0 if spec.get('centered') else radius,radius)
    elif kind == 'accent':
        polygon(pen,[(0,0),(advance,95),(0,190),(0,167),(advance-48,95),(0,23)])
    elif kind == 'tenuto':
        polygon(pen,[(0,0),(advance,0),(advance,27),(0,27)])
    elif kind == 'marcato':
        polygon(pen,[(0,0),(advance/2,240),(advance,0),(advance-33,0),
                     (advance/2-6,190),(19,0)])
    elif kind == 'staccatissimo':
        polygon(pen,[(advance/2,0),(advance,231),(0,231)])
    elif kind == 'fermata':
        ribbon(pen,(17,22),[
            ((34.5,221),((advance+69)/4,320.5),(advance/2,320.5),27,55),
            (((3*advance-69)/4,320.5),(advance-34.5,221),(advance-17,22),55,27)])
        disk(pen,advance/2,49,42)
    else:
        raise ValueError(kind)
    if spec.get('below'):
        transformed=RecordingPen()
        for op,args in pen.value:
            getattr(transformed,op)(*(tuple((x,-y) for x,y in args)))
        pen=transformed
    return pen


def specs():
    result={}
    def add(name,cp,kind,**kw):
        result[name]=dict(codepoint=cp,drawing=kind,**kw)
    add('gClef','E050','gClef'); add('fClef','E062','fClef')
    add('restWhole','E4E3','blockRest',half=False); add('restHalf','E4E4','blockRest',half=True)
    add('restQuarter','E4E5','restQuarter')
    for count,(name,cp) in enumerate([('rest8th','E4E6'),('rest16th','E4E7'),('rest32nd','E4E8'),('rest64th','E4E9')],1):
        add(name,cp,'shortRest',count=count)
    for name,cp,kind in [('accidentalSharp','E262','sharp'),('accidentalNatural','E261','natural'),
                         ('accidentalFlat','E260','flat'),('accidentalDoubleFlat','E264','doubleFlat'),
                         ('accidentalDoubleSharp','E263','doubleSharp')]:
        add(name,cp,kind)
    for name,cp,arrow in [('wiggleArpeggiatoUp','EAA9',False),('wiggleArpeggiatoDown','EAAA',False),
                           ('wiggleArpeggiatoUpArrow','EAAD',True),('wiggleArpeggiatoDownArrow','EAAE',True)]:
        add(name,cp,'arpeggio',arrow=arrow)
    for name,cp,down,count in [('flag8thUp','E240',False,1),('flag8thDown','E241',True,1),
                              ('flag16thUp','E242',False,2),('flag16thDown','E243',True,2)]:
        add(name,cp,'flag',down=down,count=count)
    add('augmentationDot','E1E7','dot',centered=True)
    add('articStaccatoAbove','E4A2','dot')
    add('articStaccatoBelow','E4A3','dot',below=True)
    for symbol,cp,kind in [('articAccent','E4A0','accent'),('articTenuto','E4A4','tenuto'),
                           ('articMarcato','E4AC','marcato'),('articStaccatissimo','E4A6','staccatissimo'),
                           ('fermata','E4C0','fermata')]:
        add(symbol+'Above',cp,kind)
        add(symbol+'Below',format(int(cp,16)+1,'04X'),kind,below=True)
    return result
