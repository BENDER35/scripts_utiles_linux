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
    draw.rectangle([(0, 85), (w, 88)], fill="#D9381E") # Red error line
    
    # RetroArch / N64 Logo circle
    draw.ellipse([(35, 20), (85, 70)], fill="#3F51B5")
    draw.ellipse([(43, 28), (77, 62)], fill="#1E1E1E")
    draw.text((50, 31), "64", font=ImageFont.truetype(FONT_BOLD, 22), fill="#FFD700")
    
    draw.text((105, 22), title, font=f_title, fill="#FFFFFF")
    draw.text((105, 56), subtitle, font=f_small, fill="#E06C75")

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
# IMAGEN 13: PANTALLA RETROARCH - ERROR AL INICIAR NÚCLEO N64
# ==========================================================
def gen_img_n64_error():
    img = Image.new("RGB", (1200, 675), "#0D0D0D")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "ERROR RETROARCH XBOX: 'FALLO EN EL NÚCLEO AL INICIAR'", "Fallo de ejecución con Nintendo 64 (Mupen64Plus-Next y ParaLLEl N64)")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    # Background: RetroArch XMB / Ozone theme mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#15171C")
    
    # Left sidebar / Ozone UI
    draw.rectangle([(50, 110), (280, 630)], fill="#1E222B")
    draw.text((70, 130), "RETROARCH", font=f_bold, fill="#FFFFFF")
    draw.text((70, 175), "🎮 Menú principal", font=f_text, fill="#CCCCCC")
    draw.text((70, 215), "⚙️ Ajustes", font=f_text, fill="#CCCCCC")
    draw.text((70, 255), "📁 Cargar contenido", font=f_bold, fill="#FFCC00")
    draw.text((70, 295), "🕹️ Nintendo 64", font=f_text, fill="#CCCCCC")
    
    # Center area showing game launch failure
    draw_card(draw, 310, 130, 810, 280, "", bg="#20242E", border="#383E4D")
    draw.text((340, 150), "Super Mario 64 (USA).z64", font=f_title, fill="#FFFFFF")
    draw.text((340, 185), "Ruta: E:\\RetroArch\\ROMS\\N64\\Super Mario 64 (USA).z64", font=f_small, fill="#8892B0")
    
    # Core selection
    draw.rounded_rectangle([(340, 220), (700, 265)], radius=6, fill="#2B303C")
    draw.text((355, 233), "Núcleo: Nintendo - Nintendo 64 (Mupen64Plus-Next)", font=f_small, fill="#E0E0E0")
    
    draw.rounded_rectangle([(340, 280), (700, 325)], radius=6, fill="#2B303C")
    draw.text((355, 293), "Núcleo: Nintendo - Nintendo 64 (ParaLLEl N64)", font=f_small, fill="#E0E0E0")
    
    # RetroArch Bottom Notification Banner (The exact yellow/red error box)
    draw.rounded_rectangle([(340, 345), (1080, 395)], radius=6, fill="#4A1515", outline="#D9381E", width=2)
    draw.text((360, 357), "⚠️  Error en el contenido: Fallo en el núcleo al iniciarlo / Failed to open libretro core", font=f_bold, fill="#FFAAAA")

    # Bottom Diagnosis Box
    draw_card(draw, 310, 430, 810, 180, "DIAGNÓSTICO TÉCNICO: ¿POR QUÉ FALLA EN XBOX UWP?", bg="#1A1C23", border="#D9381E")
    causes = [
        "1. RetroArch configurado como 'App' en vez de 'Game' en Dev Home (límite estricto de RAM y CPU).",
        "2. Controlador de vídeo incompatible: Mupen64Plus requiere 'd3d11'. Si está en 'd3d12' o 'gl' colapsa.",
        "3. ParaLLEl N64 intenta inicializar 'Vulkan': Xbox NO tiene soporte Vulkan. Provoca crash inmediato.",
        "4. ROMs comprimidas en ZIP/7Z en vez de sin comprimir (.z64/.n64) o permisos bloqueados en USB E:\\."
    ]
    cy = 465
    for c in causes:
        draw.text((330, cy), c, font=f_small, fill="#E6EDF3")
        cy += 26

    img.save(os.path.join(ASSETS_DIR, "img13_retroarch_n64_error.png"))
    print("Generated img13_retroarch_n64_error.png")

