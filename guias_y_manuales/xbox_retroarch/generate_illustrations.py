#!/usr/bin/env python3
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
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(30, 20, 16, 13)
    # Header bar
    draw.rectangle([(0, 0), (w, 85)], fill="#0D0D0D")
    draw.rectangle([(0, 85), (w, 88)], fill="#107C10") # Xbox green line
    
    # Xbox logo sphere icon mockup
    draw.ellipse([(35, 20), (85, 70)], fill="#107C10")
    draw.ellipse([(43, 28), (77, 62)], fill="#1E1E1E")
    # Stylized X
    draw.line([(48, 33), (72, 57)], fill="#FFFFFF", width=4)
    draw.line([(72, 33), (48, 57)], fill="#FFFFFF", width=4)
    
    draw.text((105, 22), title, font=f_title, fill="#FFFFFF")
    draw.text((105, 56), subtitle, font=f_small, fill="#9E9E9E")

def draw_button(draw, x, y, w, h, text, font, bg="#107C10", fg="#FFFFFF", border=None, icon=None):
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
# IMAGEN 1: DIAGRAMA DE FLUJO RETAIL <--> DEVELOPER MODE
# ==========================================================
def gen_img1():
    img = Image.new("RGB", (1200, 675), "#141414")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "ARQUITECTURA Y CICLO DE MODOS EN XBOX", "Transición bidireccional entre Modo Retail y Modo Desarrollador")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    # Left Card: Retail Mode
    draw_card(draw, 50, 120, 480, 420, "1. MODO RETAIL (NORMAL / COMERCIAL)", bg="#1A1A1A", border="#0080FF")
    draw.rectangle([(50, 120), (530, 124)], fill="#0080FF")
    
    retail_lines = [
        "• Entorno oficial estándar de Microsoft Xbox.",
        "• Compatible con juegos de disco, digitales y Game Pass.",
        "• Acceso a Xbox Network, multijugador y logros oficiales.",
        "• Seguridad total: No permite código no firmado / sideload.",
        "• Descarga de la app 'Xbox Dev Mode' desde la Store.",
        "",
        "Para pasar a Modo Dev:",
        "1. Abrir app 'Xbox Dev Mode'.",
        "2. Pulsar botón 'Switch and restart'.",
        "3. La consola se reinicia en Modo Desarrollador."
    ]
    y_off = 170
    for line in retail_lines:
        font_to_use = f_bold if line.startswith("Para pasar") or line.startswith("• Entorno") else f_text
        color = "#FFFFFF" if not line.startswith("•") else "#D0D0D0"
        if line.startswith("Para pasar"): color = "#56B6C2"
        draw.text((75, y_off), line, font=font_to_use, fill=color)
        y_off += 24

    # Right Card: Developer Mode
    draw_card(draw, 670, 120, 480, 420, "2. MODO DESARROLLADOR (DEV MODE)", bg="#1A1A1A", border="#107C10")
    draw.rectangle([(670, 120), (1150, 124)], fill="#107C10")
    
    dev_lines = [
        "• Entorno aislado de desarrollo (Sandbox UWP).",
        "• Dashboard dedicado: 'Dev Home'.",
        "• Instalación de apps propias, emuladores y herramientas.",
        "• Acceso remoto por PC vía Xbox Device Portal (puerto 11443).",
        "• Los juegos de disco/retail NO se ejecutan aquí.",
        "",
        "Para volver a Modo Retail:",
        "1. En 'Dev Home', pulsar 'Leave Dev Mode'.",
        "2. DESMARCAR 'Delete sideloaded games and apps'.",
        "3. Pulsar 'Restart now'. Consola vuelve a Retail."
    ]
    y_off = 170
    for line in dev_lines:
        font_to_use = f_bold if line.startswith("Para volver") or line.startswith("• Entorno") else f_text
        color = "#FFFFFF" if not line.startswith("•") else "#D0D0D0"
        if line.startswith("Para volver"): color = "#98C379"
        if "DESMARCAR" in line: color = "#E06C75"
        draw.text((695, y_off), line, font=font_to_use, fill=color)
        y_off += 24

    # Central Transition arrows
    # Right arrow (Retail -> Dev)
    draw.polygon([(545, 250), (635, 250), (635, 240), (655, 255), (635, 270), (635, 260), (545, 260)], fill="#107C10")
    draw.text((550, 222), "Switch & restart", font=f_small, fill="#98C379")
    
    # Left arrow (Dev -> Retail)
    draw.polygon([(655, 360), (565, 360), (565, 350), (545, 365), (565, 380), (565, 370), (655, 370)], fill="#0080FF")
    draw.text((558, 388), "Leave Dev Mode", font=f_small, fill="#61AFEF")

    # Bottom notice banner
    draw_card(draw, 50, 560, 1100, 85, "", bg="#211E16", border="#D19A66")
    draw.rectangle([(50, 560), (1150, 563)], fill="#E5C07B")
    draw.text((75, 575), "NOTA DE SEGURIDAD Y GARANTÍA:", font=f_bold, fill="#E5C07B")
    draw.text((75, 603), "El cambio de modos no formatea la consola ni anula la garantía de Microsoft. Ambas particiones están aisladas por hardware.", font=f_text, fill="#E0E0E0")

    img.save(os.path.join(ASSETS_DIR, "img1_flujo_modos.png"))
    print("Generated img1_flujo_modos.png")

