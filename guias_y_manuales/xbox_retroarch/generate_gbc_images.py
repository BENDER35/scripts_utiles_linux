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
    draw.rectangle([(0, 85), (w, 88)], fill="#FFD700") # Gold / Yellow GBC accent line
    
    # GBC handheld mockup icon
    draw.rounded_rectangle([(38, 18), (84, 70)], radius=6, fill="#E6A100", outline="#FFFFFF", width=2)
    # Screen
    draw.rounded_rectangle([(44, 25), (78, 48)], radius=2, fill="#8BAC0F")
    # D-pad & buttons
    draw.text((46, 50), "+", font=ImageFont.truetype(FONT_BOLD, 14), fill="#333333")
    draw.ellipse([(68, 54), (74, 60)], fill="#D9381E")
    
    draw.text((105, 22), title, font=f_title, fill="#FFFFFF")
    draw.text((105, 56), subtitle, font=f_small, fill="#FFE082")

def draw_card(draw, x, y, w, h, title="", bg="#1E1E1E", border="#2D2D2D", radius=8):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=bg, outline=border, width=1)
    if title:
        _, _, _, _, f_bold = get_fonts(16, 14, 13, 11)
        draw.text((x + 16, y + 14), title, font=f_bold, fill="#FFD700")

# ==========================================================
# IMAGEN 21: ERROR EN GBC (WARIO LAND 3) - DIAGNÓSTICO
# ==========================================================
def gen_img_gbc_error():
    img = Image.new("RGB", (1200, 675), "#0D0D0D")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "DIAGNÓSTICO: ERROR DE CONTENIDO EN GAME BOY COLOR", "Fallo al iniciar 'Wario Land 3' y juegos de GBC en RetroArch Xbox")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    # RetroArch UI mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#15171C")
    
    # Left sidebar / Ozone UI
    draw.rectangle([(50, 110), (280, 630)], fill="#1E222B")
    draw.text((70, 130), "RETROARCH", font=f_bold, fill="#FFFFFF")
    draw.text((70, 175), "🎮 Menú principal", font=f_text, fill="#CCCCCC")
    draw.text((70, 215), "📁 Cargar contenido", font=f_bold, fill="#FFCC00")
    draw.text((70, 255), "🕹️ Game Boy Color", font=f_text, fill="#CCCCCC")
    
    # Center area showing game launch failure
    draw_card(draw, 310, 130, 810, 260, "", bg="#20242E", border="#383E4D")
    draw.text((340, 150), "Wario Land 3 (World) (En,Ja).gbc", font=f_title, fill="#FFFFFF")
    draw.text((340, 185), "Ruta: E:\\ROMS\\GBC\\Wario Land 3.gbc", font=f_small, fill="#8892B0")
    
    # Conflicted Cores
    draw.rounded_rectangle([(340, 215), (690, 255)], radius=6, fill="#2B303C")
    draw.text((355, 226), "Asociación incorrecta: gpSP / VBA-M ➔ ERROR", font=f_small, fill="#FFAAAA")
    draw.rounded_rectangle([(710, 215), (1060, 255)], radius=6, fill="#2B303C")
    draw.text((725, 226), "ROM en archivo .zip o permisos .srm ➔ CRASH", font=f_small, fill="#FFAAAA")
    
    # Notification Banner
    draw.rounded_rectangle([(340, 280), (1060, 330)], radius=6, fill="#4A1515", outline="#D9381E", width=2)
    draw.text((360, 292), "⚠️ Error en el contenido: no se puede cargar / Failed to load content", font=f_bold, fill="#FFAAAA")

    draw.text((340, 345), "Caso real reportado: La ROM de Wario Land 3 no arranca al ejecutarla.", font=f_small, fill="#FFD54F")

    # Bottom Diagnosis Box (4 Real Culprits)
    draw_card(draw, 310, 410, 810, 200, "CAUSAS TÉCNICAS DEL ERROR EN GAME BOY COLOR EN XBOX", bg="#1A1C23", border="#FFD700")
    
    causes = [
        "1. Núcleo no correspondiente: Si se intenta abrir con núcleos de GBA (como gpSP) falla al instante.",
        "2. Wario Land 3 requiere chip MBC3 + RTC (Reloj en tiempo real): Necesita crear 'Wario Land 3.srm' y '.rtc'.",
        "3. Permisos denegados en el pendrive E:\\: Al no poder crear el guardado .srm, la consola aborta el inicio.",
        "4. ROM comprimida en .zip / .7z con cabecera extra o nombres largos con corchetes tipo '(World) [!]'.",
        "5. Conflicto con 'gbc_bios.bin': A diferencia de GBA, GBC NO necesita BIOS. Una BIOS corrupta crashea el juego."
    ]
    cy = 445
    for c in causes:
        draw.text((330, cy), c, font=f_small, fill="#E6EDF3")
        cy += 28

    img.save(os.path.join(ASSETS_DIR, "img21_gbc_error_wario.png"))
    print("Generated img21_gbc_error_wario.png")