# ==========================================================
# IMAGEN 14: CAMBIO A "GAME" EN DEV HOME (SOLUCIÓN CLAVE)
# ==========================================================
def gen_img_app_type_game():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 1 FUNDAMENTAL: CAMBIAR RETROARCH DE 'APP' A 'GAME'", "Liberar el 100% de CPU, memoria RAM y aceleración DirectX en Xbox Dev Home")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Dev Home background mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#161616")
    
    # Left: Tiles list
    draw_card(draw, 70, 130, 480, 480, "DEV HOME - APLICACIONES INSTALADAS", bg="#1E1E1E", border="#333333")
    
    # RetroArch tile selected
    draw.rounded_rectangle([(90, 180), (530, 280)], radius=8, fill="#122B15", outline="#107C10", width=3)
    draw.text((110, 200), "RetroArch", font=ImageFont.truetype(FONT_BOLD, 24), fill="#FFFFFF")
    draw.text((110, 235), "Estado: Seleccionado | Pulsa botón [Vista / Back] para opciones", font=f_small, fill="#98C379")
    
    # Other tiles
    draw.rounded_rectangle([(90, 295), (530, 360)], radius=6, fill="#252525")
    draw.text((110, 315), "Dev Home Settings", font=f_bold, fill="#888888")
    draw.rounded_rectangle([(90, 375), (530, 440)], radius=6, fill="#252525")
    draw.text((110, 395), "Xbox Device Portal", font=f_bold, fill="#888888")

    # Controller prompt hint
    draw.rectangle([(90, 460), (530, 580)], fill="#16222F", outline="#0080FF", width=1)
    draw.text((105, 475), "CÓMO ABRIR EL MENÚ DE DETALLES:", font=f_bold, fill="#61AFEF")
    draw.text((105, 505), "1. Resalta el mosaico de RetroArch.", font=f_small, fill="#E0E0E0")
    draw.text((105, 528), "2. Pulsa el botón [Vista / Menú] del mando.", font=f_small, fill="#E0E0E0")
    draw.text((105, 551), "3. Selecciona 'View details' (Ver detalles).", font=f_small, fill="#E0E0E0")

    # Right: View details modal dialog
    draw_card(draw, 580, 130, 550, 480, "VIEW DETAILS - CONFIGURACIÓN DEL PAQUETE", bg="#222222", border="#444444")
    
    draw.text((610, 180), "Package: RetroArch UWP", font=f_bold, fill="#FFFFFF")
    draw.text((610, 210), "Publisher: Libretro Team", font=f_small, fill="#AAAAAA")
    
    # App Type Selector
    draw.text((610, 250), "App type (Tipo de aplicación):", font=f_bold, fill="#FFFFFF")
    
    # Comparison boxes
    # Old mode: App (Red/Limited)
    draw.rounded_rectangle([(610, 280), (840, 350)], radius=6, fill="#2B1515", outline="#772222")
    draw.text((625, 292), "App (Por defecto)", font=f_bold, fill="#FFAAAA")
    draw.text((625, 318), "✗ Solo 1-2 GB RAM\n✗ 1 Núcleo CPU (Crash en N64)", font=ImageFont.truetype(FONT_REG, 10), fill="#DD8888")
    
    # New mode: Game (Green/Full) - SELECTED!
    draw.rounded_rectangle([(860, 280), (1090, 350)], radius=6, fill="#123512", outline="#00FF66", width=3)
    draw.text((875, 292), "Game (Juego) ★", font=f_bold, fill="#00FF66")
    draw.text((875, 318), "✓ 5+ GB RAM disponibles\n✓ Todos los núcleos CPU activos", font=ImageFont.truetype(FONT_REG, 10), fill="#CCFFCC")

    # Action instructions
    draw.rectangle([(610, 375), (1090, 500)], fill="#181818", outline="#383838")
    draw.text((625, 390), "PASOS EXACTOS:", font=f_bold, fill="#E5C07B")
    draw.text((625, 418), "1. Cambia 'App type' de 'App' a 'Game'.", font=f_small, fill="#FFFFFF")
    draw.text((625, 442), "2. Pulsa [A] para guardar los cambios.", font=f_small, fill="#FFFFFF")
    draw.text((625, 466), "3. REINICIA LA CONSOLA para aplicar la asignación de hardware.", font=f_small, fill="#00FF66")

    draw_button(draw, 610, 530, 480, 50, "Guardar cambios y Reiniciar consola", f_bold, bg="#107C10", fg="#FFFFFF")

    img.save(os.path.join(ASSETS_DIR, "img14_app_type_game.png"))
    print("Generated img14_app_type_game.png")

