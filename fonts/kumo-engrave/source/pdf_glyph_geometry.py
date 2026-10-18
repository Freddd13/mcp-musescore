"""Read a displayed PDF character's cubic geometry through PDFium.

This does not read/save a FontFile stream or change the document. The API takes
Unicode (not a glyph index). Its coordinates are normalized em outlines;
the text object's font size and matrix supply the displayed transformation.
Always verify against the actual source object, especially subset encodings.
"""
import ctypes
import pypdfium2 as pdf


def glyph_commands(obj, character):
    assert len(character) == 1
    font = pdf.raw.FPDFTextObj_GetFont(obj)
    path = pdf.raw.FPDFFont_GetGlyphPath(font, ord(character), obj.get_font_size())
    assert path, 'No outline for the observed Unicode mapping'
    commands = []; curve = []
    for i in range(pdf.raw.FPDFGlyphPath_CountGlyphSegments(path)):
        segment = pdf.raw.FPDFGlyphPath_GetGlyphPathSegment(path, i)
        kind = pdf.raw.FPDFPathSegment_GetType(segment)
        x, y = ctypes.c_float(), ctypes.c_float()
        assert pdf.raw.FPDFPathSegment_GetPoint(segment, ctypes.byref(x), ctypes.byref(y))
        point = [x.value, y.value]
        if kind == pdf.raw.FPDF_SEGMENT_MOVETO:
            assert not curve
            commands.append(['moveTo', [point]])
        elif kind == pdf.raw.FPDF_SEGMENT_LINETO:
            assert not curve
            commands.append(['lineTo', [point]])
        elif kind == pdf.raw.FPDF_SEGMENT_BEZIERTO:
            curve.append(point)
            if len(curve) == 3:
                commands.append(['curveTo', curve]); curve = []
        else:
            raise ValueError('Unsupported PDF glyph segment')
        if pdf.raw.FPDFPathSegment_GetClose(segment):
            assert not curve
            commands.append(['closePath', []])
    assert not curve and commands
    return commands


def displayed_commands(obj, commands, origin):
    m = obj.get_matrix(); scale = obj.get_font_size()
    return [[op, [[(m.a*x+m.c*y)*scale+origin[0],
                   (m.b*x+m.d*y)*scale+origin[1]] for x, y in points]]
            for op, points in commands]
