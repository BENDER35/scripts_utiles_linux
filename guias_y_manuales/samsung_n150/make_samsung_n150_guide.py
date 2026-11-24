import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
W = 2400
H = 2800

# Colors
BG = (248, 250, 252)          # Very light clean background
WHITE = (255, 255, 255)
HEADER_BG = (15, 23, 42)      # Deep Slate 900
TEXT_MAIN = (30, 41, 59)      # Slate 800
TEXT_MUTED = (100, 116, 139)  # Slate 500
BORDER = (203, 213, 225)      # Slate 300
BORDER_LIGHT = (226, 232, 240)

# Accent Colors
C_SCREEN = (2, 132, 199)      # Sky blue
C_KEYBOARD = (124, 58, 237)   # Purple
C_FRONT = (13, 148, 136)      # Teal
C_POWER = (220, 38, 38)       # Crimson Red (Highlighted)
C_POWER_BG = (255, 241, 242)  # Soft Rose / Red tint
C_SIDES = (234, 88, 12)       # Amber / Orange

# Fonts
f_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44)
f_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
f_head = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
f_subhead = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
f_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
f_body_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
f_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
f_small_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
f_tiny = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)

img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# ----------------- 1. HEADER -----------------
draw.rectangle([0, 0, W, 130], fill=HEADER_BG)
draw.text((60, 26), "PORTÁTIL SAMSUNG N150 — GUÍA VISUAL COMPLETA", fill=WHITE, font=f_title)
draw.text((60, 84), "Identificación de partes: Pantalla, Teclado, Frontal (Botón de Encendido deslizante) y Laterales", fill=(148, 163, 184), font=f_subtitle)

def draw_panel(box, fill=WHITE, outline=BORDER, radius=12, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_badge(x, y, text, color, font=f_small_bold):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 10, 5
    draw.rounded_rectangle([x, y, x + tw + px*2, y + th + py*2], radius=6, fill=color)
    draw.text((x + px, y + py - bbox[1]), text, fill=WHITE, font=font)
    return tw + px*2

def draw_callout_box(box, category, title, desc_lines, accent_color, badge_text=None):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=WHITE, outline=accent_color, width=2)
    draw.rectangle([x0+2, y0+2, x0+8, y1-2], fill=accent_color)
    
    cur_x = x0 + 18
    cur_y = y0 + 12
    if badge_text:
        bw = draw_badge(cur_x, cur_y, badge_text, accent_color)
        cur_x += bw + 10
    
    draw.text((cur_x, cur_y + 2), title, fill=accent_color, font=f_subhead)
    
    line_y = y0 + 44
    for line in desc_lines:
        draw.text((x0 + 18, line_y), line, fill=TEXT_MAIN, font=f_body)
        line_y += 22

def draw_arrow(start, end, color=C_POWER, width=3, r=6):
    draw.line([start, end], fill=color, width=width)
    draw.ellipse([end[0]-r, end[1]-r, end[0]+r, end[1]+r], fill=color, outline=WHITE, width=2)

# ----------------- 2. MAIN VIEW PANEL -----------------
MAIN_PANEL = (50, 150, 2350, 1680)
draw_panel(MAIN_PANEL)
draw.text((80, 175), "1. VISTA GENERAL ABIERTA — PANTALLA, TECLADO Y PARTE FRONTAL", fill=HEADER_BG, font=f_head)
draw.line([80, 215, 2320, 215], fill=BORDER_LIGHT, width=1)

# Paste Laptop
laptop_front = Image.open('samsung_n150_front.png').convert('RGBA')
laptop_crop = laptop_front.crop((180, 15, 1740, 1140))
tw = 1440
th = int(tw * (laptop_crop.height / laptop_crop.width))
laptop_resized = laptop_crop.resize((tw, th), Image.LANCZOS)

laptop_x = 480
laptop_y = 230
img.paste(laptop_resized, (laptop_x, laptop_y), laptop_resized)

scale = tw / 1560
def to_canvas(ox, oy):
    return (laptop_x + int((ox - 180) * scale), laptop_y + int((oy - 15) * scale))

# Targets on laptop
pt_webcam = to_canvas(960, 70)
pt_screen = to_canvas(960, 420)
pt_hinge = to_canvas(370, 780)
pt_keyboard = to_canvas(960, 890)
pt_touchpad = to_canvas(960, 1005)
pt_leds = to_canvas(515, 1085)
pt_card = to_canvas(960, 1100)
pt_power = to_canvas(1380, 1088)