# ==========================================================
# IMAGEN 15: CONTROLADOR DE VÍDEO D3D11 EN RETROARCH
# ==========================================================
def gen_img_video_driver():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 2: AJUSTAR EL CONTROLADOR DE VÍDEO A 'D3D11'", "RetroArch ➔ Ajustes ➔ Controladores ➔ Vídeo: d3d11 (Evita crash de GLideN64)")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # RetroArch UI mockup
    draw.rectangle([(50, 110), (1150, 630)], fill="#15171C")
    
    # Path Bar
    draw.rectangle([(50, 110), (1150, 160)], fill="#1E222B")
    draw.text((70, 125), "Ruta: Menú principal ➔ Ajustes ➔ Controladores (Drivers) ➔ Vídeo", font=f_bold, fill="#61AFEF")
    
    # Left column: Menu list
    draw_card(draw, 70, 180, 520, 420, "CONTROLADORES DE RETROARCH", bg="#1A1C23", border="#333842")
    
    drivers = [
        ("Vídeo (Video)", "d3d11  (RECOMENDADO N64 / UWP)", True),
        ("Audio", "xaudio  (Predeterminado Xbox)", False),
        ("Entrada (Input)", "xinput  (Mando de Xbox)", False),
        ("Controlador de menú", "ozone", False),
        ("Cámara / Ubicación", "null", False)
    ]
    dy = 230
    for dname, dval, is_sel in drivers:
        bg_col = "#153018" if is_sel else "#21252E"
        bd_col = "#107C10" if is_sel else "#2F3542"
        w_bd = 2 if is_sel else 1
        draw.rounded_rectangle([(90, dy), (570, dy + 55)], radius=6, fill=bg_col, outline=bd_col, width=w_bd)
        draw.text((105, dy + 10), dname, font=f_bold, fill="#FFFFFF")
        draw.text((105, dy + 32), dval, font=f_small, fill="#00FF66" if is_sel else "#8892B0")
        dy += 65

    # Right column: Driver comparison explanation
    draw_card(draw, 620, 180, 510, 420, "COMPATIBILIDAD CON NINTENDO 64", bg="#1A1C23", border="#333842")
    
    draw.rounded_rectangle([(640, 230), (1100, 305)], radius=6, fill="#122515", outline="#107C10", width=1)
    draw.text((655, 240), "✓ d3d11 (Direct3D 11) - ESTABLE Y COMPATIBLE", font=f_bold, fill="#98C379")
    draw.text((655, 265), "Permite que el plugin gráfico GLideN64 de Mupen64Plus\nfuncione correctamente a través de la capa ANGLE de Xbox.", font=ImageFont.truetype(FONT_REG, 11), fill="#CCCCCC")
    
    draw.rounded_rectangle([(640, 320), (1100, 395)], radius=6, fill="#2A1515", outline="#D9381E", width=1)
    draw.text((655, 330), "✗ d3d12 (Direct3D 12) - INCOMPATIBLE CON N64", font=f_bold, fill="#FFAAAA")
    draw.text((655, 355), "El plugin GLideN64 no soporta D3D12 nativo en Xbox UWP.\nProvoca cierre forzado ('Error en el contenido').", font=ImageFont.truetype(FONT_REG, 11), fill="#DD8888")

    draw.rounded_rectangle([(640, 410), (1100, 485)], radius=6, fill="#2A1515", outline="#D9381E", width=1)
    draw.text((655, 420), "✗ vulkan / gl - NO DISPONIBLE NATIVAMENTE", font=f_bold, fill="#FFAAAA")
    draw.text((655, 445), "Xbox carece de drivers Vulkan y OpenGL puros.\nParaLLEl N64 colapsa si intenta usar Vulkan.", font=ImageFont.truetype(FONT_REG, 11), fill="#DD8888")

    # Bottom tip
    draw.rectangle([(640, 505), (1100, 580)], fill="#211E16", outline="#E5C07B", width=1)
    draw.text((655, 515), "⚠️ GUARDAR CONFIGURACIÓN TRAS CAMBIAR:", font=f_bold, fill="#E5C07B")
    draw.text((655, 540), "Menú principal ➔ Archivo de configuración ➔ Guardar configuración actual,\ny luego reinicia RetroArch para que el cambio tome efecto.", font=ImageFont.truetype(FONT_REG, 11), fill="#FFFFFF")

    img.save(os.path.join(ASSETS_DIR, "img15_retroarch_video_driver.png"))
    print("Generated img15_retroarch_video_driver.png")

