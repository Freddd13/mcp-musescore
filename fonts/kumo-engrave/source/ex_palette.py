"""0.3: explicit contour studies from direct Chaconne Ex raster observation.

The previous 0.2 family is frozen. This family deliberately changes head
silhouette, counters and stroke hierarchy instead of applying uniform thinning.
Control points are authored here; no reference font program or PDF paths enter
the build. Coordinates use 250 units per staff space.
"""
import math
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from .piano_palette import polygon, disk, ribbon, draw as old_draw, specs as old_specs


def contour(pen, start, segments, reverse=False):
    target = ReverseContourPen(pen) if reverse else pen
    target.moveTo(start)
    for c1, c2, end in segments:
        target.curveTo(c1, c2, end)
    target.closePath()


def oval(pen,cx,cy,rx,ry,shear,reverse=False):
    """Eight round-ended arcs, with the counter direction independent of body."""
    target=ReverseContourPen(pen) if reverse else pen
    def p(t):return (cx+rx*math.cos(t),cy+ry*math.sin(t)+shear*rx*math.cos(t))
    def tangent(t):return (-rx*math.sin(t),ry*math.cos(t)-shear*rx*math.sin(t))
    step=math.pi/4;k=4/3*math.tan(step/4)
    target.moveTo(p(0))
    for i in range(8):
        a=i*step;b=a+step;start=p(a);end=p(b);u=tangent(a);v=tangent(b)
        target.curveTo(tuple(start[j]+k*u[j] for j in (0,1)),
                       tuple(end[j]-k*v[j] for j in (0,1)),end)
    target.closePath()


