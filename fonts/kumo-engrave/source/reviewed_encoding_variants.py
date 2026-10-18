"""Reviewed displayed shapes in the eight PDFs with alternate Chaconne codes.

Scope is per-PDF key samples, not a new universal Chaconne encoding table.
All 65 representative groups and 18 selected page contexts were inspected.
"""

VARIANTS_SHA = '4c6d1b4a73f8381fe278c1d2b141e73496aab724e8830493f56f5fb856d8bebe'
CONTEXT_SHA = '0f57ee3a89e2c87ab5a250c549a3842257f1ac249f2ef2d19eef8d2510791189'
SCORES = {'A020', 'A024', 'A036', 'A055', 'A082', 'A087', 'A106', 'A142'}


def selected_encoding_roles():
    result = {}
    for codes, names in [
        ('0005', 'caesura'), ('0006', 'accidentalSharp'), ('0008', 'segno'),
        ('0009', 'gClef'), ('000C', 'accidentalParensRight noteheadParenthesisRight'),
        ('000D', 'keyboardPedalUp'), ('0010', 'articTenutoAbove articTenutoBelow'),
        ('0011', 'articStaccatoAbove articStaccatoBelow'), ('0015', 'timeSig2'),
        ('0016', 'timeSig3'), ('0017', 'timeSig4'), ('0019', 'timeSig6'),
        ('001B', 'timeSig8'), ('001F', 'articTenutoStaccatoBelow'),
        ('0021', 'articAccentAbove articAccentBelow'), ('0022', 'fClef'),
        ('0023', 'tremolo2'), ('0024', 'accidentalParensLeft accidentalFlat accidentalParensRight'),
        ('0028', 'dynamicMF'), ('002C', 'flag8thDown'),
        ('0030', 'accidentalParensLeft accidentalNatural accidentalParensRight'),
        ('0032', 'dynamicMP'), ('0034', 'flag16thDown'), ('0037', 'fermataAbove'),
        ('0040', 'articMarcatoAbove'), ('0044', 'accidentalFlat'), ('0045', 'timeSigCommon'),
        ('0047', 'dynamicForte'), ('0048', 'wiggleArpeggiatoUp wiggleArpeggiatoDown'),
        ('004B', 'flag8thUp'), ('004C', 'metAugmentationDot'), ('004F', 'accidentalNatural'),
        ('0051', 'dynamicPiano'), ('0052', 'metNoteQuarterUp'), ('0053', 'flag16thUp'),
        ('0056', 'fermataBelow'), ('0058', 'noteheadWhole'), ('005F', 'wiggleTrill'),
        ('0066', 'keyboardPedalPed'), ('006C', 'dynamicSforzato'), ('006D', 'rest32nd'),
        ('007C', 'restWhole'), ('007D', 'dynamicPPP'), ('007E', 'dynamicPP'),
        ('007F', 'accidentalDoubleFlat'), ('0083', 'tremolo3'), ('0085', 'noteheadXBlack'),
        ('0089', 'dynamicFF'), ('008A', 'rest16th'), ('008D', 'timeSigEquals'),
        ('0090', 'restQuarter'), ('0091', 'noteheadBlack'), ('009B', 'ornamentTrill'),
        ('009E', 'accidentalDoubleSharp'), ('00A0', 'coda'), ('00A1', 'articAccentStaccatoBelow'),
        ('00A6', 'rest8th'), ('00AC', 'dynamicFortePiano'), ('00B0', 'restHalf'),
        ('00B7', 'kumoSwingDotted8Sixteenth'), ('00B9', 'augmentationDot'),
        ('00BA', 'articTenutoStaccatoAbove'), ('00BB', 'articAccentStaccatoAbove'),
        ('00BC', 'noteheadHalf'),
    ]:
        for cp in codes.split():
            assert cp not in result
            result[cp] = names.split()
    return result
