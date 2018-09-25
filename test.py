import os
import re

from emojipy import Emoji
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

# Pdf doesn't need any unicode inside <image>'s alt attribute
Emoji.unicode_alt = False


def replace_with_emoji_pdf(text, size):
    """
    Reportlab's Paragraph doesn't accept normal html <image> tag's attributes
    like 'class', 'alt'. Its a little hack to remove those attrbs
    """
    text = Emoji.to_image(text)
    text = text.replace('class="emojione"', 'height=%s width=%s' %
                        (size, size))
    return re.sub('alt="'+Emoji.shortcode_regexp+'"', '', text)

# Register font 'font_file' is location of symbola.ttf file

font_file = os.getcwd() + '/Symbola.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)

width, height = A4
pdf_content = "Ejemplo \u263A \U0001F61C."

styles = getSampleStyleSheet()
styles["Title"].fontName = 'Symbola'
style = styles["Title"]
content = replace_with_emoji_pdf(Emoji.to_image(pdf_content), style.fontSize)

para = Paragraph(content, style)
canv = canvas.Canvas('emoji.pdf')

para.wrap(width, height)
para.drawOn(canv, 0, height/2)

canv.save()