# ==========================================================
# IMAGEN 2: REGISTRO MICROSOFT PARTNER CENTER (WEB)
# ==========================================================
def gen_img2():
    img = Image.new("RGB", (1200, 675), "#181818")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 1: ACTIVACIÓN EN MICROSOFT PARTNER CENTER", "Vinculación de la consola en partner.microsoft.com/xboxconfig/devices")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Browser window mockup
    draw.rounded_rectangle([(50, 110), (1150, 630)], radius=10, fill="#242424", outline="#383838", width=1)
    # Browser bar
    draw.rectangle([(50, 110), (1150, 155)], fill="#1E1E1E")
    # Window circles
    draw.ellipse([(65, 127), (77, 139)], fill="#ED6A5E")
    draw.ellipse([(85, 127), (97, 139)], fill="#F4BF4F")
    draw.ellipse([(105, 127), (117, 139)], fill="#61C554")
    # Address bar
    draw.rounded_rectangle([(140, 120), (1000, 147)], radius=5, fill="#121212", outline="#3A3A3A", width=1)
    draw.text((155, 126), "https://partner.microsoft.com/xboxconfig/devices (o aka.ms/activatexbox)", font=f_small, fill="#9CDCFE")
    
    # Page Content
    draw.text((80, 180), "Microsoft Developer | Partner Center - Xbox Consoles", font=f_title, fill="#FFFFFF")
    draw.text((80, 215), "Administrar y activar consolas de prueba y desarrollo", font=f_small, fill="#888888")
    
    # Form box
    draw_card(draw, 80, 250, 600, 240, "", bg="#1C1C1C", border="#333333")
    draw.text((105, 275), "Introducir código de activación de la consola", font=f_bold, fill="#FFFFFF")
    draw.text((105, 305), "Abre la app 'Xbox Dev Mode' en tu consola para obtener el código de 6 caracteres:", font=f_text, fill="#CCCCCC")
    
    # Input field
    draw.rounded_rectangle([(105, 340), (450, 390)], radius=6, fill="#0E0E0E", outline="#107C10", width=2)
    draw.text((130, 350), "X7K2 - 9B4F", font=ImageFont.truetype(FONT_BOLD, 22), fill="#00FF66")
    
    # Submit button
    draw_button(draw, 105, 415, 240, 48, "Agree and activate", f_bold, bg="#107C10", fg="#FFFFFF")
    draw.text((360, 430), "Términos del programa aceptados", font=f_small, fill="#777777")
    
    # Right column info: Registered devices list
    draw_card(draw, 710, 250, 410, 240, "CONSOLAS VINCULADAS (Límite: 3)", bg="#1C1C1C", border="#333333")
    draw.rectangle([(730, 310), (1095, 370)], fill="#282828")
    draw.text((745, 320), "Xbox Series X (Salón)", font=f_bold, fill="#FFFFFF")
    draw.text((745, 345), "ID: 1048-5928-8472 | Estado: ACTIVA", font=f_small, fill="#98C379")
    
    draw.rectangle([(730, 385), (1095, 445)], fill="#222222")
    draw.text((745, 395), "Xbox One X (Estudio)", font=f_bold, fill="#FFFFFF")
    draw.text((745, 420), "ID: 9021-3819-1102 | Estado: ACTIVA", font=f_small, fill="#98C379")

    # Bottom notice
    draw.rectangle([(80, 520), (1120, 595)], fill="#172535", outline="#204A87", width=1)
    draw.text((105, 535), "IMPORTANTE:", font=f_bold, fill="#61AFEF")
    draw.text((105, 560), "Se requiere una cuenta de desarrollador de Microsoft Partner Center (coste único aproximado de 14-19 €/$, pago único de por vida).", font=f_text, fill="#E0E0E0")

    img.save(os.path.join(ASSETS_DIR, "img2_partner_center.png"))
    print("Generated img2_partner_center.png")

