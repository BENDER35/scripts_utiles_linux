import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Base paths
font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_reg_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

font_title = ImageFont.truetype(font_bold_path, 42)
font_subtitle = ImageFont.truetype(font_reg_path, 22)
font_sec_title = ImageFont.truetype(font_bold_path, 26)
font_badge = ImageFont.truetype(font_bold_path, 18)
font_label_b = ImageFont.truetype(font_bold_path, 20)
font_label = ImageFont.truetype(font_reg_path, 18)
font_small = ImageFont.truetype(font_reg_path, 16)
font_small_b = ImageFont.truetype(font_bold_path, 16)
font_micro = ImageFont.truetype(font_reg_path, 14)

# Create canvas
W, H = 2600, 2300
canvas = Image.new("RGB", (W, H), (245, 247, 250))
draw = ImageDraw.Draw(canvas)

# 1. Header Banner
draw.rectangle([(0, 0), (W, 110)], fill=(24, 32, 47))
# Decorative accent line
draw.rectangle([(0, 110), (W, 116)], fill=(220, 53, 69)) # Red accent for power focus

draw.text((50, 22), "SAMSUNG N150 / NP-N150  —  GUÍA VISUAL DE PARTES Y COMPONENTES", fill=(255, 255, 255), font=font_title)
draw.text((50, 72), "Identificación completa: Pantalla, Teclado, Frontal, Laterales y Enfoque Especial en el Botón de Encendido", fill=(180, 200, 225), font=font_subtitle)

# Helper function for card drawing
def draw_card(box, title, title_color=(30, 41, 59), bg_color=(255, 255, 255), border_color=(226, 232, 240)):
    x1, y1, x2, y2 = box
    # shadow
    draw.rounded_rectangle([(x1+2, y1+2), (x2+2, y2+2)], radius=12, fill=(230, 234, 240))
    # card body
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=12, fill=bg_color, outline=border_color, width=2)
    if title:
        draw.text((x1 + 25, y1 + 18), title, fill=title_color, font=font_sec_title)
        draw.line([(x1 + 20, y1 + 56), (x2 - 20, y1 + 56)], fill=(235, 238, 245), width=1)

print("Canvas initialized successfully.")
