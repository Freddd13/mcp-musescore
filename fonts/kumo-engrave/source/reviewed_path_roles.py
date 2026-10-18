"""Human review of all 864 A064 path-group representatives.

These are shape/use decisions for the displayed representatives, not a claim
that all members of a geometric group have one musical meaning. The 24 boards
were inspected; selected ambiguous instances were also checked on their pages.
Matcher proposals are deliberately not read here.
"""

PATHS_SHA = 'ac4be06dcb041ae648e6709d23babb07e941d6fb46963004f4fe0f58740c52f3'
GROUPS_SHA = 'c7ea3e7b2424bce1b9ca36fcb1dfc7ab48bb7d981ffbd9809fbd92d30d29ee87'
CONTEXT_HASHES = {
    'path-context-152/contexts.json': 'afe5b7909f1a47d07f90d1d4ab7b66fe1b74a4daac51df6285f753173a507fb7',
    'path-context-154/contexts.json': 'e55200cc28b9daf745638f600f066b9cbb464263cd6be4526cbe34e610ca7e6e',
}
CANCELLATION_HASH = '2f148be14d7a49de2fea74fd3c0cf22a839206b8437902705456d70b8a29d69a'


def reviewed_roles():
    # The remaining representatives are page geometry: lines/line groups,
    # sloped beams, open arcs, wedges, dashed spans, frames and their fragments.
    # This explicit reviewed negative category is not a best-match threshold.
    result = {n: dict(category='non-font-page-geometry', targets=[],
                     note='Reviewed representative only; exact function of each grouped member is not certified.')
              for n in range(1, 865)}
    assigned = set()

    def put(ids, category, targets='', note=''):
        for n in map(int, ids.split()):
            assert n not in assigned, n
            assigned.add(n)
            result[n] = dict(category=category, targets=targets.split(), note=note)

    for ids, targets in [
        ('4', 'noteheadBlack'), ('8 33 141', 'accidentalSharp'),
        ('17 139', 'fClef'), ('19', 'accidentalNatural'),
        ('20 56', 'flag8thDown'), ('21 140 146', 'articAccentAbove articAccentBelow'),
        ('25', 'wiggleTrill'), ('26 57', 'flag8thUp'), ('27', 'noteheadWhole'),
        ('30', 'wiggleArpeggiatoUp wiggleArpeggiatoDown'),
        ('31 36 58', 'noteheadHalf'), ('32 59 149 150', 'gClef'),
        ('34', 'rest8th'), ('35 134', 'accidentalFlat'), ('54', 'timeSig4'),
        ('55', 'dynamicMP'), ('118', 'timeSig1'), ('119', 'dynamicForte'),
        ('120', 'timeSig8'), ('121', 'timeSig2'), ('122', 'restQuarter'),
        ('123', 'metNoteQuarterUp'), ('124 144', 'dynamicSforzato'),
        ('125', 'dynamicPiano'), ('126', 'fermataAbove'), ('127', 'timeSig3'),
        ('128', 'dynamicPPP'), ('129', 'rest16th'), ('130', 'dynamicMF'),
        ('131 142', 'accidentalDoubleSharp'), ('132', 'dynamicPP'),
        ('133', 'dynamicFF'), ('135', 'ottava'),
        ('136 151', 'accidentalParensLeft accidentalSharp accidentalParensRight'),
        ('137 145', 'keyboardPedalPed'), ('138 143', 'keyboardPedalUp'),
        ('147', 'accidentalParensRight noteheadParenthesisRight'),
        ('148', 'accidentalParensLeft noteheadParenthesisLeft'), ('213', 'ornamentTrill'),
    ]:
        put(ids, 'music-shape-existing-target', targets,
            'Existing default target; the group may include size/direction variants, not identical native placement.')
    put('9', 'shared-dot-primitive',
        'augmentationDot articStaccatoAbove articStaccatoBelow repeatDot',
        'A round dot alone does not identify augmentation, staccato or repeat function for every member.')
    put('13', 'shared-rest-body-primitive', 'restWhole restHalf',
        'Page context of the representative is a half rest. Rectangular shape alone does not distinguish all uses.')
    put('40 43 79 83', 'brace-half-existing-construction',
        'braceSmall brace braceLarge braceLarger',
        'Halves of system braces, not quarter rests or arpeggio segments; existing paired construction retained.')

    put('''37 41 63 65 66 69 74 76 77 155 158 159 160 161 163 165 166 167
        171 173 174 176 177 184 186 190 192 193 194 195 196 197 198 199 200
        202 203 204 207 208 209 212 214 215 216 218 220 221 222 223 224 225
        226 227 228 229 231 232 233 234 235 236 238 239 240 241 242 244 246
        249 250 253 254 255 256 257 258 260 262 263 264 267 268 269 270 272
        273 275 276 277 278 279 280 281 283 284 285 286 287 288 289 290 291
        293 294 295 296 298 299 300 301 303 304 305 306 307 309 310 312 313
        314 316 317 318 320 321 322 325 326 327 329 330 331 334 337 341 342
        344 346 351 355 360 379''', 'ordinary-type', '',
        'Outlined letters, numerals or punctuation; preserve the native text style rather than assign a music codepoint.')
    put('67 68 71 180 185 187 189 217 237', 'tuplet-text', '',
        'Page contexts include 3, 5, 6, 10 and 11 groups. Tuplet text is separate from meter numerals.')
    put('152 162 245', 'tempo-number-text', '',
        'Representative contexts show tempo 66 or 74, not time-signature digits.')
    put('183 188', 'ordinary-expression-letter', '',
        'Letter o in sotto voce, not a half-note head.')
    put('252', 'mixed-expression-text', '',
        'Italic p in p espress.; musical piano meaning in a text run does not establish a standalone dynamics-font route.')
    put('261 271', 'ordinary-expression-letter', '',
        'Letter p in a tempo / a piacere, not a piano dynamic.')
    # Page geometry whose context is especially easy to misread in isolation.
    result[24]['note'] = 'Square rehearsal-B frame, not beamed tempo notes.'
    result[251]['note'] = 'Corner at the end of a dashed octave span, not a double sharp.'
    result[265]['note'] = 'Corner at the end of an 8-below octave span, not a double sharp.'
    result[315]['note'] = 'Tie beside a dotted half note; no fermata dot.'
    result[324]['note'] = 'Short tie above a note beside a longer slur; no fermata dot.'
    result[350]['note'] = 'Repeat barline pair in context, not an accidental natural.'
    return result