# --- LEFT CALLOUTS (PANTALLA & BISAGRA) ---
draw_callout_box((80, 250, 460, 370), "PANTALLA", "CÁMARA DIGITAL LIVECAM", 
                 ["• Cámara web integrada 0.3 MP", "• Micrófono digital superior", "• Indicador LED de cámara activa"], 
                 C_SCREEN, "PANTALLA")
draw_arrow((460, 310), pt_webcam, C_SCREEN)

draw_callout_box((80, 410, 460, 550), "PANTALLA", "PANTALLA LCD 10.1\" MATE",
                 ["• Panel WSVGA 1024 x 600 píxeles", "• Acabado mate antirreflejos", "• Retroiluminación LED de bajo consumo"],
                 C_SCREEN, "PANTALLA")
draw_arrow((460, 480), (pt_screen[0]-240, pt_screen[1]), C_SCREEN)

draw_callout_box((80, 680, 460, 800), "PANTALLA", "BISAGRAS INTEGRADAS",
                 ["• Mecanismo reforzado de 135°", "• Perfil aerodinámico curvo", "• Cierre magnético sin pestillo"],
                 C_SCREEN, "PANTALLA")
draw_arrow((460, 740), pt_hinge, C_SCREEN)

draw_callout_box((80, 1000, 460, 1160), "FRONTAL", "INDICADORES LED FRONTALES",
                 ["• Bloq Mayús / Scroll Lock", "• Actividad de Disco Duro (HDD)", "• Estado de Red Wi-Fi", "• Carga de Batería y Encendido"],
                 C_FRONT, "FRONTAL")
draw_arrow((460, 1080), pt_leds, C_FRONT)

# --- RIGHT CALLOUTS (TECLADO & TOUCHPAD) ---
draw_callout_box((1940, 680, 2320, 820), "TECLADO", "TECLADO TIPO ISLA (CHICLET)",
                 ["• 83 teclas ergonómicas espaciadas", "• Mayor comodidad y precisión", "• Teclas de acceso rápido Fn (F1-F12)"],
                 C_KEYBOARD, "TECLADO")
draw_arrow((1940, 750), (pt_keyboard[0]+280, pt_keyboard[1]), C_KEYBOARD)

draw_callout_box((1940, 910, 2320, 1040), "TECLADO", "TOUCHPAD TÁCTIL",
                 ["• Superficie multitáctil sensible", "• Barra basculante clic izq./der.", "• Reposamuñecas amplio"],
                 C_KEYBOARD, "TECLADO")
draw_arrow((1940, 975), (pt_touchpad[0]+280, pt_touchpad[1]), C_KEYBOARD)

# --- BOTTOM CENTER: CARD READER ---
draw_callout_box((680, 1340, 1140, 1450), "FRONTAL", "LECTOR DE TARJETAS 3 EN 1",
                 ["• Compatible con SD, SDHC y MMC", "• Borde frontal central inferior"],
                 C_FRONT, "FRONTAL")
draw_arrow((910, 1340), pt_card, C_FRONT)

# --- HIGHLIGHTED POWER BUTTON CALLOUT (SPECIAL FOCUS) ---
POWER_BOX = (1200, 1280, 2320, 1650)
draw.rounded_rectangle(POWER_BOX, radius=14, fill=C_POWER_BG, outline=C_POWER, width=3)

# Zoomed image of power button on the left of POWER_BOX
crop_power = Image.open('crop_power.jpg')
cp_w, cp_h = 360, 135
crop_power_res = crop_power.resize((cp_w, cp_h), Image.LANCZOS)
# Zoom box frame
draw.rectangle([1225-2, 1350-2, 1225+cp_w+2, 1350+cp_h+2], fill=WHITE, outline=C_POWER, width=2)
img.paste(crop_power_res, (1225, 1350))
draw.text((1235, 1350 + cp_h + 8), "DETALLE REAL: INTERRUPTOR CON RESORTE", fill=C_POWER, font=f_small_bold)
draw.text((1235, 1350 + cp_h + 26), "Icono '⏻/I' superior + pestaña con flecha ▶", fill=TEXT_MUTED, font=f_small)

# Header inside POWER_BOX (to the right of the arrow entry)
draw_badge(1630, 1295, "★ PARTE CLAVE DESTACADA", C_POWER, f_subhead)
draw.text((1950, 1300), "BOTÓN DE ENCENDIDO", fill=C_POWER, font=f_head)

