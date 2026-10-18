"""Authored integration fixture; never opens or modifies a user's score."""
import xml.etree.ElementTree as ET


def integration_score(data):
    tree=ET.fromstring(data);score=tree.find('Score');staves=score.findall('Staff')
    for staff in staves:
        for child in list(staff):staff.remove(child)
    def measure(staff,label,items):
        m=ET.SubElement(staff,'Measure');voice=ET.SubElement(m,'voice')
        if label:ET.SubElement(ET.SubElement(voice,'StaffText'),'text').text=label
        for item in items:voice.append(ET.fromstring(item))
        return voice
    def chord(pitch=72,tpc=14,stem='up',duration='quarter',head='',parentheses=False,accidental=False,second=False):
        c=ET.Element('Chord');ET.SubElement(c,'durationType').text=duration;ET.SubElement(c,'StemDirection').text=stem
        for p,t in [(pitch,tpc)]+([(pitch+2,16)] if second else []):
            n=ET.SubElement(c,'Note');ET.SubElement(n,'pitch').text=str(p);ET.SubElement(n,'tpc').text=str(t)
            if head:ET.SubElement(n,'head').text=head
            if parentheses:
                for side in ('Left','Right'):ET.SubElement(ET.SubElement(n,'Symbol'),'name').text='noteheadParenthesis'+side
            if accidental:
                a=ET.SubElement(n,'Accidental');ET.SubElement(a,'subtype').text='sharp';ET.SubElement(a,'bracket').text='1'
        return ET.tostring(c,encoding='unicode')
    rest=lambda dur,off:f'<Rest><durationType>{dur}</durationType><offset x="0" y="{off}"/></Rest>'
    rows=[
        ('X heads: both stems and seconds',[chord(head='cross',stem=s,second=i>=2) for i,s in enumerate(('up','down','up','down'))]),
        ('Note parentheses / accidental parentheses',[chord(duration='half',parentheses=True),chord(pitch=73,tpc=21,duration='half',accidental=True)]),
        ('Ledger rests outside staff',[rest('whole',-4)]),
        ('Half rests outside staff',[rest('half',-4),rest('half',4)]),
        ('8va default native line',[chord(duration='whole')]),
        ('8 numbers-only native line',[chord(duration='whole')]),
        ('Native sf dynamics',[chord(duration='whole')]),
        ('Tempo and swing Text extras',[chord(duration='whole')]),
    ]
    for i,(label,items) in enumerate(rows):
        v=measure(staves[0],label,items);measure(staves[1],'',[chord(48,14,duration='whole')])
        if i==0:
            v.insert(0,ET.fromstring('<Clef><concertClefType>G</concertClefType><transposingClefType>G</transposingClefType></Clef>'))
            v.insert(1,ET.fromstring('<TimeSig><sigN>4</sigN><sigD>4</sigD></TimeSig>'))
            staves[1].find('Measure/voice').insert(0,ET.fromstring('<Clef><concertClefType>F</concertClefType><transposingClefType>F</transposingClefType></Clef>'))
        if i in (1,3,5,7):
            b=ET.SubElement(staves[0].findall('Measure')[-1],'LayoutBreak');ET.SubElement(b,'subtype').text='line'
        if i in (4,5):
            # Same-measure spanner ends one whole note later. Native default
            # text resolves the standard ottavaAlta / ottava glyphs.
            sp=ET.fromstring('<Spanner type="Ottava"><Ottava><subtype>8va</subtype><numbersOnly>'+str(i-4)+'</numbersOnly></Ottava><next><location><fractions>1/1</fractions></location></next></Spanner>')
            v.insert(1,sp)
            v.append(ET.fromstring('<Spanner type="Ottava"><prev><location><fractions>-1/1</fractions></location></prev></Spanner>'))
        if i==6:v.insert(1,ET.fromstring('<Dynamic><subtype>sf</subtype></Dynamic>'))
        if i==7:
            bodies=['<sym>metNoteQuarterUp</sym><font face="Kumo Score Study Text"/>\u2252<font face="FreeSerif"/>100',
                    '<font face="Kumo Score Study Text"/>\uF700<sym>timeSigEquals</sym>\uF702',
                    '<font face="Kumo Score Study Text"/>\uF703<sym>timeSigEquals</sym>\uF704']
            for k,body in enumerate(bodies):
                v.insert(k+1,ET.fromstring('<StaffText><offset x="'+str(k*18)+'" y="'+str(-7-k*4)+'"/><text><font size="12"/>'+body+'</text></StaffText>'))
    # The fixture intentionally contains only this authored music. Layout
    # parameters and all font choices remain controlled by the proof harness.
    return ET.tostring(tree)
