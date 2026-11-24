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
    draw.rectangle([(0, 0), (w, 85)], fill="#0D0D0D")
    draw.rectangle([(0, 85), (w, 88)], fill="#D9381E")
    
    draw.ellipse([(35, 20), (85, 70)], fill="#D9381E")
    draw.ellipse([(43, 28), (77, 62)], fill="#1E1E1E")
    draw.line([(48, 33), (72, 57)], fill="#FFFFFF", width=4)
    draw.line([(72, 33), (48, 57)], fill="#FFFFFF", width=4)
    
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

def gen_img_error_screen():
    img = Image.new("RGB", (1200, 675), "#0D0D0D")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "DIAGNÓSTICO: ERROR DE INICIO 0x8027025a", "Tiempo de espera agotado al abrir Xbox Dev Mode o aplicaciones")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(24, 18, 15, 12)
    
    draw.rectangle([(50, 110), (1150, 630)], fill="#161616")
    draw.rounded_rectangle([(160, 140), (1040, 580)], radius=12, fill="#1F1F1F", outline="#444444", width=2)
    
    draw.ellipse([(200, 175), (250, 225)], fill="#D9381E")
    draw.text((220, 182), "!", font=ImageFont.truetype(FONT_BOLD, 32), fill="#FFFFFF")
    
    draw.text((270, 180), "Vuelve a intentarlo", font=ImageFont.truetype(FONT_BOLD, 28), fill="#FFFFFF")
    draw.text((270, 218), "(Give it another try)", font=f_small, fill="#888888")
    
    msg = (
        "Por algún motivo, Xbox Dev Mode (o la aplicación seleccionada) tardó\n"
        "demasiado tiempo en iniciarse.\n\n"
        "Código de error: 0x8027025a"
    )
    draw.text((200, 265), msg, font=ImageFont.truetype(FONT_REG, 18), fill="#E0E0E0")
    
    draw.rounded_rectangle([(200, 375), (550, 425)], radius=6, fill="#2C1212", outline="#D9381E", width=1)
    draw.text((220, 390), "ERROR CODE: 0x8027025a", font=ImageFont.truetype(FONT_BOLD, 18), fill="#FF6B6B")
    
    draw_card(draw, 580, 260, 420, 170, "CAUSAS PRINCIPALES DEL FALLO", bg="#181818", border="#333333")
    causes = [
        "1. Caché del sistema saturada tras cambio de modo.",
        "2. Proceso anterior zombi / bloqueado en RAM.",
        "3. Timeout de autenticación con Xbox Network.",
        "4. Unidad de disco ocupada o suspendida."
    ]
    cy = 300
    for c in causes:
        draw.text((595, cy), c, font=f_small, fill="#CCCCCC")
        cy += 24

    draw.rounded_rectangle([(200, 480), (380, 535)], radius=8, fill="#107C10", outline="#66FF66", width=2)
    draw.text((260, 497), "Cerrar", font=f_bold, fill="#FFFFFF")
    draw.ellipse([(225, 496), (248, 519)], fill="#008000")
    draw.text((232, 498), "A", font=ImageFont.truetype(FONT_BOLD, 13), fill="#FFFFFF")
    
    draw.rounded_rectangle([(410, 480), (620, 535)], radius=8, fill="#2B2B2B", outline="#444444", width=1)
    draw.text((450, 497), "Más ayuda", font=f_text, fill="#CCCCCC")

    img.save(os.path.join(ASSETS_DIR, "img9_error_0x8027025a.png"))
    print("Generated img9_error_0x8027025a.png")