# ==========================================================
# IMAGEN 3: INSTALACIÓN DESDE MICROSOFT STORE EN XBOX
# ==========================================================
def gen_img3():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 2: DESCARGAR 'XBOX DEV MODE' EN LA STORE", "Localizar e instalar la aplicación oficial gratuita en Modo Retail")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    # Xbox Store Interface Mockup
    # Search Bar
    draw.rounded_rectangle([(60, 110), (700, 155)], radius=6, fill="#252525", outline="#3E3E3E", width=1)
    draw.text((80, 122), "Buscar: Xbox Dev Mode", font=f_text, fill="#FFFFFF")
    draw.text((630, 122), "🔍", font=f_text, fill="#888888")
    
    # Store App Card Details
    draw_card(draw, 60, 180, 1080, 440, "", bg="#1C1C1C", border="#333333")
    
    # App Icon Box
    draw.rounded_rectangle([(100, 220), (280, 400)], radius=12, fill="#107C10")
    # Icon inner graphic
    draw.ellipse([(140, 260), (240, 360)], fill="#0E0E0E")
    draw.text((165, 290), "</>", font=ImageFont.truetype(FONT_BOLD, 36), fill="#107C10")
    draw.text((120, 370), "DEV MODE", font=f_small, fill="#FFFFFF")
    
    # App Info
    draw.text((320, 220), "Xbox Dev Mode", font=ImageFont.truetype(FONT_BOLD, 32), fill="#FFFFFF")
    draw.text((320, 265), "Microsoft Corporation  •  Herramientas de desarrollo  •  Gratis", font=f_text, fill="#9E9E9E")
    draw.text((320, 295), "Calificación: 4.8 ★★★★★ | PEGI 3 | Tamaño: ~45 MB", font=f_small, fill="#707070")
    
    # Description
    desc = (
        "La aplicación Xbox Dev Mode permite activar las funciones de desarrollo en tu consola comercial,\n"
        "habilitando la ejecución de aplicaciones UWP, herramientas de depuración y pruebas de software.\n"
        "Requiere una cuenta válida en Microsoft Partner Center para su registro inicial."
    )
    draw.text((320, 335), desc, font=f_text, fill="#CCCCCC")
    
    # Install Button (Selected/Focused)
    draw.rounded_rectangle([(320, 430), (520, 490)], radius=8, fill="#107C10", outline="#5CD65C", width=2)
    draw.text((365, 447), "Obtener / Instalar", font=f_bold, fill="#FFFFFF")
    
    # Controller prompt (A)
    draw.ellipse([(335, 447), (355, 467)], fill="#008000")
    draw.text((340, 449), "A", font=ImageFont.truetype(FONT_BOLD, 12), fill="#FFFFFF")
    
    # Status indicator
    draw_card(draw, 550, 430, 550, 60, "", bg="#152615", border="#2B5B2B")
    draw.text((570, 448), "✓ Aplicación oficial de Microsoft para todas las consolas Xbox One / Series", font=f_small, fill="#98C379")

    # Footer tip
    draw.text((100, 570), "CONSEJO: Esta aplicación permanecerá instalada tanto en Retail como en Dev Mode para cambiar entre ambos.", font=f_small, fill="#888888")

    img.save(os.path.join(ASSETS_DIR, "img3_xbox_store_search.png"))
    print("Generated img3_xbox_store_search.png")

