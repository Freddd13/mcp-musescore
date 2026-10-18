"""Observed Chaconne encodings, identified from corpus-v2 object rasters.

This is a semantic/coordinate map of selected ATLAS INSTANCES, not font outlines
or a universal encoding table. Even the same family/code can mean a different
glyph in another PDF (e.g. R is sometimes a tempo note). First alias selects
the captured source; all alternatives remain in the local atlas for review.
Only catalogued source objects can be captured by the local study tool.
"""

# (SMuFL name, observed Unicode aliases in hexadecimal, coordinate convention)
GLYPHS = [
 ('noteheadBlack','0153 0091','head'),
 ('noteheadHalf','02D9 00BC','head'),
 ('noteheadWhole','0077 0058','raw'),
 ('noteheadXBlack','00BF 0085','head'),
 ('gClef','0026 0009','raw'),('fClef','003F 0022','raw'),
 ('accidentalSharp','0023 0006','raw'),('accidentalNatural','006E 004F','raw'),
 ('accidentalFlat','0062','raw'),('accidentalDoubleFlat','222B 007F','raw'),
 ('accidentalDoubleSharp','2039 009E','raw'),
 ('accidentalParensLeft','0028','center_y'),('accidentalParensRight','0029 000C','center_y'),
 ('timeSigCommon','0063 0045','center_y'),('timeSigCutCommon','0043 0044','center_y'),
 ('timeSig1','0031','center_y'),('timeSig2','0032 0015','center_y'),
 ('timeSig3','0033 0016','center_y'),('timeSig4','0034 0017','center_y'),
 ('timeSig5','0035','center_y'),('timeSig6','0036 0019','center_y'),
 ('timeSig8','0038 001B 2022','center_y'),('timeSig9','0039','center_y'),
 ('restWhole','2211 007C','top_zero'),('restHalf','00D3','bottom_zero'),
 ('restQuarter','0152 0090','raw'),('rest8th','2030 00A6','raw'),
 ('rest16th','2248 008A','raw'),('rest32nd','00AE 006D','raw'),
 ('flag8thUp','006A 004B','flag_up'),('flag8thDown','004A 002C','flag_down'),
 ('flag16thUp','0072 0053','flag_up'),('flag16thDown','0052','flag_down'),
 ('augmentationDot','02DC 00B9','center_y'),
 ('articStaccatoAbove','002E 0011','bottom_zero'),
 ('articStaccatoBelow','002E 0011','top_zero'),
 ('articTenutoAbove','002D 0002 0010','bottom_zero'),
 ('articTenutoBelow','002D 0002 0010','top_zero'),
 ('articAccentAbove','003E 0021','bottom_zero'),
 ('articAccentBelow','003E 0021','top_zero'),
 ('articMarcatoAbove','005E 0040','bottom_zero'),
 ('articMarcatoBelow','0076','top_zero'),
 ('articStaccatissimoAbove','00C6 0079','bottom_zero'),
 ('articStaccatissimoBelow','0027','top_zero'),
 ('articTenutoStaccatoAbove','00AF 00BA','bottom_zero'),
 ('articTenutoStaccatoBelow','003C 001F','top_zero'),
 ('articAccentStaccatoAbove','02D8','bottom_zero'),
 ('articAccentStaccatoBelow','006C 00A1','top_zero'),
 ('fermataAbove','0055 0037','bottom_zero'),('fermataBelow','0075 0056','top_zero'),
 ('segno','0025 0008','bottom_zero'),('coda','0069 00A0','raw'),
 ('keyboardPedalPed','00B0','raw'),('keyboardPedalUp','002A 000D','raw'),
 ('ornamentTrill','0178 009B','raw'),('caesura','0005','raw'),
 ('tremolo3','0083','center_xy'),
 ('dynamicPiano','0070 0051','raw'),('dynamicForte','0066 0047','raw'),
 ('dynamicPP','03C0 007E','raw'),('dynamicPPP','220F 007D','raw'),
 ('dynamicMP','0050','raw'),('dynamicMF','0046','raw'),
 ('dynamicFF','0192 0089','raw'),('dynamicFFF','00CF','raw'),
 ('dynamicFortePiano','00CD 00AC','raw'),('dynamicSforzato','00DF','raw'),
 ('dynamicSforzatoFF','00E7','raw'),
 ('metNoteHalfUp','0068','met_baseline'),('metNoteQuarterUp','0071','met_baseline'),
 ('metNote8thUp','0065','met_baseline'),('metAugmentationDot','006B 004C','center_y'),
 ('wiggleArpeggiatoUp','0067 0048','arpeggio_rotate'),
 ('wiggleArpeggiatoDown','0067 0048','arpeggio_rotate'),
 ('wiggleTrill','005F','repeat_wave'),
]

# Observed compounds and variants need engine composition/alternate handling.
# They are never silently counted as ordinary glyph replacements.
COMPOUNDS = {
 '0024': ['accidentalFlat','accidentalParensLeft','accidentalParensRight'],
 '0041': ['accidentalFlat','accidentalParensLeft','accidentalParensRight'],
 '004E': ['accidentalNatural','accidentalParensLeft','accidentalParensRight'],
 '0030': ['accidentalNatural','accidentalParensLeft','accidentalParensRight'],
 '0061': ['accidentalSharp','accidentalParensLeft','accidentalParensRight'],
 '00B8': ['metNote8thUp','engine:beamed-pair'],
 '00B7': ['metNote8thUp','engine:dotted8-16-pair'],
 '0131': ['metNote8thUp','engine:dotted8-16-pair'],
 '02DB': ['metNoteQuarterUp','metNote8thUp','engine:triplet-bracket'],
 '00BB': ['text:equals'], '008D': ['text:equals'],
 '00D4': ['variant:short-flag8thDown'],
}

EMPTY = {'0003','0020'}

LIGATURES=[
 ('dynamicSforzatoFF',['dynamicSforzando','dynamicForte','dynamicForte','dynamicZ']),
 ('dynamicSforzato',['dynamicSforzando','dynamicForte','dynamicZ']),
 ('dynamicPPP',['dynamicPiano']*3),('dynamicFFF',['dynamicForte']*3),
 ('dynamicPP',['dynamicPiano']*2),('dynamicFF',['dynamicForte']*2),
 ('dynamicMP',['dynamicMezzo','dynamicPiano']),('dynamicMF',['dynamicMezzo','dynamicForte']),
 ('dynamicFortePiano',['dynamicForte','dynamicPiano']),
]


def observed_codes():
    return set(COMPOUNDS)|EMPTY|{cp for _,aliases,_ in GLYPHS for cp in aliases.split()}
