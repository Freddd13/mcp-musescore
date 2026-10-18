"""Roles reviewed on all 21 delta boards plus all 17 visible U+0000 objects.

These decisions apply only to the pinned source instances. A control code or
font name in another PDF does not inherit them. Board fitting is for shape
identification and is never a physical-size measurement.
"""
DELTA_SHA = '97c4d4aa5873e592b208990837b47dfccd8b1678680287d8c5f7c073325aeb0e'
VISIBILITY_SHA = '227d020c72012c575f207554fe7e12d770d1a83b62c47ebb7c2023adad264f9a'
INVENTORY_SHA = '33e0464897191d709b14fa1f7ea556b5dd727b6f07394b15b80e8434e486d85a'

# Full-object representatives: paired parentheses must not be mistaken for one
# glyph. The tempo object contains a quarter plus equals, not two beamed notes.
MUSIC_REPRESENTATIVES = {
    188: ['noteheadParenthesisLeft', 'accidentalParensLeft'],
    **{i:['noteheadParenthesisLeft', 'noteheadParenthesisRight',
          'accidentalParensLeft', 'accidentalParensRight'] for i in range(217,225)},
    259: ['noteheadParenthesisLeft', 'noteheadParenthesisRight',
          'accidentalParensLeft', 'accidentalParensRight'],
    260: ['noteheadParenthesisLeft', 'noteheadParenthesisRight',
          'accidentalParensLeft', 'accidentalParensRight'],
    264: ['metNoteQuarterUp', 'timeSigEquals'],
    374: ['noteheadXBlack'],
}

# Code-level roles were read from actual object bitmaps. A pair above is a
# compound object; these entries distinguish its individual source codes.
MUSIC_KEYS = {
    ('A024','Chaconne',11): ['noteheadParenthesisLeft','accidentalParensLeft'],
    ('A036','Chaconne',11): ['noteheadParenthesisLeft','accidentalParensLeft'],
    ('A036','Chaconne',12): ['noteheadParenthesisRight','accidentalParensRight'],
    ('A055','Chaconne',11): ['noteheadParenthesisLeft','accidentalParensLeft'],
    ('A055','Chaconne',12): ['noteheadParenthesisRight','accidentalParensRight'],
    ('A057','FEF4ADEE9C2',9): ['timeSigEquals'],
    ('A082','Chaconne',133): ['noteheadXBlack'],
}

# Every other representative on these specific boards is ordinary type:
# titles/credits/page numbers, expression words, rotated gliss./black keys.
# U+0020 crop ink often belongs to a neighbouring italic or serif letter.
ORDINARY_REPRESENTATIVES = set(range(1,504))-set(MUSIC_REPRESENTATIVES)