# ==========================================================
# IMAGEN 4: PANTALLA DE CÓDIGO DE EMPAREJAMIENTO
# ==========================================================
def gen_img4():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 3: OBTENCIÓN DEL CÓDIGO DE ACTIVACIÓN", "Pantalla de vinculación mostrada en la app 'Xbox Dev Mode'")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 16, 13)
    
    # Main container
    draw_card(draw, 100, 120, 1000, 500, "", bg="#181818", border="#2E2E2E")
    
    draw.text((150, 160), "Activar el Modo Desarrollador en esta consola", font=ImageFont.truetype(FONT_BOLD, 28), fill="#FFFFFF")
    draw.text((150, 210), "Sigue estos sencillos pasos desde tu PC o teléfono móvil:", font=f_text, fill="#CCCCCC")
    
    draw.text((180, 250), "1. Abre un navegador e ingresa a:  aka.ms/activatexbox", font=f_bold, fill="#61AFEF")
    draw.text((180, 285), "2. Inicia sesión con tu cuenta de Microsoft Partner Center.", font=f_text, fill="#E0E0E0")
    draw.text((180, 320), "3. Introduce el siguiente código de activación de 6 caracteres:", font=f_text, fill="#E0E0E0")
    
    # Big Code Display Box
    draw.rounded_rectangle([(350, 370), (750, 460)], radius=12, fill="#080808", outline="#107C10", width=3)
    draw.text((410, 385), "X 7 K 2 - 9 B", font=ImageFont.truetype(FONT_BOLD, 44), fill="#00FF66")
    
    draw.text((280, 480), "Esperando confirmación desde el portal web de Microsoft...", font=f_small, fill="#E5C07B")
    
    # Buttons
    draw_button(draw, 150, 540, 160, 45, "Cancelar", f_text, bg="#2D2D2D", fg="#CCCCCC")
    draw_button(draw, 850, 540, 200, 45, "Siguiente >", f_bold, bg="#107C10", fg="#FFFFFF")

    img.save(os.path.join(ASSETS_DIR, "img4_dev_mode_activation_code.png"))
    print("Generated img4_dev_mode_activation_code.png")

# ==========================================================
# IMAGEN 5: PANTALLA "SWITCH AND RESTART" (RETAIL -> DEV)
# ==========================================================
def gen_img5():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 4: CAMBIAR Y REINICIAR (RETAIL -> DEV)", "Iniciar la transición al Modo Desarrollador desde la app 'Xbox Dev Mode'")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 16, 13)
    
    draw_card(draw, 100, 120, 1000, 500, "", bg="#181818", border="#2E2E2E")
    
    # Success badge
    draw.ellipse([(150, 160), (200, 210)], fill="#107C10")
    draw.text((168, 168), "✓", font=ImageFont.truetype(FONT_BOLD, 28), fill="#FFFFFF")
    
    draw.text((220, 165), "Consola activada correctamente", font=ImageFont.truetype(FONT_BOLD, 26), fill="#FFFFFF")
    draw.text((220, 202), "Tu dispositivo está vinculado a tu cuenta de desarrollador de Microsoft.", font=f_text, fill="#98C379")
    
    # Explanation
    info_p = (
        "Para ingresar al Modo Desarrollador, la consola debe reiniciarse.\n"
        "Durante el primer arranque en Dev Mode, el sistema configurará el espacio aislado (Sandbox),\n"
        "lo cual puede tomar entre 2 y 5 minutos. No apagues la consola durante este proceso."
    )
    draw.text((150, 260), info_p, font=f_text, fill="#D0D0D0")
    
    # Central Highlighted Action: SWITCH AND RESTART Button
    draw.rounded_rectangle([(320, 360), (780, 450)], radius=12, fill="#107C10", outline="#66FF66", width=3)
    draw.text((380, 385), "Switch and restart", font=ImageFont.truetype(FONT_BOLD, 34), fill="#FFFFFF")
    draw.text((430, 425), "(Cambiar y reiniciar)", font=f_small, fill="#E0FFE0")
    
    # Subtext prompt
    draw.text((340, 480), "Presiona [A] en tu mando para confirmar el reinicio", font=f_bold, fill="#FFFFFF")
    draw.ellipse([(310, 478), (330, 498)], fill="#008000")
    draw.text((315, 480), "A", font=ImageFont.truetype(FONT_BOLD, 12), fill="#FFFFFF")

    # Warning note
    draw_card(draw, 150, 530, 900, 60, "", bg="#241B12", border="#E5C07B")
    draw.text((170, 548), "💡 En el futuro, siempre que estés en Retail y quieras ir a Dev Mode, solo abre esta app y pulsa este botón.", font=f_small, fill="#E5C07B")

    img.save(os.path.join(ASSETS_DIR, "img5_switch_and_restart.png"))
    print("Generated img5_switch_and_restart.png")