# Details in the right column
px_lbl = 1630
px_val = 1810
items = [
    ("• UBICACIÓN:", "Borde frontal derecho (debajo del reposamuñecas)."),
    ("• MECANISMO:", "Interruptor DESLIZANTE con resorte (NO es botón pulsador)."),
    ("• ACCIÓN:", "Deslizar la pestaña hacia la DERECHA (▶) y soltar para encender."),
    ("• MARCAS:", "Grabado con el icono universal de energía '⏻/I' sobre el borde blanco."),
    ("• SUSPENSIÓN:", "Un toque deslizante rápido pone el portátil en modo reposo / lo reactiva."),
    ("• CONFUSIÓN:", "Muchos usuarios lo buscan arriba del teclado; en el N150 está en el frontal.")
]

py_line = 1350
for lbl, val in items:
    draw.text((px_lbl, py_line), lbl, fill=C_POWER if "MECANISMO" in lbl or "ACCIÓN" in lbl else TEXT_MAIN, font=f_body_bold)
    # Check width to avoid overflow
    draw.text((px_val, py_line), val, fill=(185, 28, 28) if "MECANISMO" in lbl or "ACCIÓN" in lbl else TEXT_MAIN, font=f_body_bold if "MECANISMO" in lbl else f_body)
    py_line += 26

# Prominent red circle on the laptop's actual power slider
draw.ellipse([pt_power[0]-14, pt_power[1]-14, pt_power[0]+14, pt_power[1]+14], fill=None, outline=C_POWER, width=4)
# Arrow connecting the Zoom Frame directly to the laptop target
draw_arrow((1400, 1350), pt_power, C_POWER, width=4, r=8)


# ----------------- 3. BOTTOM PANELS: SIDES (LATERALES) -----------------
SIDE_Y = 1720
SIDE_H = 1030
PANEL_W = 1120

# Panel Left Side
PANEL_LEFT = (50, SIDE_Y, 50 + PANEL_W, SIDE_Y + SIDE_H)
draw_panel(PANEL_LEFT)
draw_badge(75, SIDE_Y + 20, "LATERAL", C_SIDES)
draw.text((180, SIDE_Y + 20), "2. VISTA LATERAL IZQUIERDA — PUERTOS Y CONEXIONES", fill=HEADER_BG, font=f_head)
draw.line([75, SIDE_Y + 60, 50 + PANEL_W - 25, SIDE_Y + 60], fill=BORDER_LIGHT, width=1)

# Left Side Image
img_left = Image.open('nbc_full_55.jpg')
il_w = PANEL_W - 50
il_h = int(il_w * (img_left.height / img_left.width))
img_left_res = img_left.resize((il_w, il_h), Image.LANCZOS)
base_lx = 75
base_ly = SIDE_Y + 80
img.paste(img_left_res, (base_lx, base_ly))

ports_left = [
    ("1. ALIMENTACIÓN CC (DC-IN 19V)", "Conector cilíndrico para el cargador de red eléctrica original.", 0.307, 0.567),
    ("2. PUERTO DE RED ETHERNET (LAN RJ-45)", "Conector Fast Ethernet 10/100 Mbps con solapa abatible.", 0.393, 0.583),
    ("3. REJILLA DE VENTILACIÓN ACTIVA", "Salida de aire caliente impulsada por el disipador interno.", 0.543, 0.600),
    ("4. PUERTO USB 2.0 (SLEEP & CHARGE)", "Permite transferencias y carga de móviles con el equipo apagado.", 0.679, 0.600),
    ("5. SALIDA DE AUDIO / AURICULARES (3.5 mm)", "Jack estéreo analógico para auriculares o altavoces externos.", 0.739, 0.617),
    ("6. ENTRADA DE MICRÓFONO (3.5 mm)", "Jack analógico para micrófono externo o equipo de grabación.", 0.796, 0.617),
]

# Draw exact pins on Left Side image
for i, (title, desc, rx, ry) in enumerate(ports_left, 1):
    px = base_lx + int(rx * il_w)
    py = base_ly + int(ry * il_h)
    draw.ellipse([px-7, py-7, px+7, py+7], fill=C_POWER, outline=WHITE, width=2)
    draw.text((px-5, py-19), str(i), fill=C_POWER, font=f_small_bold)