# ==========================================================
# IMAGEN 16: CONFIGURACIÓN NÚCLEO N64 Y GESTIÓN DE ROMS
# ==========================================================
def gen_img_n64_core_and_roms():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 3: CONFIGURACIÓN DEL NÚCLEO Y FORMATO DE ROMS", "Reglas clave para Mupen64Plus-Next, ParaLLEl N64 y descompresión de juegos")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Left Card: Core selection and plugins
    draw_card(draw, 60, 120, 520, 500, "1. NÚCLEO RECOMENDADO Y PLUGINS GRÁFICOS", bg="#191B22", border="#303542")
    
    # Recommendation Banner
    draw.rounded_rectangle([(80, 165), (560, 235)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((95, 175), "★ UTILIZA: Mupen64Plus-Next (Recomendado)", font=f_bold, fill="#00FF66")
    draw.text((95, 202), "Es el núcleo más optimizado y estable en Xbox One y Series.\nEvita ParaLLEl N64 salvo que uses render por CPU (Angrylion).", font=ImageFont.truetype(FONT_REG, 11), fill="#D0E8FF")

    draw.text((80, 255), "Opciones del núcleo (Menú rápido ➔ Opciones):", font=f_bold, fill="#FFFFFF")
    
    opts = [
        ("Plugin gráfico (RDP):", "GLideN64  (Rendimiento fluido)", "#00FF66"),
        ("Plugin de audio/RSP:", "HLE  (Emulación de alto nivel)", "#00FF66"),
        ("Resolución 4:3 / 16:9:", "Original (o 2x en Xbox Series)", "#FFFFFF"),
        ("ParaLLEl N64 (Si se usa):", "RDP: angrylion | RSP: cxd4 / hle", "#E5C07B")
    ]
    oy = 285
    for opt_name, opt_val, val_col in opts:
        draw.rounded_rectangle([(80, oy), (560, oy + 45)], radius=5, fill="#222530")
        draw.text((95, oy + 12), opt_name, font=f_small, fill="#AAAAAA")
        draw.text((275, oy + 12), opt_val, font=f_small, fill=val_col)
        oy += 52

    draw.rectangle([(80, 495), (560, 600)], fill="#211E16", outline="#E5C07B", width=1)
    draw.text((95, 505), "ARCHIVO .OPT SALVAVIDAS:", font=f_bold, fill="#E5C07B")
    draw.text((95, 530), "Si el núcleo crashea antes de abrir el Menú Rápido,\ncrea un archivo de texto en tu pendrive:\nE:\\RetroArch\\config\\Mupen64Plus-Next\\mupen64plus-next.opt\ncon: mupen64plus-rdp-plugin = 'GLideN64'", font=ImageFont.truetype(FONT_REG, 10), fill="#E0E0E0")

    # Right Card: ROM Formats and USB Permissions
    draw_card(draw, 620, 120, 520, 500, "2. FORMATO DE LAS ROMS Y UNIDAD USB E:\\", bg="#191B22", border="#303542")
    
    # Formats
    draw.text((645, 165), "Formato de las ROMs (Extensión):", font=f_bold, fill="#FFFFFF")
    
    draw.rounded_rectangle([(645, 195), (1115, 260)], radius=6, fill="#122515", outline="#107C10", width=1)
    draw.text((660, 205), "✓ EXTENSIONES VÁLIDAS: .z64 / .n64 / .v64", font=f_bold, fill="#98C379")
    draw.text((660, 230), "Las ROMs deben estar DESCOMPRIMIDAS para garantizar carga directa.", font=ImageFont.truetype(FONT_REG, 11), fill="#CCCCCC")
    
    draw.rounded_rectangle([(645, 275), (1115, 340)], radius=6, fill="#281515", outline="#D9381E", width=1)
    draw.text((660, 285), "✗ EVITAR: Archivos .zip y .7z", font=f_bold, fill="#FFAAAA")
    draw.text((660, 310), "Descomprimir 16-64 MB de ROM en la RAM limitada de UWP suele\nagotar el búfer temporal y lanzar 'Error en el contenido'.", font=ImageFont.truetype(FONT_REG, 11), fill="#DD8888")

    # USB Permissions checklist
    draw.text((645, 360), "Permisos del Pendrive (Unidad E:\\):", font=f_bold, fill="#FFFFFF")
    draw.rounded_rectangle([(645, 390), (1115, 480)], radius=6, fill="#16222F", outline="#0080FF", width=1)
    draw.text((660, 400), "✓ Permiso UWP: 'ALL APPLICATION PACKAGES'", font=f_bold, fill="#61AFEF")
    draw.text((660, 425), "• Sistema de archivos obligatorio: NTFS.\n• Permiso 'Control Total' otorgado en Windows.\n• Permite a RetroArch escribir partidas .srm y estados .state.", font=ImageFont.truetype(FONT_REG, 11), fill="#E0E0E0")

    draw.rounded_rectangle([(645, 500), (1115, 600)], radius=6, fill="#20242E", outline="#3F4656")
    draw.text((660, 510), "RESUMEN DE SOLUCIÓN RÁPIDA:", font=f_bold, fill="#00FF66")
    draw.text((660, 535), "1. Dev Home ➔ App Type = 'Game' ➔ Reiniciar Xbox.\n2. RetroArch ➔ Vídeo = 'd3d11'.\n3. Usar núcleo Mupen64Plus-Next con ROM .z64 sin comprimir.", font=ImageFont.truetype(FONT_REG, 11), fill="#FFFFFF")

    img.save(os.path.join(ASSETS_DIR, "img16_n64_core_and_roms.png"))
    print("Generated img16_n64_core_and_roms.png")

if __name__ == "__main__":
    gen_img_n64_error()
    gen_img_app_type_game()
    gen_img_video_driver()
    gen_img_n64_core_and_roms()
    print("All N64 images generated successfully!")
