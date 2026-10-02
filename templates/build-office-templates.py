"""Builds the Chimalaya Word and PowerPoint templates.

The .docx and .pptx are committed, but they are generated rather than
hand-made, so the brand values live in one place and the files can be rebuilt:

    python3 templates/build-office-templates.py

Needs: pip install python-docx python-pptx
"""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Emu

from pptx import Presentation
from pptx.dml.color import RGBColor as PRGB
from pptx.util import Inches as PInches, Pt as PPt

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, 'assets', 'chimalaya-logo.png')
MARK = os.path.join(HERE, 'assets', 'chimalaya-mark.png')
LOGO_REV = os.path.join(HERE, 'assets', 'chimalaya-logo-reverse.png')

NAVY    = RGBColor(0x12, 0x3F, 0x6B)
CRIMSON = RGBColor(0xE5, 0x00, 0x46)
INK     = RGBColor(0x16, 0x23, 0x3A)
MUTED   = RGBColor(0x5B, 0x6B, 0x80)
FONT    = 'Inter'          # falls back to the Office default if not installed

P_NAVY    = PRGB(0x12, 0x3F, 0x6B)
P_CRIMSON = PRGB(0xE5, 0x00, 0x46)
P_INK     = PRGB(0x16, 0x23, 0x3A)
P_MUTED   = PRGB(0x5B, 0x6B, 0x80)
P_WHITE   = PRGB(0xFF, 0xFF, 0xFF)


# --------------------------------------------------------------------- Word

def style_font(style, size, color, bold=False, name=FONT):
    style.font.name = name
    style.font.size = Pt(size)
    style.font.color.rgb = color
    style.font.bold = bold
    # python-docx only sets the Latin font; set the others so Word does not
    # silently substitute for non-Latin runs
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:asciiTheme', 'w:hAnsiTheme', 'w:cstheme', 'w:eastAsiaTheme'):
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rfonts.set(qn(attr), name)


def strip_borders(style):
    """Word's Title style ships with a bottom rule; the template draws its own."""
    ppr = style.element.find(qn('w:pPr'))
    if ppr is None:
        return
    for bdr in ppr.findall(qn('w:pBdr')):
        ppr.remove(bdr)


def shade(cell, hexcolor):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), hexcolor)
    tc_pr.append(shd)


def bottom_border(paragraph, color='E50046', size=18):
    """A coloured rule under a paragraph, used for the heading accent."""
    ppr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), color)
    borders.append(bottom)
    ppr.append(borders)


def build_docx(path):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(0.95)
    section.right_margin = Inches(0.95)

    style_font(doc.styles['Normal'], 10.5, INK)
    doc.styles['Normal'].paragraph_format.space_after = Pt(8)
    doc.styles['Normal'].paragraph_format.line_spacing = 1.15

    style_font(doc.styles['Title'], 30, NAVY, bold=True)
    strip_borders(doc.styles['Title'])
    doc.styles['Subtitle'].font.italic = False
    style_font(doc.styles['Heading 1'], 16, NAVY, bold=True)
    style_font(doc.styles['Heading 2'], 12.5, NAVY, bold=True)
    style_font(doc.styles['Heading 3'], 11, NAVY, bold=True)
    style_font(doc.styles['Subtitle'], 14, MUTED)
    for name in ('Heading 1', 'Heading 2', 'Heading 3'):
        doc.styles[name].paragraph_format.space_before = Pt(16)
        doc.styles[name].paragraph_format.space_after = Pt(4)

    # running footer: organisation on the left, page number on the right
    footer = section.footer.paragraphs[0]
    footer.text = 'Chimalaya Charity'
    footer.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in footer.runs:
        run.font.size = Pt(8.5)
        run.font.color.rgb = MUTED
        run.font.name = FONT

    # masthead
    doc.add_picture(LOGO, width=Inches(2.3))
    doc.add_paragraph()

    title = doc.add_paragraph('Document title', style='Title')
    sub = doc.add_paragraph('Subtitle or project name', style='Subtitle')
    rule = doc.add_paragraph()
    bottom_border(rule)

    meta = doc.add_paragraph('Author  ·  Date')
    meta.runs[0].font.color.rgb = MUTED
    meta.runs[0].font.size = Pt(10)

    doc.add_page_break()

    doc.add_paragraph('Heading 1', style='Heading 1')
    doc.add_paragraph(
        'Body text. Replace this with your own. The Normal style is Inter at '
        '10.5 pt in the brand ink colour; headings are navy. Styles are set up '
        'so the document stays consistent as it grows.')
    doc.add_paragraph('Heading 2', style='Heading 2')
    doc.add_paragraph('First bullet point', style='List Bullet')
    doc.add_paragraph('Second bullet point', style='List Bullet')
    doc.add_paragraph('First numbered item', style='List Number')
    doc.add_paragraph('Second numbered item', style='List Number')

    doc.add_paragraph('Table', style='Heading 2')
    table = doc.add_table(rows=3, cols=3)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    data = [('Indicator', 'Baseline', 'Endline'),
            ('Home visits within 48 h', '42 %', '68 %'),
            ('Newborns weighed', '55 %', '91 %')]
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            run = cell.paragraphs[0].runs[0]
            run.font.name = FONT
            run.font.size = Pt(10)
            if r == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                shade(cell, '123F6B')

    doc.save(path)
    return path