# ==========================================================
# IMAGEN 6: DEV HOME DASHBOARD (INTERFAZ DE DESARROLLO)
# ==========================================================
def gen_img6():
    img = Image.new("RGB", (1200, 675), "#0E0E0E")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 5: DASHBOARD 'DEV HOME' EN MODO DESARROLLADOR", "Panel de control principal del entorno de desarrollo de Xbox")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Top Status Bar in Dev Home
    draw.rectangle([(50, 110), (1150, 160)], fill="#1A1A1A", outline="#303030", width=1)
    draw.text((70, 125), "🟢 MODO: DEVELOPER (ACTIVO)", font=f_bold, fill="#98C379")
    draw.text((380, 125), "IP LAN: 192.168.1.85", font=f_bold, fill="#61AFEF")
    draw.text((630, 125), "Xbox Device Portal: https://192.168.1.85:11443", font=f_text, fill="#E5C07B")
    draw.text((1030, 125), "Espacio: 28.5 GB", font=f_small, fill="#888888")
    
    # Left Column: Quick Actions
    draw_card(draw, 50, 180, 400, 440, "QUICK ACTIONS (ACCIONES RÁPIDAS)", bg="#161616", border="#2A2A2A")
    
    # Highlighted "Leave Dev Mode" Tile!
    draw.rounded_rectangle([(70, 225), (430, 310)], radius=8, fill="#0F3860", outline="#61AFEF", width=2)
    draw.text((95, 240), "➡ Leave Dev Mode", font=ImageFont.truetype(FONT_BOLD, 20), fill="#FFFFFF")
    draw.text((95, 275), "Salir y reiniciar en Modo Retail", font=f_small, fill="#D0E8FF")
    
    # Other actions
    draw_button(draw, 70, 325, 360, 50, "Restart console", f_text, bg="#262626", fg="#FFFFFF", border="#3A3A3A")
    draw_button(draw, 70, 385, 360, 50, "Xbox Device Portal settings", f_text, bg="#262626", fg="#FFFFFF", border="#3A3A3A")
    draw_button(draw, 70, 445, 360, 50, "Launch Dev Home settings", f_text, bg="#262626", fg="#FFFFFF", border="#3A3A3A")
    draw_button(draw, 70, 505, 360, 50, "Manage test accounts", f_text, bg="#262626", fg="#FFFFFF", border="#3A3A3A")
    draw_button(draw, 70, 565, 360, 40, "File Explorer & Storage", f_small, bg="#1E1E1E", fg="#888888")

    # Center/Right Area: Games & Apps installed in Dev Mode
    draw_card(draw, 470, 180, 680, 440, "DEVELOPMENT GAMES & APPS (SIDELOADED)", bg="#161616", border="#2A2A2A")
    
    # Grid of sideloaded apps
    apps = [
        ("RetroArch UWP", "Emulador Multi-sistema", "#7B1FA2"),
        ("Kodi Xbox", "Centro Multimedia", "#0288D1"),
        ("Dev File Explorer", "Explorador de Archivos", "#388E3C"),
        ("FTP Server UWP", "Servidor FTP Local", "#F57C00"),
        ("PPSSPP", "Emulador PSP", "#0097A7"),
        ("DuckStation", "Emulador PS1", "#C2185B")
    ]
    for idx, (aname, adesc, acol) in enumerate(apps):
        row = idx // 2
        col = idx % 2
        ax = 495 + col * 325
        ay = 230 + row * 125
        draw.rounded_rectangle([(ax, ay), (ax + 310, ay + 110)], radius=8, fill="#222222", outline="#353535", width=1)
        draw.rectangle([(ax, ay), (ax + 8, ay + 110)], fill=acol)
        draw.text((ax + 20, ay + 20), aname, font=f_bold, fill="#FFFFFF")
        draw.text((ax + 20, ay + 50), adesc, font=f_small, fill="#AAAAAA")
        draw.text((ax + 20, ay + 80), "Versión UWP | Sideloaded", font=ImageFont.truetype(FONT_REG, 10), fill="#777777")

    img.save(os.path.join(ASSETS_DIR, "img6_dev_home_dashboard.png"))
    print("Generated img6_dev_home_dashboard.png")