# ==========================================================
# IMAGEN 22: SOLUCIÓN DEFINITIVA GBC - NÚCLEO GAMBATTE
# ==========================================================
def gen_img_gbc_solucion():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SOLUCIÓN DEFINITIVA: CONFIGURACIÓN ÓPTIMA DE GAME BOY COLOR", "Uso del núcleo oficial Gambatte, descompresión de Wario Land 3 y permisos de guardado")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # 3 Column Cards Layout
    # Card 1: Core Selection: GAMBATTE
    draw_card(draw, 50, 120, 350, 500, "1. NÚCLEO OFICIAL: GAMBATTE", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(70, 165), (380, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((85, 175), "★ Gambatte (Recomendado)", font=f_bold, fill="#00FF66")
    draw.text((85, 198), "El estándar dorado en GB y GBC", font=f_small, fill="#CCFFCC")
    
    core_steps = [
        "• Por qué usar Gambatte:",
        "  Diseñado específicamente para",
        "  Game Boy y Game Boy Color.",
        "  100% compatible con chips",
        "  complejos como el MBC3 y RTC",
        "  de Wario Land 3 y Pokémon.",
        "",
        "• Cómo seleccionarlo:",
        "  Cargar contenido ➔",
        "  Wario Land 3.gbc ➔",
        "  Cargar con el núcleo ➔",
        "  'Nintendo - GB/Color (Gambatte)'"
    ]
    cy = 240
    for cs in core_steps:
        col = "#00FF66" if "Gambatte" in cs else "#CCCCCC"
        draw.text((80, cy), cs, font=f_small, fill=col)
        cy += 21

    # Card 2: ROM Preparation
    draw_card(draw, 425, 120, 350, 500, "2. ROM DESCOMPRIMIDA .GBC", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(445, 165), (755, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((460, 175), "Wario Land 3.gbc", font=f_bold, fill="#00FF66")
    draw.text((460, 198), "Extensión limpia obligatoria", font=f_small, fill="#CCFFCC")
    
    rom_steps = [
        "• Descomprime el archivo .zip:",
        "  No dejes 'Wario Land 3.zip'.",
        "  Extrae el archivo directo .gbc.",
        "",
        "• Renombra a un título limpio:",
        "  Quita corchetes molestos como",
        "  '[!]', '(World)' o '(En,Ja)'.",
        "  Deja solo 'Wario Land 3.gbc'.",
        "",
        "• Tamaño habitual:",
        "  2.097.152 bytes (2 MB exactos).",
        "  Verifica que no esté corrupta."
    ]
    ry = 240
    for rs in rom_steps:
        col = "#E5C07B" if "Wario Land 3.gbc" in rs else "#CCCCCC"
        draw.text((455, ry), rs, font=f_small, fill=col)
        ry += 21

    # Card 3: BIOS & Save Permissions (RTC)
    draw_card(draw, 800, 120, 350, 500, "3. BIOS Y GUARDADO RTC (.SRM)", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(820, 165), (1130, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((835, 175), "¡NO REQUIERE BIOS!", font=f_bold, fill="#00FF66")
    draw.text((835, 198), "Gambatte emula la BIOS por HLE", font=f_small, fill="#CCFFCC")
    
    bios_steps = [
        "• No necesitas 'gbc_bios.bin':",
        "  Gambatte tiene arranque nativo.",
        "  Si tienes un gbc_bios.bin que",
        "  no pesa 2.048 bytes (2 KB),",
        "  bórralo porque provocará error.",
        "",
        "• Permiso de escritura NTFS:",
        "  Wario Land 3 crea dos archivos:",
        "  'Wario Land 3.srm' (Partida)",
        "  'Wario Land 3.rtc' (Reloj interno)",
        "  El pendrive E:\\ DEBE tener",
        "  'ALL APPLICATION PACKAGES'."
    ]
    by = 240
    for bs in bios_steps:
        col = "#61AFEF" if ".srm" in bs or ".rtc" in bs else ("#FFAAAA" if "bórralo" in bs else "#CCCCCC")
        draw.text((830, by), bs, font=f_small, fill=col)
        by += 21

    img.save(os.path.join(ASSETS_DIR, "img22_gbc_solucion_gambatte.png"))
    print("Generated img22_gbc_solucion_gambatte.png")

if __name__ == "__main__":
    gen_img_gbc_error()
    gen_img_gbc_solucion()
    print("All GBC images generated successfully!")
