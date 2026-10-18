"""Actual Coda markers and accent-staccato articulations in piano context."""
import xml.etree.ElementTree as E


def refinement_score(data):
    tree=E.fromstring(data);score=tree.find('Score');staves=score.findall('Staff')
    for staff in staves:
        for child in list(staff):staff.remove(child)
    for i in range(3):
        upper=E.SubElement(staves[0],'Measure');v=E.SubElement(upper,'voice')
        lower=E.SubElement(staves[1],'Measure');lv=E.SubElement(lower,'voice')
        E.SubElement(E.SubElement(v,'StaffText'),'text').text=['Coda marker / first system',
            'Accent-staccato / below and above','Coda marker / dense notes'][i]
        if i==0:
            v.append(E.fromstring('<Clef><concertClefType>G</concertClefType><transposingClefType>G</transposingClefType></Clef>'))
            v.append(E.fromstring('<TimeSig><sigN>4</sigN><sigD>4</sigD></TimeSig>'))
            lv.append(E.fromstring('<Clef><concertClefType>F</concertClefType><transposingClefType>F</transposingClefType></Clef>'))
        if i in (0,2):upper.append(E.fromstring('<Marker><label>codab</label><text><sym>coda</sym></text></Marker>'))
        count=16 if i==2 else 4
        for k in range(count):
            c=E.SubElement(v,'Chord');E.SubElement(c,'durationType').text='16th' if i==2 else 'quarter'
            E.SubElement(c,'StemDirection').text='down' if k%2 else 'up'
            n=E.SubElement(c,'Note');E.SubElement(n,'pitch').text=str([72,76,79,77][k%4]);E.SubElement(n,'tpc').text=str([14,18,15,13][k%4])
            if i>0:
                a=E.SubElement(c,'Articulation');E.SubElement(a,'subtype').text='articAccentStaccatoAbove'
                E.SubElement(a,'direction').text='up' if k%2 else 'down';E.SubElement(a,'anchor').text='0' if k%2 else '1'
        lv.append(E.fromstring('<Chord><durationType>whole</durationType><Note><pitch>48</pitch><tpc>14</tpc></Note></Chord>'))
        E.SubElement(E.SubElement(upper,'LayoutBreak'),'subtype').text='line'
    return E.tostring(tree)
