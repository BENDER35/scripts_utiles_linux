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
    draw.rectangle([(0, 85), (w, 88)], fill="#9C27B0") # Purple GBA accent line
    
    # GBA cart / logo mockup
    draw.rounded_rectangle([(38, 20), (84, 68)], radius=6, fill="#5C2D91", outline="#FFFFFF", width=2)
    draw.text((44, 30), "GBA", font=ImageFont.truetype(FONT_BOLD, 14), fill="#FFFFFF")
    draw.rectangle([(50, 52), (72, 60)], fill="#333333")
    
    draw.text((105, 22), title, font=f_title, fill="#FFFFFF")
    draw.text((105, 56), subtitle, font=f_small, fill="#BA68C8")

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
        draw.text((x + 16, y + 14), title, font=f_bold, fill="#BA68C8")

# ==========================================================
# IMAGEN 19: ERROR DE CONTENIDO EN GBA - DIAGNÓSTICO
# ==========================================================
def gen_img_gba_error():
    img = Image.new("RGB", (1200, 675), "#0D0D0D")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "DIAGNÓSTICO: ERROR DE CONTENIDO EN GAME BOY ADVANCE", "Fallo al cargar ROMs de GBA en RetroArch Xbox pese a tener seleccionada la BIOS")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    # RetroArch background mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#15171C")
    
    # Left: Ozone menu bar
    draw.rectangle([(50, 110), (280, 630)], fill="#1E222B")
    draw.text((70, 130), "RETROARCH", font=f_bold, fill="#FFFFFF")
    draw.text((70, 175), "🎮 Menú principal", font=f_text, fill="#CCCCCC")
    draw.text((70, 215), "📁 Cargar contenido", font=f_bold, fill="#FFCC00")
    draw.text((70, 255), "🕹️ Game Boy Advance", font=f_text, fill="#CCCCCC")
    
    # Center area showing the game launch failure
    draw_card(draw, 310, 130, 810, 260, "", bg="#20242E", border="#383E4D")
    draw.text((340, 150), "The Legend of Zelda - The Minish Cap.gba", font=f_title, fill="#FFFFFF")
    draw.text((340, 185), "Ruta: E:\\ROMS\\GBA\\The Legend of Zelda - The Minish Cap.gba", font=f_small, fill="#8892B0")
    
    # Cores tested
    draw.rounded_rectangle([(340, 215), (690, 255)], radius=6, fill="#2B303C")
    draw.text((355, 226), "Núcleo: Game Boy Advance (gpSP) ➔ CRASH", font=f_small, fill="#FFAAAA")
    draw.rounded_rectangle([(710, 215), (1060, 255)], radius=6, fill="#2B303C")
    draw.text((725, 226), "Núcleo: Game Boy Advance (mGBA) ➔ ERROR", font=f_small, fill="#FFAAAA")
    
    # Bottom notification banner (The exact RetroArch pop-up)
    draw.rounded_rectangle([(340, 280), (1060, 330)], radius=6, fill="#4A1515", outline="#D9381E", width=2)
    draw.text((360, 292), "⚠️ Error en el contenido: no se puede cargar / Failed to load content", font=f_bold, fill="#FFAAAA")

    draw.text((340, 345), "Estado reportado: Ruta de BIOS asignada en Ajustes, pero la ROM sigue sin arrancar.", font=f_small, fill="#E5C07B")

    # Bottom Diagnosis Box (4 Real Culprits)
    draw_card(draw, 310, 410, 810, 200, "¿POR QUÉ OCURRE SI YA SELECCIONASTE LA RUTA DE LA BIOS?", bg="#1A1C23", border="#BA68C8")
    
    causes = [
        "1. BIOS corrupta, falsa o con peso incorrecto: La BIOS de GBA DEBE pesar exactamente 16.384 bytes (16 KB).",
        "2. Nombre de archivo erróneo: Debe llamarse estrictamente 'gba_bios.bin' (en minúsculas; no 'GBA.BIN').",
        "3. El núcleo gpSP choca con Xbox: gpSP usa Dynarec (recompilador) que la seguridad UWP bloquea. Usar mGBA.",
        "4. ROM en formato .zip o .7z: RetroArch en Xbox falla al descomprimir si el zip contiene archivos extra o caracteres raros.",
        "5. Bloqueo de permisos al crear guardado (.srm): El núcleo aborta si la carpeta de guardado no tiene permisos de escritura."
    ]
    cy = 445
    for c in causes:
        draw.text((330, cy), c, font=f_small, fill="#E6EDF3")
        cy += 28

    img.save(os.path.join(ASSETS_DIR, "img19_gba_error_content.png"))
    print("Generated img19_gba_error_content.png")

