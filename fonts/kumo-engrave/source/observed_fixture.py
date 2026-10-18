"""Real note, articulation, breath, repeat and flag paths for reviewed additions."""
import xml.etree.ElementTree as E


def observed_score(data):
    tree=E.fromstring(data);score=tree.find('Score');staves=score.findall('Staff')
    for staff in staves:
        for child in list(staff):staff.remove(child)
    def chord(duration='quarter',stem='up',head='',articulation='',tenuto=False):
        c=E.Element('Chord');E.SubElement(c,'durationType').text=duration;E.SubElement(c,'StemDirection').text=stem
        E.SubElement(c,'BeamMode').text='no'
        note=E.SubElement(c,'Note');E.SubElement(note,'pitch').text='72';E.SubElement(note,'tpc').text='14'
        if head:E.SubElement(note,'head').text=head
        if articulation:
            a=E.SubElement(c,'Articulation');E.SubElement(a,'subtype').text='articMarcatoTenutoAbove' if tenuto else 'articMarcatoStaccatoAbove'
            E.SubElement(a,'direction').text='up' if articulation=='above' else 'down'
            E.SubElement(a,'anchor').text='0' if articulation=='above' else '1'
        return c
    labels=['Circle-X / both stems','Marcato-staccato / both placements','Native breath comma',
            'Native 32nd flags / source assembled 16th + internal','Native repeat dots / start and end',
            'Native single-letter dynamics / m, s, z','Marcato-tenuto / both placements']
    for i,label in enumerate(labels):
        measure=E.SubElement(staves[0],'Measure');v=E.SubElement(measure,'voice')
        E.SubElement(E.SubElement(v,'StaffText'),'text').text=label
        lower=E.SubElement(staves[1],'Measure');lv=E.SubElement(lower,'voice')
        if i==0:
            v.append(E.fromstring('<Clef><concertClefType>G</concertClefType><transposingClefType>G</transposingClefType></Clef>'))
            v.append(E.fromstring('<TimeSig><sigN>4</sigN><sigD>4</sigD></TimeSig>'))
            lv.append(E.fromstring('<Clef><concertClefType>F</concertClefType><transposingClefType>F</transposingClefType></Clef>'))
        for k in range(4 if i!=3 else 8):
            if i==5 and k<3:
                d=E.SubElement(v,'Dynamic');E.SubElement(d,'subtype').text='other-dynamics'
                d.append(E.fromstring('<text><sym>'+['dynamicMezzo','dynamicSforzando','dynamicZ'][k]+'</sym></text>'))
            v.append(chord('32nd' if i==3 else 'quarter','down' if k%2 else 'up','xcircle' if i==0 else '',
                           ('below' if k%2 else 'above') if i in (1,6) else '',i==6))
            if i==2 and k in (0,2):v.append(E.fromstring('<Breath><symbol>breathMarkComma</symbol></Breath>'))
        if i==3:v.append(E.fromstring('<Rest><durationType>half</durationType><dots>1</dots></Rest>'))
        lv.append(E.fromstring('<Rest><durationType>whole</durationType></Rest>'))
        if i==4:E.SubElement(measure,'startRepeat');E.SubElement(measure,'endRepeat').text='2'
        E.SubElement(E.SubElement(measure,'LayoutBreak'),'subtype').text='line'
    return E.tostring(tree)


def brace_score(data,count):
    tree=E.fromstring(data);score=tree.find('Score');part=score.find('Part')
    for staff in list(part.findall('Staff')):part.remove(staff)
    for staff in list(score.findall('Staff')):score.remove(staff)
    for i in range(1,count+1):
        staff=E.SubElement(part,'Staff',id=str(i));kind=E.SubElement(staff,'StaffType',group='pitched');E.SubElement(kind,'name').text='stdNormal'
        if i==1:E.SubElement(staff,'bracket',type='1',span=str(count),col='0')
        music=E.SubElement(score,'Staff',id=str(i));v=E.SubElement(E.SubElement(music,'Measure'),'voice')
        v.append(E.fromstring('<TimeSig><sigN>4</sigN><sigD>4</sigD></TimeSig>'))
        v.append(E.fromstring('<Chord><durationType>whole</durationType><Note><pitch>60</pitch><tpc>14</tpc></Note></Chord>'))
    return E.tostring(tree)