# ==========================================================
# IMAGEN 7: DIÁLOGO CRÍTICO "LEAVE DEV MODE" (DEV -> RETAIL)
# ==========================================================
def gen_img7():
    img = Image.new("RGB", (1200, 675), "#0A0A0A")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 6: SALIR DE DEV MODE A RETAIL (¡PASO CRÍTICO!)", "Ventana de confirmación y preservación de juegos y aplicaciones")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 16, 13)
    
    # Dimmed background representation
    draw.rectangle([(50, 110), (1150, 630)], fill="#141414")
    
    # Modal Dialog Box (Centered)
    draw.rounded_rectangle([(180, 140), (1020, 590)], radius=12, fill="#1E1E1E", outline="#404040", width=2)
    
    # Dialog Title
    draw.text((220, 175), "¿Salir del Modo Desarrollador?", font=ImageFont.truetype(FONT_BOLD, 26), fill="#FFFFFF")
    draw.text((220, 215), "Al reiniciar, la consola volverá al Modo Retail estándar para jugar con normalidad.", font=f_text, fill="#CCCCCC")
    
    # CRITICAL WARNING BOX - THE CHECKBOX!
    draw_card(draw, 220, 260, 760, 190, "", bg="#2A1414", border="#E06C75", radius=10)
    draw.rectangle([(220, 260), (980, 266)], fill="#E06C75")
    
    # Checkbox graphic (UNCHECKED - SAFE STATE)
    draw.rounded_rectangle([(250, 290), (285, 325)], radius=4, fill="#121212", outline="#E06C75", width=2)
    # Highlight that it MUST BE EMPTY
    draw.text((305, 293), "Delete sideloaded games and apps", font=ImageFont.truetype(FONT_BOLD, 20), fill="#FFFFFF")
    draw.text((305, 325), "(Eliminar juegos y aplicaciones transferidas)", font=f_small, fill="#E06C75")
    
    # Big warning explanation
    warning_text = (
        "⚠️ ¡ATENCIÓN MUY IMPORTANTE!\n"
        "• DEJA ESTA CASILLA DESMARCADA (VACÍA) para conservar tus emuladores, ROMs y datos.\n"
        "• Si la marcas, borrarás todas las aplicaciones instaladas en Dev Mode.\n"
        "• Al dejarla vacía, todo seguirá ahí esperándote cuando regreses a Dev Mode."
    )
    draw.text((250, 360), warning_text, font=f_small, fill="#FFCCCC")
    
    # Buttons
    # "Restart now" focused
    draw.rounded_rectangle([(220, 485), (480, 545)], radius=8, fill="#107C10", outline="#5CD65C", width=2)
    draw.text((280, 502), "Restart now", font=f_bold, fill="#FFFFFF")
    draw.text((260, 525), "(Reiniciar ahora a Retail)", font=ImageFont.truetype(FONT_REG, 11), fill="#E0FFE0")
    
    # Controller prompt (A)
    draw.ellipse([(240, 505), (265, 530)], fill="#008000")
    draw.text((248, 508), "A", font=ImageFont.truetype(FONT_BOLD, 14), fill="#FFFFFF")
    
    # Cancel button
    draw_button(draw, 520, 485, 200, 60, "Cancel", f_text, bg="#2E2E2E", fg="#CCCCCC")

    img.save(os.path.join(ASSETS_DIR, "img7_leave_dev_mode_dialog.png"))
    print("Generated img7_leave_dev_mode_dialog.png")