# Descriptions below left image
card_ly = base_ly + il_h + 35
for title, desc, rx, ry in ports_left:
    draw.rounded_rectangle([75, card_ly, 75 + il_w, card_ly + 64], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((95, card_ly + 10), title, fill=HEADER_BG, font=f_body_bold)
    draw.text((95, card_ly + 35), desc, fill=TEXT_MUTED, font=f_small)
    card_ly += 74


# Panel Right Side
PANEL_RIGHT = (W - 50 - PANEL_W, SIDE_Y, W - 50, SIDE_Y + SIDE_H)
draw_panel(PANEL_RIGHT)
base_rx = W - 50 - PANEL_W + 25
base_ry = SIDE_Y + 80

draw_badge(base_rx, SIDE_Y + 20, "LATERAL", C_SIDES)
draw.text((base_rx + 105, SIDE_Y + 20), "3. VISTA LATERAL DERECHA — PUERTOS Y CONEXIONES", fill=HEADER_BG, font=f_head)
draw.line([base_rx, SIDE_Y + 60, W - 75, SIDE_Y + 60], fill=BORDER_LIGHT, width=1)

# Right Side Image
img_right = Image.open('nbc_full_57.jpg')
img_right_res = img_right.resize((il_w, il_h), Image.LANCZOS)
img.paste(img_right_res, (base_rx, base_ry))

ports_right = [
    ("1. INTERRUPTOR INALÁMBRICO / BANDEJA SIM", "Conmutador de radio Wi-Fi / ranura 3G opcional según versión.", 0.268, 0.517),
    ("2. PUERTOS USB 2.0 ADICIONALES (x2)", "2 conexiones USB para ratón, pendrive o accesorios.", 0.428, 0.550),
    ("3. SALIDA DE VÍDEO VGA (D-SUB 15 PINES)", "Conexión a pantalla externa, monitor o proyector analógico.", 0.600, 0.533),
    ("4. RANURA DE SEGURIDAD KENSINGTON", "Anclaje antirrobo estándar mediante cable de acero con llave.", 0.768, 0.417),
    ("5. ESTRUCTURA DE BISAGRA Y BATERÍA", "Soporte cilíndrico posterior que aloja la batería extendida.", 0.865, 0.480),
]

# Draw exact pins on Right Side image
for i, (title, desc, rx, ry) in enumerate(ports_right, 1):
    px = base_rx + int(rx * il_w)
    py = base_ry + int(ry * il_h)
    draw.ellipse([px-7, py-7, px+7, py+7], fill=C_POWER, outline=WHITE, width=2)
    draw.text((px-5, py-19), str(i), fill=C_POWER, font=f_small_bold)

# Descriptions below right image
card_ry = base_ry + il_h + 35
for title, desc, rx, ry in ports_right:
    draw.rounded_rectangle([base_rx, card_ry, base_rx + il_w, card_ry + 64], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((base_rx + 20, card_ry + 10), title, fill=HEADER_BG, font=f_body_bold)
    draw.text((base_rx + 20, card_ry + 35), desc, fill=TEXT_MUTED, font=f_small)
    card_ry += 74

# Specs summary box
draw.rounded_rectangle([base_rx, card_ry, base_rx + il_w, card_ry + 130], radius=8, fill=(241, 245, 249), outline=BORDER, width=1)
draw.text((base_rx + 20, card_ry + 15), "RESUMEN DE ESPECIFICACIONES TÉCNICAS (SAMSUNG N150)", fill=HEADER_BG, font=f_subhead)
specs = [
    "• Procesador: Intel Atom N450 (1.66 GHz, 512 KB L2 Cache) | Gráficos: Intel GMA 3150",
    "• Pantalla: 10.1 pulgadas WSVGA LED (1024 x 600) mate antirreflectante",
    "• Almacenamiento y RAM: Disco duro SATA 160 GB / 250 GB + 1 GB DDR2 (ampliable a 2 GB)",
    "• Conectividad: Wi-Fi 802.11b/g/n, Fast Ethernet 10/100, Bluetooth 2.1+EDR (opcional 3G HSPA)"
]
sy = card_ry + 45
for s in specs:
    draw.text((base_rx + 20, sy), s, fill=TEXT_MUTED, font=f_small)
    sy += 19

# ----------------- 4. FOOTER -----------------
draw.rectangle([0, H - 40, W, H], fill=HEADER_BG)
draw.text((60, H - 28), "Infografía técnica generada para portátil Samsung Serie N (N150 / NP-N150 / N150 Plus). Guardado en formato JPG.", fill=(148, 163, 184), font=f_tiny)

# Save final JPG
output_path = '/home/bender/Descargas/samsung_n150_partes.jpg'
img.save(output_path, 'JPEG', quality=95)
print(f"Final image successfully saved to: {output_path}")
