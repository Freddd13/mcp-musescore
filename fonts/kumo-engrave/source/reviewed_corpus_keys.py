"""Human roles for all 343 conservative groups of schema-3 candidate keys.

All eight group boards and sixteen page contexts were inspected. A group
certifies the representative's shape role, not every member's musical purpose.
Same-shape dots, bars, rectangles and parentheses retain multiple legal roles.
No decision is a universal PDF encoding table.
"""
CATALOG_SHA = '56d31bbb704726ae721dd3be2f6957fcb6395d4cc70244877f910500ae2a4c1a'


def roles():
    result = {}
    def add(symbols, numbers):
        for n in numbers.split():
            key = 'K%04d'%int(n)
            assert key not in result, key
            result[key] = symbols.split()
    add('accidentalSharp','1 28 201 250 318')
    add('gClef','2 29 116 143 209 229 240 256 287 298 319 341')
    add('fClef','6 34 121 147 210 230 244 260 288 299 326 342')
    add('articTenutoAbove articTenutoBelow','3 320')
    add('timeSig1','97 118 146')
    add('timeSig2','31 71 174')
    add('timeSig3','4 196 321')
    add('timeSig4','5 32 322')
    add('timeSig5','98')
    add('timeSig6','89 242 323')
    add('timeSig8','90 119 279 324')
    add('timeSig9','243 259')
    add('timeSigCommon','44 105 126 149 213 280')
    add('timeSigCutCommon','35 101')
    add('dynamicMF','7 36 73 122 211')
    add('dynamicMP','9 38 123 158 176 212')
    add('dynamicForte','12 45 127 253 312')
    add('dynamicPiano','16 50 215 314')
    add('dynamicPP','25 62 248 296')
    add('dynamicPPP','138 153 249')
    add('dynamicFF','22 60 135 272')
    add('dynamicFFF','53 111 191 278')
    add('dynamicFortePiano','85 133 286 304')
    add('dynamicSforzando1','40 75 124 261')
    add('dynamicSforzato','95 204')
    add('dynamicSforzatoFF','56 192 264')
    add('dynamicMezzo','313')
    add('dynamicSforzando','316')
    add('dynamicZ','317')
    add('fermataAbove','10 41 125')
    add('fermataBelow','18 130')
    add('accidentalFlat','11 43 159')
    add('accidentalNatural','15 49 160 251 329')
    add('accidentalDoubleFlat','27 139 193')
    add('accidentalDoubleSharp','65 113 115 152 334')
    add('accidentalParensLeft noteheadParenthesisLeft','68 86 144 154 173 202 222 236 238 241 306 335')
    add('accidentalParensRight noteheadParenthesisRight','69 87 145 155 156 164 166 194 203 207 223 237 239 281 282 285 307 336 340')
    add('accidentalFlat accidentalParensLeft accidentalParensRight','100 187')
    add('accidentalNatural accidentalParensLeft accidentalParensRight','102 148 270')
    add('accidentalSharp accidentalParensLeft accidentalParensRight','104 245 302')
    add('noteheadBlack','21 58 331')
    add('noteheadHalf','23 61 206 332')
    add('noteheadWhole','51 78')
    add('noteheadXBlack','110 151 171 271')
    add('noteheadCircleX','290')
    add('restWhole restHalf','79')
    add('restWholeLegerLine','66')
    add('restHalfLegerLine','54')
    add('restQuarter','20 57 131 134 218 231 303 330')
    add('rest8th','26 64 84 137 333')
    add('rest16th','67 81 140 208 247 284')
    add('rest32nd','92')
    add('flag8thUp','14 48 128 167 328')
    add('flag8thDown','8 37 268 276 327')
    add('flag16thUp','77 219 234')
    add('flag16thDown','39 74')
    add('flagInternalUp flag32ndUp','200')
    add('flagInternalDown flag32ndDown kumoFlag8thDownShort','165')
    add('metNoteHalfUp','47')
    add('metNoteQuarterUp','17 76 315')
    add('metNote8thUp','91 114 246')
    add('metNote8thUp metAugmentationDot','277')
    add('augmentationDot articStaccatoAbove articStaccatoBelow repeatDot','24 70 96 182')
    add('timeSigEquals','19 82 94 177')
    add('kumoTempoApproxEquals','55')
    add('kumoSwingEighths','199 266 338')
    add('kumoSwingDotted8Sixteenth','181')
    add('kumoSwingTripletQuarterEighth','267')
    add('articAccentAbove articAccentBelow','33 72 120 157 169 175 183 252 275 294 325')
    add('articTenutoStaccatoAbove','109')
    add('articTenutoStaccatoBelow','99 293')
    add('articAccentStaccatoAbove','112 136 178 180 227')
    add('articAccentStaccatoBelow','83 107 129 205 214 269 273 291 343')
    add('articMarcatoAbove','42 103')
    add('articMarcatoBelow','142')
    add('articMarcatoStaccatoAbove','190')
    add('articStaccatissimoAbove','108 216 225 300')
    add('articStaccatissimoBelow','30 221')
    add('segno','163 232')
    add('coda','106 172 233')
    add('keyboardPedalPed','93 132 170 198')
    add('keyboardPedalUp','88 117 168 186 195 224 228 255 289')
    add('ornamentTrill','59 162')
    add('caesura','141 185 254 292')
    add('breathMarkComma','188 257')
    add('tremolo2','295')
    add('tremolo3','297')
    add('ottava','63 309')
    add('ottavaAlta','80 226 310')
    add('wiggleArpeggiatoUp wiggleArpeggiatoDown','13 46 311')
    add('wiggleGlissando','52 150 161 179 184 189 197 217 220 235 258 262 263 265 274 283 301 305 337 339')
    add('brace braceSmall braceLarge braceLarger','308')
    assert set(result) == {'K%04d'%i for i in range(1,344)}, sorted({'K%04d'%i for i in range(1,344)}-set(result))
    return result


CONTEXT_NOTES = {
    'K0013':'Vertical arpeggio at the left of a chord, not a rest.',
    'K0052':'Diagonal repeated wavy glissando, not a flag.',
    'K0055':'Tempo approximate-equals between a half note and 88, not a tenuto-staccato articulation.',
    'K0063':'Bare 8 beginning an octave line below the staff, not a time-signature digit.',
    'K0099':'Dot above tenuto bar below the notes: below variant.',
    'K0109':'Tenuto bar above dot above the notes: above variant.',
    'K0165':'Internal components participating in a down-stem 32nd flag.',
    'K0188':'Breath comma above the staff, separate from the italic expression.',
    'K0200':'Internal component participating in an up-stem 32nd flag.',
    'K0245':'Parenthesized cautionary sharp, not a new composite accidental role.',
    'K0257':'Breath comma before the final figure, not an eighth rest.',
    'K0267':'Triplet quarter/eighth swing equation, not ordinary beamed eighths.',
    'K0293':'Dot above tenuto bar below the notes: below variant.',
    'K0309':'8 component of an 8va line; native ottavaAlta supplies the complete form.',
    'K0310':'va component of the same 8va line; native ottavaAlta supplies the complete form.',
    'K0311':'Repeated vertical arpeggio next to a chord, not a quarter rest.',
}