# ==========================================================
# IMAGEN 8: VUELTA A MODO RETAIL (DASHBOARD HABITUAL)
# ==========================================================
def gen_img8():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PASO 7: RETORNO AL MODO RETAIL (JUEGOS ESTÁNDAR)", "La consola vuelve a su estado comercial con tus juegos de catálogo habituales")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    # Xbox Retail Dashboard Mockup
    # Top tab navigation
    tabs = ["Inicio", "Game Pass", "Store", "Comunidad", "Configuración"]
    tx = 60
    for tab in tabs:
        col = "#107C10" if tab == "Inicio" else "#888888"
        draw.text((tx, 115), tab, font=f_bold if tab == "Inicio" else f_text, fill=col)
        tx += 130
        
    # Big Main tile: Recent retail game (e.g. Forza Horizon 5 / Halo Infinite)
    draw_card(draw, 60, 160, 640, 360, "", bg="#1C1C1C", border="#333333")
    draw.rectangle([(60, 160), (700, 380)], fill="#202A35")
    draw.text((90, 200), "FORZA HORIZON 5", font=ImageFont.truetype(FONT_BOLD, 36), fill="#FFFFFF")
    draw.text((90, 250), "Listo para jugar con Xbox Network y Logros activos", font=f_text, fill="#A0C8FF")
    draw_button(draw, 90, 300, 200, 45, "Iniciar juego ▶", f_bold, bg="#107C10", fg="#FFFFFF")
    
    draw.text((90, 440), "Estado de la consola: Modo Retail (Comercial) 100% operativo.", font=f_text, fill="#FFFFFF")
    draw.text((90, 475), "Acceso a servidores multijugador, descargas de la Store y partidas en la nube.", font=f_small, fill="#999999")

    # Right column: My Games and Apps, with Xbox Dev Mode ready!
    draw_card(draw, 730, 160, 410, 360, "BIBLIOTECA RÁPIDA", bg="#181818", border="#303030")
    
    # Dev mode tile in library
    draw.rounded_rectangle([(755, 215), (1115, 305)], radius=8, fill="#122B15", outline="#107C10", width=2)
    draw.text((780, 230), "Xbox Dev Mode", font=f_bold, fill="#98C379")
    draw.text((780, 260), "App lista para volver a Modo Dev cuando quieras", font=f_small, fill="#CCCCCC")
    draw.text((780, 280), "Pulsar [A] -> 'Switch and restart'", font=ImageFont.truetype(FONT_BOLD, 11), fill="#00FF66")

    # Other retail apps
    draw.rounded_rectangle([(755, 320), (1115, 390)], radius=8, fill="#222222", outline="#333333", width=1)
    draw.text((780, 335), "Xbox Game Pass", font=f_bold, fill="#FFFFFF")
    draw.text((780, 360), "Biblioteca de suscripción", font=f_small, fill="#888888")

    draw.rounded_rectangle([(755, 405), (1115, 475)], radius=8, fill="#222222", outline="#333333", width=1)
    draw.text((780, 420), "Mis juegos y aplicaciones", font=f_bold, fill="#FFFFFF")
    draw.text((780, 445), "Ver todos los juegos instalados", font=f_small, fill="#888888")

    # Bottom summary bar
    draw_card(draw, 60, 545, 1080, 80, "", bg="#16222F", border="#0080FF")
    draw.text((85, 560), "RESUMEN DEL PROCESO BIDIRECCIONAL:", font=f_bold, fill="#61AFEF")
    draw.text((85, 588), "Retail ➡ Dev: Abrir 'Xbox Dev Mode' y pulsar 'Switch and restart' | Dev ➡ Retail: En Dev Home pulsar 'Leave Dev Mode' y reiniciar.", font=f_text, fill="#FFFFFF")

    img.save(os.path.join(ASSETS_DIR, "img8_regreso_retail.png"))
    print("Generated img8_regreso_retail.png")

if __name__ == "__main__":
    gen_img1()
    gen_img2()
    gen_img3()
    gen_img4()
    gen_img5()
    gen_img6()
    gen_img7()
    gen_img8()
    print("All 8 images generated successfully!")
