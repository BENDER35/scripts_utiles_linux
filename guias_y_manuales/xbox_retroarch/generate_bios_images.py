import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "/home/bender/Descargas/manual_xbox_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def get_fonts(title_sz=28, sub_sz=20, text_sz=16, small_sz=13):
    return (
        ImageFont.truetype(FONT_BOLD, title_sz),
        ImageFont.truetype(FONT_BOLD, sub_sz),
        ImageFont.truetype(FONT_REG, text_sz),
        ImageFont.truetype(FONT_REG, small_sz),
        ImageFont.truetype(FONT_BOLD, text_sz)
    )

def draw_header(draw, title, subtitle, w=1200):
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(28, 19, 15, 12)
    draw.rectangle([(0, 0), (w, 85)], fill="#0D0D0D")
    draw.rectangle([(0, 85), (w, 88)], fill="#107C10")
    
    # Chip / BIOS icon mockup
    draw.rectangle([(38, 22), (82, 68)], fill="#107C10", outline="#FFFFFF", width=2)
    draw.rectangle([(48, 32), (72, 58)], fill="#1E1E1E")
    # Chip pins
    for py in [28, 38, 48, 58]:
        draw.line([(32, py), (38, py)], fill="#CCCCCC", width=2)
        draw.line([(82, py), (88, py)], fill="#CCCCCC", width=2)
    draw.text((52, 38), "B", font=ImageFont.truetype(FONT_BOLD, 16), fill="#00FF66")
    
    draw.text((105, 22), title, font=f_title, fill="#FFFFFF")
    draw.text((105, 56), subtitle, font=f_small, fill="#98C379")

def draw_button(draw, x, y, w, h, text, font, bg="#107C10", fg="#FFFFFF", border=None):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=6, fill=bg, outline=border, width=2 if border else 0)
    tx_bbox = font.getbbox(text)
    tw = tx_bbox[2] - tx_bbox[0]
    th = tx_bbox[3] - tx_bbox[1]
    draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 2), text, font=font, fill=fg)

def draw_card(draw, x, y, w, h, title="", bg="#1E1E1E", border="#2D2D2D", radius=8):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=bg, outline=border, width=1)
    if title:
        _, _, _, _, f_bold = get_fonts(16, 14, 13, 11)
        draw.text((x + 16, y + 14), title, font=f_bold, fill="#107C10")

