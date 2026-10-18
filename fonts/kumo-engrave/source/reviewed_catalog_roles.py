"""Human-reviewed roles of the selected catalogue instances, not global encodings.

All 21 music atlas boards and 12 hidden-font contact sheets were inspected.
Hashes pin these decisions to those samples. Reusing the same PDF font name or
Unicode in another score does not inherit this certification.
"""
from .pdf_symbol_map import GLYPHS, COMPOUNDS, EMPTY


CATALOG_HASHES = {
 'chaconne-catalog-v2':'2bc694239ca8b72c814195c9d0ed75d8036d06d9516eed6b0e9d955f2c78f82c',
 'cid1-catalog-v2':'6989579e2d6f32bc7b1c093d9495f244f740f92ff0c244a03ad06fc6d2de9acb',
 'hidden-control-catalog-v2':'5eb3f27a3c222b6021a25b1d68fe1d932839b4aa2c8bf7e0dd377f59aea960f6',
 'pavane-catalog-v2':'f0182b38547e3cef32bb2fbb6e9497866c9d6045c5c20e83b8e6c0544338c1b6',
 'OpusStd-catalog-v2':'6d5fb1babe48d744131cee20dc131d5a1a1c6d3f2997918c879ba1846f501af0',
 'OpusTextStd-catalog-v2':'e18df5960c0b9fda97cd340b4b4329e2777b2dcffc11a4287bff8bdd23bf20fd',
 'OpusSpecialStd-catalog-v2':'5d09cd18529a04ca4189630ccd3b5e8930412b4daf7a3935223f9deb34b4d0c1',
}
PENDING_HASH='5c830c3968099822dff2c1cb3edbdfd54c37ce4a608c0ac71f64e38463b64846'
EMPTY_AUDIT_HASH='a872515b956c7c6cd34c07d289a31ed39c506f4e1a687541901945f25724f8bb'


def add(mapping, symbols, codes):
    for code in codes.split():mapping[code]=symbols.split()


