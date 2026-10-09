"""Author a timing-checked, two-staff fixture; no user score is edited."""
from pathlib import Path
import xml.etree.ElementTree as E

def child(parent,name,text=None,**attrs):
    node=E.SubElement(parent,name,attrs)
    if text is not None:node.text=str(text)
    return node

def note(m,dur,kind,step='C',octave=5,staff=1,rest=False,acc=None,chord=False,arp=None,art=None,fermata=False):
    n=child(m,'note')
    if chord:child(n,'chord')
    if rest:child(n,'rest')
    else:
        p=child(n,'pitch');child(p,'step',step)
        if acc:child(p,'alter',{'sharp':1,'flat':-1,'natural':0,'double-sharp':2,'flat-flat':-2}[acc])
        child(p,'octave',octave)
    child(n,'duration',dur);child(n,'voice',staff);child(n,'type',kind)
    if acc:child(n,'accidental',acc)
    if not rest and kind!='whole':child(n,'stem','up' if staff==1 and octave<6 else 'down')
    child(n,'staff',staff)
    if arp is not None or art or fermata:
        nt=child(n,'notations')
        if arp is not None:child(nt,'arpeggiate',**({'direction':arp} if arp else {}))
        if art:child(child(nt,'articulations'),art)
        if fermata:child(nt,'fermata','normal',type='upright' if staff==1 else 'inverted')
    return dur if not chord else 0

root=E.Element('score-partwise',version='3.1')
child(child(root,'work'),'work-title','Kumo Piano common-symbol proof')
part=child(child(root,'part-list'),'score-part',id='P1');child(part,'part-name','Piano')
part=child(root,'part',id='P1')
labels=['Black heads','Half heads','Whole heads','Quarter rests','Eighth rests','16th rests','32nd rests','64th rests','Arpeggio','Arpeggio up','Arpeggio down','Accidentals','Double accidentals','Up flags','Down flags','Articulations','Fermatas','Pedal and dynamics','Staccatissimo','Dense chord']
for i,label in enumerate(labels):
    m=child(part,'measure',number=str(i+1))
    if i%4==0:child(m,'print',**({'new-system':'yes'} if i else {}))
    if i==0:
        a=child(m,'attributes');child(a,'divisions',480)
        k=child(a,'key');child(k,'fifths',0)
        t=child(a,'time');child(t,'beats',4);child(t,'beat-type',4);child(a,'staves',2)
        for staff,sign,line in [(1,'G',2),(2,'F',4)]:
            c=child(a,'clef',number=str(staff));child(c,'sign',sign);child(c,'line',line)
    direction=child(m,'direction',placement='above');child(child(direction,'direction-type'),'words',label);child(direction,'staff',1)
    total=0
    if i==0:
        for step in 'CDEG':total+=note(m,480,'quarter',step)
    elif i==1:
        for step in 'CE':total+=note(m,960,'half',step)
    elif i==2:total+=note(m,1920,'whole','G')
    elif i==3:
        for _ in range(4):total+=note(m,480,'quarter',rest=True)
    elif 4<=i<=7:
        kind,dur=[('eighth',240),('16th',120),('32nd',60),('64th',30)][i-4]
        for _ in range(4):
            total+=note(m,dur,kind,rest=True);total+=note(m,dur,kind,'D')
        while total<1920:
            size=min(480,1920-total);kind2={480:'quarter',240:'eighth',120:'16th',60:'32nd',30:'64th'}[size]
            total+=note(m,size,kind2,'C')
    elif 8<=i<=10:
        for step in 'CEG':total+=note(m,1920,'whole',step,chord=step!='C',arp=['','up','down'][i-8])
    elif i==11:
        for step,acc in zip('FBCD',['sharp','flat','natural','sharp']):total+=note(m,480,'quarter',step,acc=acc)
    elif i==12:
        for step,acc in zip('FCBD',['double-sharp','flat-flat','double-sharp','natural']):total+=note(m,480,'quarter',step,acc=acc)
    elif i in [13,14]:
        for _ in range(2):
            total+=note(m,240,'eighth','C',octave=4 if i==13 else 6)
            total+=note(m,480,'quarter','D',octave=4 if i==13 else 6)
            total+=note(m,120,'16th','E',octave=4 if i==13 else 6)
            total+=note(m,120,'16th',rest=True)
    elif i==15:
        for step,art in zip('CDEG',['staccato','accent','tenuto','strong-accent']):total+=note(m,480,'quarter',step,art=art)
    elif i==16:
        for step in 'CE':total+=note(m,960,'half',step,fermata=True)
    elif i==17:
        for mode in ['start','stop']:
            dr=child(m,'direction',placement='below');child(child(dr,'direction-type'),'pedal',type=mode,line='no');child(dr,'staff',1)
            child(child(dr,'direction-type'),'dynamics').append(E.Element('mf' if mode=='start' else 'mp'))
            total+=note(m,960,'half','G')
    elif i==18:
        for step in 'CDEG':total+=note(m,480,'quarter',step,art='staccatissimo')
    else:
        for step in 'CDEFG':total+=note(m,1920,'whole',step,chord=step!='C',acc='sharp',arp='up')
    assert total==1920,(i,total)
    child(child(m,'backup'),'duration',1920)
    note(m,1920,'whole','C',octave=3,staff=2,fermata=i==16)
    if i==len(labels)-1:child(child(m,'barline',location='right'),'bar-style','light-heavy')
dest=Path(__file__).with_name('piano-palette.musicxml')
E.ElementTree(root).write(str(dest),encoding='utf-8',xml_declaration=True)
print('Authored %d complete 4/4 measures, two staves.' % len(labels))