# ==========================================================
# IMAGEN 17: COMPARATIVA PENDRIVE USB VS ALMACENAMIENTO INTERNO
# ==========================================================
def gen_img_bios_comparison():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "GESTIÓN DE BIOS: ¿PENDRIVE USB O ALMACENAMIENTO INTERNO?", "Análisis comparativo de rendimiento, seguridad de datos y facilidad de configuración")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Left Card: PENDRIVE USB (RECOMMENDED)
    draw_card(draw, 60, 120, 520, 500, "", bg="#142416", border="#107C10")
    draw.rectangle([(60, 120), (580, 126)], fill="#107C10")
    
    draw.rounded_rectangle([(80, 145), (420, 190)], radius=6, fill="#107C10")
    draw.text((95, 155), "★ OPCIÓN 1: PENDRIVE USB (E:\\)", font=f_bold, fill="#FFFFFF")
    draw.text((435, 158), "(100% RECOMENDADA)", font=ImageFont.truetype(FONT_BOLD, 14), fill="#00FF66")
    
    usb_points = [
        ("✓ Cero riesgo de pérdida:", "Las BIOS nunca se borran si reinstalas RetroArch o si sales/entras de Dev Mode."),
        ("✓ Gestión inmediata en PC:", "Copias y organizas cientos de BIOS en segundos conectando el pendrive al ordenador."),
        ("✓ Ahorro de espacio interno:", "No satura la partición SSD del sistema con BIOS pesadas (PS2, Dreamcast, Saturn)."),
        ("✓ Portabilidad absoluta:", "Llevas tu pendrive a cualquier otra Xbox o PC y tus emuladores arrancan al instante."),
        ("✓ Organización limpia:", "Todo centralizado en la carpeta E:\\RetroArch\\system\\ junto a tus ROMs y partidas.")
    ]
    uy = 210
    for title_p, desc_p in usb_points:
        draw.text((85, uy), title_p, font=f_bold, fill="#98C379")
        draw.text((85, uy + 22), desc_p, font=f_small, fill="#E0FFE0")
        uy += 52
        
    draw.rounded_rectangle([(80, 485), (560, 595)], radius=6, fill="#1B3820", outline="#107C10")
    draw.text((95, 498), "RUTA RECOMENDADA EN RETROARCH:", font=f_bold, fill="#00FF66")
    draw.text((95, 526), "E:\\RetroArch\\system\\", font=ImageFont.truetype(FONT_BOLD, 20), fill="#FFFFFF")
    draw.text((95, 560), "Permite compatibilidad directa con PS1, PS2, Saturn, SegaCD, Naomi...", font=ImageFont.truetype(FONT_REG, 11), fill="#CCCCCC")

    # Right Card: INTERNAL STORAGE (NOT RECOMMENDED)
    draw_card(draw, 620, 120, 520, 500, "", bg="#241616", border="#7A2222")
    draw.rectangle([(620, 120), (1140, 126)], fill="#D9381E")
    
    draw.rounded_rectangle([(640, 145), (960, 190)], radius=6, fill="#7A2222")
    draw.text((655, 155), "OPCIÓN 2: MEMORIA INTERNA (U:\\ / D:\\)", font=f_bold, fill="#FFAAAA")
    draw.text((975, 158), "(NO RECOMENDADA)", font=ImageFont.truetype(FONT_BOLD, 14), fill="#E06C75")
    
    internal_points = [
        ("✗ Riesgo constante de borrado:", "Si desinstalas la app, limpias caché o marcas sin querer 'Delete sideloaded', se pierden todas las BIOS."),
        ("✗ Transferencia muy lenta y tediosa:", "Obliga a usar el navegador del PC con Xbox Device Portal (puerto 11443) y subir archivo por archivo."),
        ("✗ Rutas confusas y ocultas:", "U:\\Users\\DefaultAccount\\AppData\\Local\\Packages\\...\\LocalState\\system"),
        ("✗ Límite de tamaño de subida:", "Device Portal suele dar errores de timeout al transferir archivos grandes (ej. BIOS de PS2 de 8 MB)."),
        ("✗ Falta de visibilidad:", "Dificulta revisar qué BIOS te faltan o verificar firmas hash MD5.")
    ]
    iy = 210
    for title_p, desc_p in internal_points:
        draw.text((645, iy), title_p, font=f_bold, fill="#FFAAAA")
        draw.text((645, iy + 22), desc_p, font=f_small, fill="#FFE0E0")
        iy += 52

    draw.rounded_rectangle([(640, 485), (1120, 595)], radius=6, fill="#381B1B", outline="#D9381E")
    draw.text((655, 498), "CONCLUSIÓN TÉCNICA:", font=f_bold, fill="#FFAAAA")
    draw.text((655, 526), "Carga siempre las BIOS en tu PENDRIVE USB (E:\\).", font=ImageFont.truetype(FONT_BOLD, 18), fill="#FFFFFF")
    draw.text((655, 560), "Es la práctica estándar en la comunidad de emulación de Xbox Dev Mode.", font=ImageFont.truetype(FONT_REG, 11), fill="#CCCCCC")

    img.save(os.path.join(ASSETS_DIR, "img17_bios_pendrive_vs_interno.png"))
    print("Generated img17_bios_pendrive_vs_interno.png")

