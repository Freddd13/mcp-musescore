"""Authored piano glissandi: directions, cross-staff, line break and trill control."""
import xml.etree.ElementTree as ET


def gliss_musicxml():
    tree=ET.Element('score-partwise',version='3.1')
    parts=ET.SubElement(tree,'part-list');part=ET.SubElement(parts,'score-part',id='P1')
    ET.SubElement(part,'part-name').text='Piano'
    music=ET.SubElement(tree,'part',id='P1')
    def value(parent,tag,text,**attributes):
        item=ET.SubElement(parent,tag,**attributes);item.text=str(text);return item
    for index in range(8):
        measure=ET.SubElement(music,'measure',number=str(index+1))
        if index==0:
            a=ET.SubElement(measure,'attributes');value(a,'divisions',8)
            key=ET.SubElement(a,'key');value(key,'fifths',0)
            time=ET.SubElement(a,'time');value(time,'beats',4);value(time,'beat-type',4)
            value(a,'staves',2)
            for number,sign,line in [(1,'G',2),(2,'F',4)]:
                clef=ET.SubElement(a,'clef',number=str(number));value(clef,'sign',sign);value(clef,'line',line)
        if index in (3,6):ET.SubElement(measure,'print',{'new-system':'yes'})
        direction=ET.SubElement(measure,'direction',placement='above')
        value(ET.SubElement(direction,'direction-type'),'words',[
            'Wavy rising','Wavy falling','Straight control','Dense notes',
            'Cross staff','Across system: start','Across system: end','Trill control'][index])
        pitches=[('C',5),('G',6),('G',5),('C',5)]
        if index==1:pitches=[('G',6),('C',5),('G',5),('C',5)]
        if index==4:pitches=[('G',5),('C',3),('E',5),('C',5)]
        count=32 if index==3 else 4
        for i in range(count):
            note=ET.SubElement(measure,'note');pitch=ET.SubElement(note,'pitch')
            step,octave=pitches[i%4];value(pitch,'step',step);value(pitch,'octave',octave)
            value(note,'duration',1 if index==3 else 8);value(note,'voice',1)
            value(note,'type','32nd' if index==3 else 'quarter')
            value(note,'staff',2 if index==4 and i==1 else 1)
            spans=[]
            if index<5 and i in (0,1):spans.append(('slide' if index==2 else 'glissando','start' if i==0 else 'stop'))
            if (index,i) in ((5,3),(6,0)):spans.append(('glissando','start' if index==5 else 'stop'))
            if spans:
                notation=ET.SubElement(note,'notations')
                for tag,kind in spans:ET.SubElement(notation,tag,type=kind,number='1')
            if index==7 and i in (0,3):
                ornaments=ET.SubElement(ET.SubElement(note,'notations'),'ornaments')
                if i==0:ET.SubElement(ornaments,'trill-mark')
                ET.SubElement(ornaments,'wavy-line',type='start' if i==0 else 'stop',number='1')
        value(ET.SubElement(measure,'backup'),'duration',32)
        note=ET.SubElement(measure,'note');ET.SubElement(note,'rest',measure='yes')
        value(note,'duration',32);value(note,'voice',2);value(note,'staff',2)
    # ElementTree.tostring gained xml_declaration in Python 3.8. Keep the
    # native proof usable with the same Python 3.7 runtime as the font tools.
    return b"<?xml version='1.0' encoding='utf-8'?>\n"+ET.tostring(tree,encoding='utf-8')
