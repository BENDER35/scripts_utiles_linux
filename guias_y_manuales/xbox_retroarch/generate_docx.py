import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()
    
    # Page setup - Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Title
    title = doc.add_paragraph()
    title_run = title.add_run("Overclocking en Coreboot vs. BIOS/UEFI de Fabricante")
    title_run.font.name = 'Calibri Light'
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) # Navy
    title.paragraph_format.space_after = Pt(4)
    
    subtitle = doc.add_paragraph()
    sub_run = subtitle.add_run("Análisis técnico de capacidades, limitaciones arquitectónicas y comparativa exhaustiva")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    subtitle.paragraph_format.space_after = Pt(20)

    def add_h1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Calibri Light'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x2E, 0x6B, 0x9E)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        return p

    def add_callout(text, title="NOTA"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(2)
        tr = cp.add_run(f"[{title}] ")
        tr.bold = True
        tr.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
        tr2 = cp.add_run(text)
        tr2.font.size = Pt(10)
        tr2.font.italic = True
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. Introducción y Fundamentos Arquitectónicos
    add_h1("1. Introducción y Fundamentos Arquitectónicos")
    
    p = doc.add_paragraph(
        "Para comprender el estado del overclocking en coreboot y sus diferencias respecto al firmware propietario, "
        "es indispensable analizar la disparidad fundamental en objetivos de diseño y arquitectura de software entre "
        "ambas soluciones."
    )
    p.paragraph_format.space_after = Pt(6)

    add_h2("¿Qué es coreboot?")
    p = doc.add_paragraph(
        "coreboot (anteriormente conocido como LinuxBIOS) es un proyecto de software libre enfocado en la inicialización "
        "minimalista del hardware. Su propósito no es ofrecer un entorno operativo completo con interfaces visuales ni "
        "módulos complejos de gestión de usuario, sino ejecutar únicamente las tareas estrictamente necesarias para "
        "despertar la CPU, inicializar la memoria RAM (mediante código nativo o módulos binarios como Intel FSP o AMD AGESA), "
        "configurar buses principales (PCIe, SMBus, etc.) y pasar inmediatamente el control a un payload (carga útil)."
    )
    p.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "Entre los payloads habituales se encuentran SeaBIOS (emulación BIOS heredada), EDK2/TianoCore (entorno UEFI completo), "
        "GRUB2 (gestor de arranque directo) o LinuxBoot (un kernel Linux real utilizado como firmware de arranque). "
        "Bajo este paradigma, el tiempo de arranque suele ser de menos de 1 a 2 segundos y la superficie de ataque "
        "se reduce de forma drástica frente a un firmware monolítico convencional."
    )
    p.paragraph_format.space_after = Pt(6)

    add_h2("¿Qué es una BIOS/UEFI de fabricante?")
    p = doc.add_paragraph(
        "El firmware tradicional de los fabricantes de placas base para consumo (ASUS, MSI, Gigabyte, ASRock) suele estar basado "
        "en soluciones propietarias de proveedores independientes de BIOS (IBVs) como AMI (Aptio), InsydeH2O o Phoenix. "
        "Sobre esta base, cada marca desarrolla enormes capas de personalización visual (interfaces gráficas UEFI de alta resolución "
        "controlables con ratón) y subsistemas avanzados de control de hardware orientados al mercado del gaming y entusiasta "
        "(ej. ASUS AI Overclocking, MSI Click BIOS, perfiles XMP/EXPO, calibración de línea de carga o perfiles de ventiladores)."
    )
    p.paragraph_format.space_after = Pt(6)

    add_callout(
        "Coreboot prioriza: mínima cantidad de código ejecutable en modo SMM (System Management Mode), seguridad, "
        "reproducibilidad y estabilidad estricta. Una BIOS comercial para entusiastas prioriza la compatibilidad plug-and-play, "
        "el rendimiento pico, herramientas de ajuste visual y la diferenciación comercial de producto.",
        "DIVERGENCIA FILOSÓFICA"
    )

    # 2. El Overclocking en coreboot
    add_h1("2. El Overclocking en coreboot: Estado Actual y Funcionamiento")

    p = doc.add_paragraph(
        "A diferencia de las placas base convencionales donde el overclocking se concibe como una experiencia interactiva "
        "a través de deslizadores y menús en la interfaz de configuración (setup), en coreboot el overclocking no es una prioridad "
        "ni existe un soporte 'plug-and-play' universal."
    )
    p.paragraph_format.space_after = Pt(6)

    add_h2("Ausencia de Interfaz de Configuración Dinámica (Setup GUI)")
    p = doc.add_paragraph(
        "Por diseño, coreboot no cuenta con un menú gráfico interactivo para manipular voltajes ni multiplicadores en tiempo de arranque. "
        "La configuración de coreboot se define durante el proceso de compilación a través del sistema Kconfig (make menuconfig) "
        "y árboles de dispositivos estáticos (ficheros devicetree.cb). Si se desea alterar un parámetro de bajo nivel que no esté "
        "expuesto al sistema operativo, generalmente se requiere modificar el código fuente o el archivo de configuración y compilar "
        "una nueva imagen binaria de la ROM para flashearla en el chip SPI."
    )
    p.paragraph_format.space_after = Pt(6)

    add_h2("Overclocking de Memoria RAM y Perfiles XMP/EXPO")
    p = doc.add_paragraph(
        "La inicialización de la memoria (raminit) es una de las fases más críticas y delicadas del arranque:"
    )
    p.paragraph_format.space_after = Pt(4)

    bp1 = doc.add_paragraph(style='List Bullet')
    r = bp1.add_run("Perfiles JEDEC por defecto: ")
    r.bold = True
    bp1.add_run("Coreboot prioriza siempre la máxima estabilidad leyendo los perfiles estándar JEDEC grabados en el chip SPD (Serial Presence Detect) del módulo RAM. Si un módulo comercial de 3600 MT/s requiere XMP para funcionar a esa frecuencia, coreboot normalmente lo arrancará a su frecuencia base SPD (por ejemplo, 2133 MT/s o 2400 MT/s).")
    bp1.paragraph_format.space_after = Pt(4)

    bp2 = doc.add_paragraph(style='List Bullet')
    r = bp2.add_run("Soporte nativo de Intel XMP (coreboot 4.4+): ")
    r.bold = True
    bp2.add_run("En plataformas Intel compatibles con raminit nativo, coreboot puede parsear las cabeceras XMP Perfil 1 y Perfil 2. Sin embargo, aplica de forma estricta barreras de seguridad (límites máximos de voltaje de 1.5 V en DDR3 y restricciones de número de módulos DIMM por canal). Si el perfil XMP excede estos límites, coreboot retrocede automáticamente al perfil JEDEC seguro.")
    bp2.paragraph_format.space_after = Pt(4)

    bp3 = doc.add_paragraph(style='List Bullet')
    r = bp3.add_run("Modificaciones en compilación: ")
    r.bold = True
    bp3.add_run("Para forzar frecuencias superiores en plataformas con raminit nativo, los desarrolladores deben habilitar flags especiales (como NATIVE_RAMINIT_IGNORE_XMP_MAX_DIMMS) o alterar los mapas de tiempos en el código fuente de inicialización de memoria de la arquitectura.")
    bp3.paragraph_format.space_after = Pt(4)

    bp4 = doc.add_paragraph(style='List Bullet')
    r = bp4.add_run("Evolución con Dasharo (3mdeb): ")
    r.bold = True
    bp4.add_run("Distribuciones modernas de coreboot como Dasharo (implementadas sobre placas comerciales como la MSI PRO Z690-A DDR4 / MSI PRO Z790-P DDR5) integran un payload EDK2 que expone una opción en el menú de configuración ('Dasharo System Features -> Memory Configuration -> Memory SPD Profile') que permite seleccionar perfiles XMP. No obstante, Dasharo advierte que desviarse de JEDEC puede provocar fallos de arranque (boot loops) debido a la menor tolerancia en el entrenamiento de memoria frente a la BIOS propietaria de MSI.")
    bp4.paragraph_format.space_after = Pt(6)

    add_h2("Overclocking de CPU: Multiplicadores, Reloj Base (BCLK) y Voltajes")
    p = doc.add_paragraph(
        "A nivel de procesador, el panorama de overclocking en coreboot presenta importantes limitaciones estructurales:"
    )
    p.paragraph_format.space_after = Pt(4)

    bp_cpu1 = doc.add_paragraph(style='List Bullet')
    r = bp_cpu1.add_run("Dependencia de Blobs de Fabricante (FSP / AGESA): ")
    r.bold = True
    bp_cpu1.add_run("En plataformas modernas de Intel y AMD, la inicialización del procesador no se realiza íntegramente con código abierto, sino a través de blobs binarios como Intel FSP (Firmware Support Package) o AMD AGESA / openSIL. Aunque las estructuras de datos de FSP permiten configurar ciertos ratios y límites de energía (PL1/PL2), coreboot por lo general pasa valores estándar especificados por el fabricante para garantizar la fiabilidad del sistema.")
    bp_cpu1.paragraph_format.space_after = Pt(4)

    bp_cpu2 = doc.add_paragraph(style='List Bullet')
    r = bp_cpu2.add_run("Ausencia de control de VRM y LLC: ")
    r.bold = True
    bp_cpu2.add_run("Las funciones de ajuste de Load-Line Calibration (LLC), control de fases de potencia PWM, frecuencias de conmutación de los reguladores y offset de voltaje Vcore dinámico no están implementadas ni accesibles en coreboot. Los circuitos integrados de control de energía del fabricante (como los controladores de Digi+ VRM de ASUS o chips TPU/EPU) permanecen con sus valores por defecto o en modo genérico.")
    bp_cpu2.paragraph_format.space_after = Pt(4)

    bp_cpu3 = doc.add_paragraph(style='List Bullet')
    r = bp_cpu3.add_run("Impacto de la desactivación de Intel ME (Management Engine): ")
    r.bold = True
    bp_cpu3.add_run("Muchos usuarios que instalan coreboot aplican herramientas como 'me_cleaner' para neutralizar el motor de gestión de Intel. Esto puede alterar el ICC (Integrated Clock Controller), impidiendo modificaciones del reloj base (BCLK) o forzando límites de energía de fábrica inmutables.")
    bp_cpu3.paragraph_format.space_after = Pt(4)

    bp_cpu4 = doc.add_paragraph(style='List Bullet')
    r = bp_cpu4.add_run("Overclocking mediante el Sistema Operativo: ")
    r.bold = True
    bp_cpu4.add_run("La vía más viable para realizar ajustes de frecuencia en un equipo con coreboot es delegar la tarea al sistema operativo una vez completado el arranque. En Linux, si los registros de control específicos del modelo (MSR) no han sido bloqueados (MSR lock bit) por el firmware, se pueden utilizar utilidades de espacio de usuario como msr-tools, undervolt, ryzenadj (para APUs AMD) o CoreFreq. En Windows, herramientas como Intel XTU pueden operar si la interfaz ACPI y las tablas correspondientes fueron expuestas por el payload.")
    bp_cpu4.paragraph_format.space_after = Pt(6)

    add_h2("Riesgo de Bloqueo (Brick) y Recuperación ante Inestabilidad")
    p = doc.add_paragraph(
        "En un entorno con BIOS comercial, si una configuración de overclocking o subtiempos de memoria resulta inestable, "
        "un circuito perro guardián (watchdog timer) detecta la falta de señal POST tras 2 o 3 intentos fallidos y resetea "
        "automáticamente los valores de la CMOS a niveles seguros, o se cuenta con tecnologías como BIOS Flashback y Dual BIOS. "
        "En coreboot, un fallo en el entrenamiento de memoria a nivel de FSP/MRC suele dejar la placa en un estado no recuperable "
        "por software, requiriendo un borrado manual de la CMOS (mediante jumper físico o extrayendo la pila) o, en el peor "
        "de los casos, reprogramar el chip SPI flash externamente usando pinzas SOIC8/Pomona y un programador hardware (como CH341A o Raspberry Pi)."
    )
    p.paragraph_format.space_after = Pt(6)

    # 3. Comparativa Detallada
    add_h1("3. Comparativa Detallada: coreboot vs. BIOS/UEFI de Fabricante")

    p = doc.add_paragraph(
        "A continuación se presenta un cuadro comparativo exhaustivo entre coreboot y una BIOS/UEFI de fabricante "
        "orientada al rendimiento:"
    )
    p.paragraph_format.space_after = Pt(6)

    # Table
    table = doc.add_table(rows=8, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.8), Inches(2.3), Inches(2.4)]
    
    headers = ["Característica / Parámetro", "coreboot (+ Payloads habituales)", "BIOS/UEFI Propietaria (ASUS/MSI/etc.)"]
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(h_text)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)

    rows_data = [
        (
            "Interfaz de configuración de Overclocking",
            "Inexistente en coreboot puro. Opciones muy limitadas en payloads modernos como Dasharo/EDK2. No hay controles gráficos interactivos.",
            "Interfaz UEFI gráfica avanzada (modo EZ y modo Avanzado) con soporte completo para ratón, perfiles guardables en USB y monitoreo en tiempo real."
        ),
        (
            "Perfiles de Memoria (Intel XMP / AMD EXPO)",
            "Prioriza perfiles SPD JEDEC básicos. Requiere habilitar flags en compilación o soporte específico en EDK2 (Dasharo). Límite estricto de voltajes.",
            "Soporte inmediato 'un clic' (XMP 2.0/3.0, AMD EXPO). Reentrenamiento automático de algoritmos de memoria y perfiles preconfigurados de fábrica."
        ),
        (
            "Control de CPU (Multiplicadores, PBO, Curve Optimizer)",
            "Valores estándar por defecto gobernados por Intel FSP o AMD AGESA. Sin ajustes manuales de PBO o curvas de voltaje en el firmware.",
            "Ajuste granular por núcleo, offset de ratios AVX, AMD Precision Boost Overdrive (PBO), Curve Optimizer por núcleo, BCLK con generadores de reloj externos."
        ),
        (
            "Regulación de Voltajes y VRM (LLC, Vcore, VDDQ)",
            "No implementada. El VRM opera con la curva de fábrica o predefinida por las tablas de inicialización. Sin gestión de Load-Line Calibration.",
            "Control milivoltio a milivoltio (modo fijo, offset o adaptativo), niveles de LLC (1 a 8), frecuencias de conmutación PWM y límites térmicos de VRM."
        ),
        (
            "Ajuste de tiempos y subtiempos de RAM",
            "Tiempos determinados por JEDEC o parámetros fijos del árbol devicetree.cb. Modificarlos requiere recompilar la ROM o alterar código C.",
            "Control exhaustivo de temporizaciones primarias (tCL, tRCD, tRP, tRAS), secundarias y terciarias (tRFC, tREFI, tWR, Gear 1/2/4)."
        ),
        (
            "Recuperación ante fallos de arranque (Boot Failure)",
            "Sin watchdog de recuperación de OC. Riesgo de cuelgue en POST. Requiere borrado manual de CMOS (jumper/pila) o flasheo externo por SPI.",
            "Sistemas integrados de autodiagnóstico: Watchdog automático que restaura valores seguros tras 3 intentos, botones Safe Boot, Flashback y Dual BIOS."
        ),
        (
            "Objetivos primarios y Tiempo de arranque",
            "Arranque ultrarrápido (< 1-2 s), mínima superficie de ataque, auditoría de código libre, eliminación de telemetría y bloatware.",
            "Rendimiento extremo, máxima compatibilidad comercial y estética, pero con arranque más lento (5-15 s) y millones de líneas de código cerrado (SMM/DXE)."
        )
    ]

    for row_idx, row_data in enumerate(rows_data):
        row_cells = table.rows[row_idx + 1].cells
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F7F9FB"
        for col_idx, text in enumerate(row_data):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.bold = True
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4. Conclusiones y Caso de Uso
    add_h1("4. Conclusión: ¿Para qué perfiles es adecuado cada firmware?")
    
    p = doc.add_paragraph(
        "La elección entre coreboot y una BIOS de fabricante depende enteramente de las prioridades del usuario:"
    )
    p.paragraph_format.space_after = Pt(4)

    bp_c1 = doc.add_paragraph(style='List Bullet')
    r = bp_c1.add_run("coreboot es la opción óptima para: ")
    r.bold = True
    bp_c1.add_run("Servidores, centros de datos, portátiles corporativos (como Lenovo ThinkPad certificados o Chromebooks), entusiastas de la privacidad y sistemas de alta seguridad donde la auditabilidad del código, la ausencia de puertas traseras propietarias y la velocidad de arranque son imperativas.")
    bp_c1.paragraph_format.space_after = Pt(4)

    bp_c2 = doc.add_paragraph(style='List Bullet')
    r = bp_c2.add_run("La BIOS propietaria del fabricante es la opción óptima para: ")
    r.bold = True
    bp_c2.add_run("Jugadores competitivos, 'overclockers' y creadores de contenido que buscan exprimir cada megahertzio de su procesador y memoria RAM, requiriendo soporte inmediato de XMP/EXPO, ajustes térmicos finos del VRM y salvaguardas automáticas contra inestabilidades.")
    bp_c2.paragraph_format.space_after = Pt(8)

    # 5. Fuentes y Referencias
    add_h1("5. Fuentes y Referencias Consultadas")
    
    sources = [
        ("Documentación Oficial de Coreboot (coreboot.org)", "https://doc.coreboot.org/ y https://doc.coreboot.org/getting_started/architecture.html", "Arquitectura general de coreboot, separación de fases (bootblock, romstage, ramstage) y desacoplamiento de cargas útiles (payloads)."),
        ("Repositorio Oficial de Coreboot - raminit & XMP", "https://review.coreboot.org/cgit/coreboot.git/ y docs.coreboot.org", "Implementación del soporte para perfiles Intel XMP en el inicializador de memoria nativo (raminit) y directivas de seguridad como NATIVE_RAMINIT_IGNORE_XMP_MAX_DIMMS."),
        ("Dasharo Documentation (3mdeb)", "https://docs.dasharo.com/unified/msi/overview/ y https://docs.dasharo.com/guides/memory-configuration/", "Documentación de la distribución Dasharo coreboot+EDK2 para placas base de sobremesa MSI PRO Z690/Z790: menús de configuración de perfiles SPD/XMP, estabilidad de memoria y overclocking a nivel de SO."),
        ("Listas de Correo de Desarrolladores de Coreboot (coreboot-mailing-list)", "https://mail.coreboot.org/hyperkitty/list/coreboot@coreboot.org/", "Hilos técnicos de discusión sobre límites de frecuencia en chipsets Intel/AMD, omisión de fusibles de memoria, bypass de multiplicadores mediante FSP y limitaciones de circuitos VRM comerciales."),
        ("Documentación de Intel FSP (Firmware Support Package)", "https://github.com/intel/FSP y https://www.intel.com/content/www/us/en/developer/topic-technology/open/firmware-support-package/overview.html", "Detalles sobre la interfaz binaria de Intel para inicialización de silicio y memoria, y cómo gestiona los parámetros de ratio y consumo transferidos por coreboot."),
        ("Comunidad de Modding y Foros de Coreboot (Reddit r/coreboot)", "https://www.reddit.com/r/coreboot/", "Experiencias de usuarios y desarrolladores en optimización de frecuencias de RAM (ej. ThinkPads X230/T430), incompatibilidades de XMP no estándar y procedimientos de recuperación de CMOS.")
    ]

    for title_s, url_s, desc_s in sources:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(4)
        sp.paragraph_format.left_indent = Inches(0.2)
        
        r1 = sp.add_run(f"• {title_s}: ")
        r1.bold = True
        r1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
        r2 = sp.add_run(desc_s + " ")
        
        r3 = sp.add_run(f"[{url_s}]")
        r3.font.italic = True
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x2E, 0x6B, 0x9E)

    # Save
    output_path = "/home/bender/Descargas/overclocking_coreboot_vs_bios.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