def draw(spec, advance):
    pen = RecordingPen()
    kind = spec['ex_drawing']
    if kind in ('black', 'half'):
        # Different black/half body proportions and round ends; stem origins stay at
        # (0,-42) / (325,40), with sufficient overlap at both attachments.
        oval(pen,162.5,0,162.5,132 if kind=='black' else 119,.37 if kind=='black' else .4)
        if kind == 'half':
            oval(pen,162.5,0,143,65,.58,reverse=True)
    elif kind == 'whole':
        oval(pen,219,0,219,134,0)
        oval(pen,219,0,96,104,-.62,reverse=True)
    elif kind == 'gClef':
        # Broad diagonal ribbon through the loop; a genuinely fine spine.
        ribbon(pen,(263,-96),[
            ((150,-51),(161,153),(330,158),20,100),
            ((584,191),(663,-188),(416,-272),100,30),
            ((196,-347),(-1,-177),(41,39),30,96),
            ((81,244),(382,410),(421,681),96,28),
            ((450,850),(414,1009),(374,1089),28,20),
            ((258,1026),(234,840),(256,680),20,70)])
        ribbon(pen,(256,680),[
            ((283,420),(350,-98),(391,-493),23,20),
            ((422,-718),(164,-722),(143,-610),20,24)])
        disk(pen,168,-596,77,79)
    elif kind == 'fClef':
        ribbon(pen,(84,146),[
            ((298,361),(517,199),(438,-60),45,136),
            ((372,-299),(144,-503),(0,-584),136,15)])
        disk(pen,91,82,96,95)
        disk(pen,592,125,45);disk(pen,592,-125,45)
    elif kind == 'restQuarter':
        pen.moveTo((70,400))
        pen.curveTo((50,421),(44,407),(61,384));pen.lineTo((139,265))
        pen.curveTo((152,242),(161,216),(149,188));pen.lineTo((76,8))
        pen.curveTo((64,-16),(70,-38),(86,-59));pen.lineTo((144,-139))
        pen.curveTo((111,-110),(42,-101),(10,-143))
        pen.curveTo((-37,-209),(29,-305),(122,-330))
        pen.curveTo((140,-336),(151,-330),(135,-317))
        pen.curveTo((79,-278),(58,-210),(99,-180))
        pen.curveTo((128,-159),(162,-166),(187,-191))
        pen.curveTo((210,-216),(239,-204),(219,-177));pen.lineTo((159,-95))
        pen.curveTo((127,-51),(117,-24),(131,5));pen.lineTo((206,177))
        pen.curveTo((221,210),(214,237),(194,263));pen.lineTo((78,395))
        pen.curveTo((75,400),(73,402),(70,400));pen.closePath()
    elif kind == 'shortRest':
        count=spec['count'];top=200 if count<3 else 450
        end=-255 if count==1 else (-505 if count<4 else -755)
        x=advance-20
        ribbon(pen,(x,top),[((x-40,top-135),(x-109,end+90),(x-139,end),34,29)])
        for i in range(count):
            y=top-79-i*250;left=x-166-i*56
            disk(pen,left,y,59,60)
            ribbon(pen,(left-10,y-24),[
                ((left+54,y-86),(x-37-i*59,y-51),(x-i*60,top-i*250),29,30)])
    elif kind == 'sharp':
        for x in (63,174):
            polygon(pen,[(x-15,-331),(x+15,-315),(x+15,333),(x-15,317)])
        for y in (-140,125):
            polygon(pen,[(0,y-44),(244,y+16),(244,y+102),(0,y+42)])
    elif kind == 'natural':
        polygon(pen,[(0,-130),(30,-118),(30,330),(0,339)])
        polygon(pen,[(140,-337),(170,-346),(170,130),(140,118)])
        for y in (-125,87):
            polygon(pen,[(0,y-9),(170,y+35),(170,y+99),(0,y+55)])
    elif kind in ('flat','doubleFlat'):
        for shift in ([0,223] if kind=='doubleFlat' else [0]):
            polygon(pen,[(shift,-177),(shift,448),(shift+29,454),(shift+29,-140)])
            contour(pen,(shift+24,-160),[
                ((shift+65,-129),(shift+199,-37),(shift+196,72)),
                ((shift+193,184),(shift+73,139),(shift+27,67)),
                ((shift+25,55),(shift+25,-135),(shift+24,-160))])
            contour(pen,(shift+35,-94),[
                ((shift+95,-49),(shift+145,4),(shift+145,69)),
                ((shift+141,125),(shift+70,79),(shift+35,38)),
                ((shift+35,20),(shift+35,-76),(shift+35,-94))],reverse=True)
    elif kind == 'flag':
        # A weight-bearing shoulder, open lower return, and tapered tip.
        contour(pen,(0,12),[
            ((28,-119),(187,-151),(253,-290)),
            ((335,-475),(219,-686),(141,-805)),
            ((126,-826),(118,-817),(130,-789)),
            ((192,-644),(278,-443),(193,-322)),
            ((142,-252),(25,-240),(0,-169)),
            ((0,-121),(0,-33),(0,12))])
        if spec.get('count',1)>1:
            ribbon(pen,(11,-190),[((76,-309),(254,-324),(211,-522),105,19)])
        if spec.get('down'):pen=reflect(pen)
    elif kind == 'arpeggio':
        arrow=spec.get('arrow',False);period=220 if arrow else advance
        length=advance-100 if arrow else advance
        pts=[]
        for i in range(129):
            x=length*i/128;phase=2*math.pi*x/period
            y=82+65*math.sin(phase);slope=65*2*math.pi/period*math.cos(phase)
            norm=math.hypot(1,slope)
            half=18+8*abs(math.sin(phase))
            pts.append(((x-slope*half/norm,y+half/norm),(x+slope*half/norm,y-half/norm)))
        polygon(pen,[p[0] for p in pts]+[p[1] for p in pts[::-1]])
        if arrow:
            polygon(pen,[(advance-130,-62),(advance,82),(advance-130,226),(advance-91,82)])
            polygon(pen,[(length-3,64),(advance-40,64),(advance-40,100),(length-3,100)])
    elif kind == 'tenuto':
        polygon(pen,[(0,0),(advance,0),(advance,40),(0,40)])
    elif kind == 'fermata':
        ribbon(pen,(15,20),[
            ((30,220),((advance+65)/4,319),(advance/2,319),28,82),
            (((3*advance-65)/4,319),(advance-30,220),(advance-15,20),82,28)])
        disk(pen,advance/2,49,49)
    else:
        previous=dict(spec);previous.pop('ex_drawing')
        previous.pop('below',None)
        pen=old_draw(previous,advance)
    if spec.get('below'):pen=reflect(pen)
    return pen


def reflect(recording):
    result=RecordingPen()
    for op,args in recording.value:
        getattr(result,op)(*(tuple((x,-y) for x,y in args)))
    return result


def specs():
    result=old_specs()
    for spec in result.values():spec['ex_drawing']=spec['drawing']
    for name,code,kind in [('noteheadBlack','E0A4','black'),
                           ('noteheadHalf','E0A3','half'),('noteheadWhole','E0A2','whole')]:
        result[name]=dict(codepoint=code,ex_drawing=kind,head=True)
    # Only whole-note advance changes. Ordinary stemmed heads keep Leland's
    # 325-unit advance and both stem attachment coordinates.
    result['noteheadWhole']['advance']=438
    return result