# ==========================================================
# IMAGEN 18: CONFIGURACIÓN DE RUTA Y VERIFICACIÓN DE BIOS
# ==========================================================
def gen_img_config_bios():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO A PASO: VINCULAR Y VERIFICAR LAS BIOS EN RETROARCH", "Ajustar la ruta a E:\\RetroArch\\system y comprobar el estado en Información del Núcleo")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # RetroArch UI mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#15171C")
    
    # Path Bar
    draw.rectangle([(50, 110), (1150, 155)], fill="#1E222B")
    draw.text((70, 123), "Ruta: Ajustes ➔ Directorios (Directory) ➔ Sistema/BIOS ➔ Asignar 'E:\\RetroArch\\system'", font=f_bold, fill="#61AFEF")
    
    # Left Card: Directory Configuration in RetroArch
    draw_card(draw, 70, 175, 520, 430, "1. ASIGNACIÓN DEL DIRECTORIO SISTEMA/BIOS", bg="#191B22", border="#303542")
    
    dir_items = [
        ("Sistema/BIOS", "E:\\RetroArch\\system\\", True),
        ("Descargas (Downloads)", "E:\\RetroArch\\downloads\\", False),
        ("Partidas guardadas (Saves)", "E:\\RetroArch\\saves\\", False),
        ("Estados de guardado (States)", "E:\\RetroArch\\states\\", False),
        ("Capturas de pantalla", "E:\\RetroArch\\screenshots\\", False)
    ]
    dy = 220
    for dlabel, dpath, is_hl in dir_items:
        bg_col = "#153018" if is_hl else "#21252E"
        bd_col = "#00FF66" if is_hl else "#2F3542"
        draw.rounded_rectangle([(90, dy), (570, dy + 52)], radius=6, fill=bg_col, outline=bd_col, width=2 if is_hl else 1)
        draw.text((105, dy + 8), dlabel, font=f_bold, fill="#FFFFFF")
        draw.text((105, dy + 28), dpath, font=f_small, fill="#00FF66" if is_hl else "#8892B0")
        dy += 60

    draw.rectangle([(90, 525), (570, 585)], fill="#16222F", outline="#0080FF")
    draw.text((105, 535), "GUARDAR CAMBIO PERMANENTE:", font=f_bold, fill="#61AFEF")
    draw.text((105, 558), "Menú principal ➔ Archivo de configuración ➔ Guardar config actual.", font=ImageFont.truetype(FONT_REG, 11), fill="#E0E0E0")

    # Right Card: Core Information Verification (The checklist!)
    draw_card(draw, 610, 175, 520, 430, "2. COMPROBACIÓN DE ESTADO (INFORMACIÓN DEL NÚCLEO)", bg="#191B22", border="#303542")
    
    draw.text((630, 215), "Ejemplo: Núcleo Sony PlayStation (PCSX ReARMed / Beetle)", font=f_bold, fill="#FFFFFF")
    draw.text((630, 238), "Menú principal ➔ Cargar núcleo ➔ Información ➔ Información del núcleo", font=f_small, fill="#AAAAAA")
    
    # Checklist rows
    bios_checks = [
        ("scph5501.bin (PS1 NTSC-U)", "(!) Presente (MD5 correcto)", True),
        ("scph5500.bin (PS1 NTSC-J)", "(!) Presente (MD5 correcto)", True),
        ("scph5502.bin (PS1 PAL-EU)", "(!) Presente (MD5 correcto)", True),
        ("dc_boot.bin (Dreamcast)", "(!) Presente (Ruta: dc/dc_boot.bin)", True),
        ("neogeo.zip (Arcade/NeoGeo)", "(!) Presente (En raíz system)", True),
        ("ps2-0230a-20080220.bin (PS2)", "(!) Presente (Ruta: pcsx2/bios/)", True)
    ]
    by = 265
    for bfile, bstat, is_ok in bios_checks:
        draw.rounded_rectangle([(630, by), (1110, by + 40)], radius=5, fill="#1E222D")
        draw.text((645, by + 10), bfile, font=f_small, fill="#FFFFFF")
        draw.text((880, by + 10), bstat, font=f_bold, fill="#00FF66" if is_ok else "#FFAAAA")
        by += 46

    draw.rectangle([(630, 545), (1110, 595)], fill="#152615", outline="#254A25")
    draw.text((645, 555), "✓ Si aparece 'Presente' en verde, el juego arrancará al 100% sin fallos.", font=f_small, fill="#98C379")

    img.save(os.path.join(ASSETS_DIR, "img18_configurar_directorio_bios.png"))
    print("Generated img18_configurar_directorio_bios.png")

if __name__ == "__main__":
    gen_img_bios_comparison()
    gen_img_config_bios()
    print("All BIOS images generated successfully!")