def gen_img_force_quit():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SOLUCIÓN 1: CIERRE FORZADO DE LA APLICACIÓN", "Finalizar el proceso colgado desde la Guía de Xbox (Botón Menú ➔ Salir)")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    draw.rectangle([(50, 110), (450, 630)], fill="#1C1C1C", outline="#303030", width=1)
    draw.rectangle([(50, 110), (450, 160)], fill="#252525")
    draw.text((70, 125), "GUÍA DE XBOX", font=f_bold, fill="#FFFFFF")
    draw.text((320, 125), "20:15", font=f_text, fill="#888888")
    
    draw.rounded_rectangle([(70, 180), (430, 235)], radius=6, fill="#122B15", outline="#107C10", width=2)
    draw.text((90, 195), "Xbox Dev Mode", font=f_bold, fill="#98C379")
    draw.text((90, 215), "En ejecución (Sin responder)", font=ImageFont.truetype(FONT_REG, 11), fill="#E06C75")
    
    draw.rounded_rectangle([(470, 180), (820, 480)], radius=10, fill="#232323", outline="#444444", width=2)
    draw.text((495, 200), "Opciones de la app", font=f_bold, fill="#A0A0A0")
    
    menu_items = [
        ("Abrir", False),
        ("Administrar app y complementos", False),
        ("Ver en Microsoft Store", False),
        ("Salir (Quit)", True),
        ("Anclar a Inicio", False)
    ]
    my = 235
    for item_text, is_selected in menu_items:
        if is_selected:
            draw.rounded_rectangle([(485, my), (805, my + 45)], radius=6, fill="#D9381E", outline="#FFAAAA", width=2)
            draw.text((505, my + 12), f"➡ {item_text}", font=f_bold, fill="#FFFFFF")
        else:
            draw.text((505, my + 12), f"   {item_text}", font=f_text, fill="#D0D0D0")
        my += 48
        
    draw.text((495, 445), "Presiona [A] para forzar el cierre", font=f_small, fill="#FFFFFF")

    draw_card(draw, 850, 180, 310, 430, "INSTRUCCIONES", bg="#181818", border="#333333")
    steps = [
        "1. Pulsa el botón Xbox del",
        "   mando para abrir la Guía.",
        "",
        "2. Resalta el icono de",
        "   'Xbox Dev Mode'.",
        "",
        "3. Pulsa el botón Menú",
        "   (las 3 líneas horizontales).",
        "",
        "4. Selecciona 'Salir' (Quit).",
        "",
        "5. Espera 10 segundos antes",
        "   de volver a abrir la app.",
        "",
        "✓ Libera la memoria RAM",
        "  y reinicia el proceso."
    ]
    sy = 220
    for s in steps:
        col = "#98C379" if s.startswith("✓") else ("#E5C07B" if s.startswith("4.") else "#D0D0D0")
        draw.text((865, sy), s, font=f_small, fill=col)
        sy += 20

    img.save(os.path.join(ASSETS_DIR, "img10_solucion1_force_quit.png"))
    print("Generated img10_solucion1_force_quit.png")

def gen_img_power_cycle():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SOLUCIÓN 2: REINICIO COMPLETO Y VACIADO DE CACHÉ", "Power Cycle (Hard Reset) de 10 segundos para limpiar la memoria residual")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    cards = [
        ("PASO A: APAGADO FORZADO", "Mantén presionado el botón Xbox físico frontal de la consola durante 10 SEGUNDOS completos hasta que el sistema se apague por completo.", "#107C10", "10 SEG"),
        ("PASO B: DESCONECTAR CORRIENTE", "Desconecta el cable de alimentación trasero de la consola. Espera de 30 a 60 SEGUNDOS para drenar los condensadores y la caché volátil.", "#0080FF", "30-60 SEG"),
        ("PASO C: RECONECTAR Y ENCENDER", "Vuelve a conectar el cable de alimentación y enciende la consola. El sistema operativo arrancará desde cero con la memoria limpia.", "#98C379", "INICIO LIMPIO")
    ]
    
    for idx, (ctitle, cdesc, ccol, cbadge) in enumerate(cards):
        cx = 50 + idx * 375
        draw_card(draw, cx, 140, 350, 440, "", bg="#181818", border="#333333")
        draw.rectangle([(cx, 140), (cx + 350, 146)], fill=ccol)
        
        draw.rounded_rectangle([(cx + 20, 165), (cx + 180, 205)], radius=6, fill=ccol)
        draw.text((cx + 30, 175), cbadge, font=f_bold, fill="#FFFFFF")
        
        draw.text((cx + 20, 230), ctitle, font=f_bold, fill="#FFFFFF")
        
        draw.rounded_rectangle([(cx + 20, 270), (cx + 330, 420)], radius=8, fill="#101010", outline="#282828", width=1)
        if idx == 0:
            draw.ellipse([(cx + 125, 295), (cx + 225, 395)], fill="#222222", outline="#107C10", width=3)
            draw.line([(cx + 175, 310), (cx + 175, 350)], fill="#107C10", width=4)
            draw.arc([(cx + 145, 320), (cx + 205, 380)], 310, 230, fill="#107C10", width=4)
        elif idx == 1:
            draw.rounded_rectangle([(cx + 115, 315), (cx + 235, 375)], radius=8, fill="#222222", outline="#0080FF", width=2)
            draw.line([(cx + 145, 375), (cx + 145, 410)], fill="#0080FF", width=4)
            draw.line([(cx + 205, 375), (cx + 205, 410)], fill="#0080FF", width=4)
            draw.text((cx + 130, 335), "PLUG OFF", font=f_small, fill="#0080FF")
        else:
            draw.ellipse([(cx + 125, 295), (cx + 225, 395)], fill="#107C10")
            draw.ellipse([(cx + 135, 305), (cx + 215, 385)], fill="#121212")
            draw.line([(cx + 145, 315), (cx + 205, 375)], fill="#FFFFFF", width=4)
            draw.line([(cx + 205, 315), (cx + 145, 375)], fill="#FFFFFF", width=4)
            
        draw.text((cx + 20, 440), cdesc, font=f_small, fill="#CCCCCC")

    draw.rectangle([(50, 600), (1150, 645)], fill="#152615", outline="#254A25", width=1)
    draw.text((70, 615), "✓ EFECTIVIDAD: Soluciona más del 85% de los errores 0x8027025a debidos a estados de suspensión rápida (Instant-On).", font=f_small, fill="#98C379")

    img.save(os.path.join(ASSETS_DIR, "img11_solucion2_power_cycle.png"))
    print("Generated img11_solucion2_power_cycle.png")