# --------------------------------------------------------- PowerPoint

def textbox(slide, left, top, width, height, text, size, color,
            bold=False, align=None, spacing=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    if align is not None:
        p.alignment = align
    run = p.runs[0]
    run.font.size = PPt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = FONT
    if spacing is not None:
        run.font._rPr.set('spc', str(int(spacing * 100)))
    return box


def band(slide, left, top, width, height, color):
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def build_pptx(path):
    prs = Presentation()
    prs.slide_width = PInches(13.333)      # 16:9
    prs.slide_height = PInches(7.5)
    W, H = prs.slide_width, prs.slide_height
    blank = prs.slide_layouts[6]

    # ---- 1. title slide
    s = prs.slides.add_slide(blank)
    band(s, 0, 0, W, PInches(0.14), P_NAVY)
    band(s, int(W * 0.62), 0, int(W * 0.26), PInches(0.14), P_CRIMSON)
    s.shapes.add_picture(LOGO, PInches(0.9), PInches(0.85), width=PInches(2.6))
    textbox(s, PInches(0.9), PInches(2.5), PInches(11), PInches(1.6),
            'Presentation title', 40, P_NAVY, bold=True)
    textbox(s, PInches(0.9), PInches(4.0), PInches(11), PInches(0.8),
            'Subtitle or event name', 18, P_MUTED)
    band(s, PInches(0.9), PInches(4.85), PInches(1.4), PInches(0.06), P_CRIMSON)
    textbox(s, PInches(0.9), PInches(5.2), PInches(11), PInches(0.6),
            'Presenter  ·  Date  ·  Location', 13, P_MUTED)

    # ---- 2. section divider
    s = prs.slides.add_slide(blank)
    band(s, 0, 0, W, H, P_NAVY)
    s.shapes.add_picture(LOGO_REV, PInches(0.9), PInches(0.8), width=PInches(2.4))
    textbox(s, PInches(0.9), PInches(3.0), PInches(11), PInches(1.4),
            'Section title', 36, P_WHITE, bold=True)
    band(s, PInches(0.9), PInches(4.4), PInches(1.4), PInches(0.06), P_CRIMSON)

    # ---- 3. content slide
    s = prs.slides.add_slide(blank)
    band(s, 0, 0, W, PInches(0.14), P_NAVY)
    band(s, int(W * 0.62), 0, int(W * 0.26), PInches(0.14), P_CRIMSON)
    textbox(s, PInches(0.9), PInches(0.6), PInches(11), PInches(0.9),
            'Slide title', 28, P_NAVY, bold=True)
    band(s, PInches(0.9), PInches(1.45), PInches(1.1), PInches(0.05), P_CRIMSON)

    body = s.shapes.add_textbox(PInches(0.9), PInches(1.9), PInches(11.5), PInches(4.4))
    tf = body.text_frame
    tf.word_wrap = True
    for i, (txt, level) in enumerate([
            ('First point', 0),
            ('Supporting detail', 1),
            ('Second point', 0),
            ('Third point', 0)]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ('— ' if level else '• ') + txt
        p.level = level
        p.space_after = PPt(10)
        run = p.runs[0]
        run.font.size = PPt(18 if level == 0 else 15)
        run.font.color.rgb = P_INK if level == 0 else P_MUTED
        run.font.name = FONT

    s.shapes.add_picture(MARK, PInches(12.5), PInches(6.75), height=PInches(0.4))

    # ---- 4. closing slide
    s = prs.slides.add_slide(blank)
    band(s, 0, 0, W, PInches(0.14), P_NAVY)
    band(s, int(W * 0.62), 0, int(W * 0.26), PInches(0.14), P_CRIMSON)
    s.shapes.add_picture(LOGO, PInches(4.6), PInches(2.6), width=PInches(4.1))
    textbox(s, PInches(0.9), PInches(4.3), PInches(11.5), PInches(0.6),
            'chimalayanepal.org', 16, P_MUTED, align=2)

    prs.save(path)
    return path


if __name__ == '__main__':
    print('wrote', build_docx(os.path.join(HERE, 'chimalaya-document.docx')))
    print('wrote', build_pptx(os.path.join(HERE, 'chimalaya-presentation.pptx')))
