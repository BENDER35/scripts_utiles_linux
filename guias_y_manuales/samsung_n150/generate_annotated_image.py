import os
from PIL import Image, ImageDraw, ImageFont

# Canvas size
CANVAS_W = 2400
CANVAS_H = 2600

# Colors
BG_COLOR = (248, 250, 252) # Light sleek gray
HEADER_BG = (15, 23, 42)    # Slate 900
PANEL_BG = (255, 255, 255)
BORDER_COLOR = (226, 232, 240)

# Category colors
COLOR_SCREEN = (2, 132, 199)     # Sky blue
COLOR_KEYBOARD = (147, 51, 234)  # Purple
COLOR_FRONT = (13, 148, 136)     # Teal
COLOR_POWER = (220, 38, 38)      # Crimson Red (Highlighted)
COLOR_SIDES = (234, 88, 12)      # Amber/Orange

# Fonts
font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
font_section = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
font_badge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_text = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
font_text_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
font_small_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)

img = Image.new('RGB', (CANVAS_W, CANVAS_H), BG_COLOR)
draw = ImageDraw.Draw(img)

# 1. Header Banner
draw.rectangle([0, 0, CANVAS_W, 140], fill=HEADER_BG)
draw.text((60, 30), "SAMSUNG N150 NETBOOK — GUÍA DE PARTES Y COMPONENTES", fill=(255, 255, 255), font=font_title)
draw.text((60, 90), "Desglose visual detallado: Pantalla, Teclado, Frontal (Botón de encendido) y Laterales", fill=(148, 163, 184), font=font_subtitle)

# Helper for drawing cards
def draw_card(box, title=None, badge_color=None):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=PANEL_BG, outline=BORDER_COLOR, width=2)
    if title:
        draw.text((x0 + 24, y0 + 18), title, fill=badge_color if badge_color else (30, 41, 59), font=font_section)
        draw.line([x0 + 24, y0 + 58, x1 - 24, y0 + 58], fill=BORDER_COLOR, width=1)

# Main front laptop view container
MAIN_BOX = (60, 160, 2340, 1600)
draw_card(MAIN_BOX, "1. VISTA PRINCIPAL: PANTALLA, TECLADO Y PARTE FRONTAL", (15, 23, 42))

# Load front image
laptop_front = Image.open('samsung_n150_front.png').convert('RGBA')
# Crop white borders tightly
laptop_crop = laptop_front.crop((180, 15, 1740, 1140))
# Target width ~ 1550
target_w = 1500
aspect = laptop_crop.height / laptop_crop.width
target_h = int(target_w * aspect)
laptop_resized = laptop_crop.resize((target_w, target_h), Image.LANCZOS)

# Paste laptop image in center of main box
laptop_x = 60 + (2280 - target_w) // 2
laptop_y = 230
img.paste(laptop_resized, (laptop_x, laptop_y), laptop_resized)

print("Laptop pasted at:", laptop_x, laptop_y, "size:", target_w, target_h)

# Save intermediate to check coordinates
img.save('test_layout.jpg', 'JPEG', quality=90)
print("Saved test_layout.jpg")