def selected_roles(directory):
    base={}
    for name,aliases,mode in GLYPHS:
        for code in aliases.split():base.setdefault(code,[]).append(name)
    for code,names in COMPOUNDS.items():base[code]=[n for n in names if not n.startswith(('engine:','text:'))]
    for code in EMPTY:base[code]=[]
    add(base,'kumoSwingEighths','00B8')
    add(base,'kumoSwingDotted8Sixteenth','00B7 0131')
    add(base,'kumoSwingTripletQuarterEighth','02DB')
    add(base,'timeSigEquals','00BB 008D')
    add(base,'flagInternalUp flag32ndUp','004B')
    add(base,'flagInternalDown flag32ndDown kumoFlag8thDownShort','00D4')
    add(base,'accidentalParensLeft noteheadParenthesisLeft','0028')
    add(base,'accidentalParensRight noteheadParenthesisRight','0029 000C')
    if directory in ('chaconne-catalog-v2','OpusStd-catalog-v2'):return base
    if directory=='cid1-catalog-v2':
        add(base,'caesura','0022')
        add(base,'dynamicSforzando1','0053')
        add(base,'wiggleGlissando','007E F07E')
        add(base,'restHalfLegerLine','00D3')
        add(base,'kumoTempoApproxEquals','00DA')
        # Explicitly reviewed PUA layout: F0xx is not a universal low-byte alias.
        for names,codes in [
            ('','F020'),('accidentalSharp','F023'),('segno','F025'),('gClef','F026'),
            ('accidentalParensLeft noteheadParenthesisLeft','F028'),
            ('accidentalParensRight noteheadParenthesisRight','F029'),
            ('articTenutoAbove articTenutoBelow','F02D'),
            ('articStaccatoAbove articStaccatoBelow','F02E'),
            ('timeSig2','F032'),('timeSig3','F033'),('timeSig4','F034'),('timeSig6','F036'),('timeSig8','F038'),
            ('articAccentAbove articAccentBelow','F03E'),('fClef','F03F'),('dynamicMF','F046'),
            ('flag8thDown','F04A'),('flagInternalUp flag32ndUp','F04B'),('dynamicMP','F050'),
            ('flag16thDown','F052'),('dynamicSforzando1','F053'),('fermataAbove','F055'),
            ('articMarcatoAbove','F05E'),('accidentalFlat','F062'),('metNote8thUp','F065'),
            ('dynamicForte','F066'),('wiggleArpeggiatoUp wiggleArpeggiatoDown','F067'),
            ('flag8thUp','F06A'),('accidentalNatural','F06E'),('dynamicPiano','F070'),
            ('metNoteQuarterUp','F071'),('flag16thUp','F072'),('fermataBelow','F075'),
            ('articMarcatoBelow','F076'),('noteheadWhole','F077'),('dynamicSforzatoFF','F08D'),
            ('keyboardPedalPed','F0A1'),('dynamicSforzato','F0A7'),('rest32nd','F0A8'),
            ('restWhole','F0B7'),('dynamicPPP','F0B8'),('dynamicPP','F0B9'),('accidentalDoubleFlat','F0BA'),
            ('ottavaAlta','F0C3'),('dynamicFF','F0C4'),('rest16th','F0C5'),('timeSigEquals','F0C8'),
            ('restQuarter','F0CE'),('noteheadBlack','F0CF'),('ornamentTrill','F0D9'),
            ('accidentalDoubleSharp','F0DC'),('coda','F0DE'),('articAccentStaccatoBelow','F0DF'),
            ('rest8th','F0E4'),('dynamicFortePiano','F0EA'),('dynamicFFF','F0EC'),('restHalf','F0EE'),
            ('augmentationDot','F0F7'),('articAccentStaccatoAbove','F0F9'),('noteheadHalf','F0FA'),
            ('kumoSwingEighths','F0FC'),('kumoSwingTripletQuarterEighth','F0FE')]:add(base,names,codes)
        return base
    if directory=='pavane-catalog-v2':
        for names,codes in [('restWholeLegerLine','0001'),('articTenutoAbove articTenutoBelow','0002'),
            ('rest16th','0003'),('noteheadHalf','0016 0017 0019 001A 001B 001D'),
            ('caesura','0022'),('dynamicSforzando1','0053'),('wiggleGlissando','007E'),
            ('restHalfLegerLine','00D3'),('kumoTempoApproxEquals','00DA')]:add(base,names,codes)
        return base
    if directory=='OpusTextStd-catalog-v2':
        return {code:[name] for code,name in [('0066','dynamicForte'),('006D','dynamicMezzo'),
            ('0070','dynamicPiano'),('0071','metNoteQuarterUp'),('0073','dynamicSforzando'),('007A','dynamicZ')]}
    if directory=='OpusSpecialStd-catalog-v2':
        return {'003C':['accidentalParensLeft','noteheadParenthesisLeft'],
            '003E':['accidentalParensRight','noteheadParenthesisRight'],'007B':['brace'],
            '201C':['ottava'],'201D':['ottavaAlta'],'2122':['augmentationDot','repeatDot'],
            '220F':['wiggleArpeggiatoUp','wiggleArpeggiatoDown']}
    if directory=='hidden-control-catalog-v2':
        result={}
        for names,codes in [
            ('gClef','0001'),('accidentalSharp','0002'),('timeSigCommon','0003'),('noteheadBlack','0004'),
            ('augmentationDot articStaccatoAbove articStaccatoBelow repeatDot','0005 001F'),
            ('noteheadHalf','0006'),('noteheadWhole','0007'),('metNoteQuarterUp timeSigEquals','0008'),
            ('restQuarter','000A'),('fermataAbove','000B'),('fermataBelow','000C'),('accidentalNatural','000D'),
            ('fClef','000E'),('dynamicPiano','000F'),('articTenutoAbove articTenutoBelow','0010'),
            ('rest8th','0011'),('flag8thUp','0012'),('timeSig8','0013'),('flag16thUp','0014'),
            ('dynamicMP','0015'),('flag8thDown','0016'),('dynamicMF','0017'),
            ('articAccentAbove articAccentBelow','0018'),('dynamicFF','0019'),('dynamicForte','001A'),
            ('timeSig4','001B'),('timeSig2','001C'),('flag16thDown','001D'),('restHalfLegerLine','001E'),
            ('articTenutoStaccatoBelow','0020'),('caesura','0021'),
            ('wiggleArpeggiatoUp wiggleArpeggiatoDown','0022'),('keyboardPedalPed','0023'),('keyboardPedalUp','0024')]:add(result,names,codes)
        return result
    raise KeyError(directory)


# Full-object samples distinguish hidden music from ordinary type. The remaining
# groups were viewed as title/credit, rehearsal/tempo, tuplet/fingering or prose;
# that review does not certify every unshown character of their font subsets.
HIDDEN_MUSIC={
 'H005':{'kumoSwingSixteenths','kumoSwingTripletEighthSixteenth','timeSigEquals'},
 'H008':{'fermataAbove','fermataBelow'},'H027':{'fermataAbove'},
 'H050':{'fermataAbove','fermataBelow'},'H068':{'fermataAbove'},'H089':{'fermataAbove'},
 'H111':{'rest16th','dynamicPP','restWhole','restWholeLegerLine'},
 'H157':{'ottava'},'H193':{'noteheadHalf','articAccentStaccatoBelow'},
 'H196':{'noteheadHalf','articAccentStaccatoBelow'},'H236':{'fermataAbove'},
 'H242':{'fermataAbove'},'H269':{'noteheadParenthesisLeft','noteheadParenthesisRight'},
}
HIDDEN_NONMUSIC_EXCEPTIONS={
 'H010':'Japanese title quotation marks U+300C/U+300D around lit, not hand brackets',
 'H053':'U+2606 star in the Madoka Magica subtitle, not a piano articulation',
 'H251':'U+266A note in the Tokimeki poporon title, not a tempo/score note',
 'H112':'Control-encoded ordinary cresc./l.h./rit. letters, not SMuFL symbols',
}