# ==========================================================
# IMAGEN 20: PROTOCOLO DE SOLUCIÓN DEFINITIVA PARA GBA
# ==========================================================
def gen_img_gba_solucion():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SOLUCIÓN DEFINITIVA: PASOS PARA EJECUTAR GBA SIN ERRORES", "Verificación de BIOS (16 KB), núcleo mGBA / HLE y formato desarchivado .gba")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # 3 Column Cards Layout
    # Card 1: BIOS Integrity Check
    draw_card(draw, 50, 120, 350, 500, "1. VERIFICAR LA BIOS", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(70, 165), (380, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((85, 175), "gba_bios.bin", font=f_bold, fill="#00FF66")
    draw.text((85, 198), "Peso exacto: 16.384 bytes (16 KB)", font=f_small, fill="#CCFFCC")
    
    bios_steps = [
        "• Ubicación correcta:",
        "  E:\\RetroArch\\system\\gba_bios.bin",
        "",
        "• ¡Cuidado con internet!",
        "  Muchos sitios ofrecen volcados",
        "  de 32 KB o páginas HTML",
        "  renombradas a .bin que hacen",
        "  crashear al emulador.",
        "",
        "• Comprobación MD5 oficial:",
        "  a860e8c0b6d573d191e4ec7db1b1e4f6"
    ]
    by = 240
    for bs in bios_steps:
        col = "#E5C07B" if bs.startswith("  a8") or bs.startswith("  E:") else "#CCCCCC"
        draw.text((80, by), bs, font=f_small, fill=col)
        by += 21

    # Card 2: Core Selection (mGBA vs gpSP)
    draw_card(draw, 425, 120, 350, 500, "2. CAMBIAR AL NÚCLEO mGBA", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(445, 165), (755, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((460, 175), "★ Nintendo - GBA (mGBA)", font=f_bold, fill="#00FF66")
    draw.text((460, 198), "El núcleo más robusto en Xbox UWP", font=f_small, fill="#CCFFCC")
    
    core_steps = [
        "• NO utilices gpSP en Xbox:",
        "  gpSP requiere dynarec y crashea",
        "  con facilidad en Xbox Dev Mode.",
        "",
        "• mGBA tiene BIOS HLE propia:",
        "  Si tu BIOS da fallos, mGBA",
        "  puede arrancar el 100% de ROMs",
        "  con su emulación interna sin",
        "  necesitar archivo externo.",
        "",
        "• Alternativa muy ligera:",
        "  Nintendo - GBA (VBA Next)"
    ]
    cy = 240
    for cs in core_steps:
        col = "#E06C75" if cs.startswith("• NO") else ("#00FF66" if cs.startswith("• mGBA") else "#CCCCCC")
        draw.text((455, cy), cs, font=f_small, fill=col)
        cy += 21

    # Card 3: ROMs & Save Permissions
    draw_card(draw, 800, 120, 350, 500, "3. ROMS LIMPIAS Y PERMISOS", bg="#191B22", border="#303542")
    
    draw.rounded_rectangle([(820, 165), (1130, 225)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((835, 175), "Extensión limpia: .gba", font=f_bold, fill="#00FF66")
    draw.text((835, 198), "Descomprimir todo archivo .zip/.7z", font=f_small, fill="#CCFFCC")
    
    rom_steps = [
        "• Descomprime el juego en PC:",
        "  Guarda el archivo 'Juego.gba'.",
        "  Evita nombres con caracteres",
        "  extraños o símbolos como [!].",
        "",
        "• Permiso de escritura NTFS:",
        "  RetroArch crea 'Juego.srm'",
        "  al iniciar la ROM.",
        "  Si la carpeta E:\\ROMS\\GBA",
        "  o E:\\RetroArch\\saves",
        "  no tiene permiso 'Control Total',",
        "  el juego colapsa al arrancar."
    ]
    ry = 240
    for rs in rom_steps:
        col = "#61AFEF" if "Juego.gba" in rs or "Juego.srm" in rs else "#CCCCCC"
        draw.text((830, ry), rs, font=f_small, fill=col)
        ry += 21

    img.save(os.path.join(ASSETS_DIR, "img20_gba_solucion_paso_a_paso.png"))
    print("Generated img20_gba_solucion_paso_a_paso.png")

if __name__ == "__main__":
    gen_img_gba_error()
    gen_img_gba_solucion()
    print("All GBA images generated successfully!")