def gen_img_soft_reset():
    img = Image.new("RGB", (1200, 675), "#101010")
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SOLUCIÓN 3: RESTABLECER CONSOLA SIN PERDER JUEGOS", "Restablecer sistema operativo conservando aplicaciones, juegos y emuladores")
    f_title, f_sub, f_text, f_small, f_bold = get_fonts(22, 17, 14, 12)
    
    draw.rectangle([(50, 110), (1150, 155)], fill="#1C1C1C", outline="#303030", width=1)
    draw.text((70, 123), "Ruta: Configuración ➔ Sistema ➔ Información de la consola ➔ Restablecer consola", font=f_text, fill="#61AFEF")
    
    draw_card(draw, 100, 180, 480, 420, "", bg="#152415", border="#107C10")
    draw.rectangle([(100, 180), (580, 186)], fill="#107C10")
    
    draw.rounded_rectangle([(130, 205), (370, 245)], radius=6, fill="#107C10")
    draw.text((145, 217), "★ OPCIÓN RECOMENDADA", font=f_bold, fill="#FFFFFF")
    
    draw.text((130, 265), "Restablecer y mantener mis\njuegos y aplicaciones", font=ImageFont.truetype(FONT_BOLD, 22), fill="#FFFFFF")
    draw.text((130, 335), "(Reset and keep my games & apps)", font=f_small, fill="#98C379")
    
    safe_points = [
        "✓ Reinstala los archivos del sistema operativo.",
        "✓ Repara archivos corruptos de arranque.",
        "✓ CONSERVA todos tus juegos de Retail.",
        "✓ CONSERVA todas tus apps y datos de Dev Mode.",
        "✓ Resuelve el error 0x8027025a persistente."
    ]
    py = 370
    for p in safe_points:
        draw.text((130, py), p, font=f_small, fill="#E0FFE0")
        py += 24
        
    draw_button(draw, 130, 520, 260, 48, "Seleccionar opción [A]", f_bold, bg="#107C10", fg="#FFFFFF")

    draw_card(draw, 620, 180, 480, 420, "", bg="#241515", border="#552222")
    draw.rectangle([(620, 180), (1100, 186)], fill="#882222")
    
    draw.rounded_rectangle([(650, 205), (860, 245)], radius=6, fill="#552222")
    draw.text((665, 217), "⚠️ NO SELECCIONAR", font=f_bold, fill="#FFAAAA")
    
    draw.text((650, 265), "Restablecer y quitar todo\n(Factory Reset Total)", font=ImageFont.truetype(FONT_BOLD, 22), fill="#FFAAAA")
    draw.text((650, 335), "(Reset and remove everything)", font=f_small, fill="#888888")
    
    danger_points = [
        "✗ Borra absolutamente todo el disco duro.",
        "✗ Elimina tus perfiles, cuentas y configuraciones.",
        "✗ Elimina todos los juegos y emuladores instalados.",
        "✗ Desvincula el Modo Desarrollador por completo.",
        "✗ Solo usar si vas a vender o donar la consola."
    ]
    dy = 370
    for dp in danger_points:
        draw.text((650, dy), dp, font=f_small, fill="#FFCCCC")
        dy += 24
        
    draw_button(draw, 650, 520, 260, 48, "Evitar esta opción", f_text, bg="#332222", fg="#888888")

    img.save(os.path.join(ASSETS_DIR, "img12_solucion3_soft_reset.png"))
    print("Generated img12_solucion3_soft_reset.png")

if __name__ == "__main__":
    gen_img_error_screen()
    gen_img_force_quit()
    gen_img_power_cycle()
    gen_img_soft_reset()
    print("All error images generated successfully!")
