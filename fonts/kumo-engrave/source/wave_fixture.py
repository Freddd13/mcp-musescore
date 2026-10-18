"""Real arpeggio/trill elements at several lengths, not repeated Text symbols."""
import xml.etree.ElementTree as ET


def wave_score(data):
    tree=ET.fromstring(data);score=tree.find('Score');staves=score.findall('Staff');staff=staves[0]
    for extra in staves[1:]:score.remove(extra)
    part=score.find('Part')
    for extra in part.findall('Staff')[1:]:part.remove(extra)
    for b in part.findall('Staff/bracket'):part.find('Staff').remove(b)
    for child in list(staff):staff.remove(child)
    style=score.find('Style')
    for key,value in [('pageHeight','16.5354'),('pageWidth','11.6929'),('lastSystemFillLimit','0')]:
        item=style.find(key)
        if item is None:item=ET.SubElement(style,key)
        item.text=value
    for i in range(12):
        m=ET.SubElement(staff,'Measure');v=ET.SubElement(m,'voice')
        if i==0:
            v.append(ET.fromstring('<Clef><concertClefType>G</concertClefType><transposingClefType>G</transposingClefType></Clef>'))
            v.append(ET.fromstring('<TimeSig><sigN>4</sigN><sigD>4</sigD></TimeSig>'))
        label=('normal','up arrow','down arrow')[i//3]+' / '+('short','medium','long')[i%3] if i<9 else ['trill long','line-only trill','cross-system continuation'][i-9]
        ET.SubElement(ET.SubElement(v,'StaffText'),'text').text=label
        if i>=9:
            kind='prallprall' if i==10 else 'trill'
            next_location='<fractions>1/1</fractions>' if i<11 else '<measures>1</measures><fractions>1/1</fractions>'
            v.append(ET.fromstring('<Spanner type="Trill"><Trill><subtype>'+kind+'</subtype></Trill><next><location>'+next_location+'</location></next></Spanner>'))
        chord=ET.SubElement(v,'Chord');ET.SubElement(chord,'durationType').text='whole'
        for pitch,tpc in [(72,14),(76,18),(79,15)]:
            note=ET.SubElement(chord,'Note');ET.SubElement(note,'pitch').text=str(pitch);ET.SubElement(note,'tpc').text=str(tpc)
        if i<9:
            arp=ET.SubElement(chord,'Arpeggio');ET.SubElement(arp,'subtype').text=str(i//3)
            ET.SubElement(arp,'userLen2').text=str([0,4,10][i%3])
        if 9<=i<11:v.append(ET.fromstring('<Spanner type="Trill"><prev><location><fractions>-1/1</fractions></location></prev></Spanner>'))
        if i in (2,5,8,10,11):ET.SubElement(ET.SubElement(m,'LayoutBreak'),'subtype').text='line'
    m=ET.SubElement(staff,'Measure');v=ET.SubElement(m,'voice')
    v.append(ET.fromstring('<Chord><durationType>whole</durationType><Note><pitch>72</pitch><tpc>14</tpc></Note></Chord>'))
    v.append(ET.fromstring('<Spanner type="Trill"><prev><location><measures>-1</measures><fractions>-1/1</fractions></location></prev></Spanner>'))
    return ET.tostring(tree)
