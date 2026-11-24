import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

font_family = "Segoe UI"
header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
title_font = Font(name=font_family, size=15, bold=True, color="1F497D")
subtitle_font = Font(name=font_family, size=10, italic=True, color="595959")
cell_font = Font(name=font_family, size=10, color="000000")
bold_font = Font(name=font_family, size=10, bold=True, color="000000")

thin_border_side = Side(border_style="thin", color="D9D9D9")
table_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

fill_sheet0 = PatternFill(start_color="333F48", end_color="333F48", fill_type="solid") # Slate
fill_sheet1 = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Navy Blue
fill_sheet2 = PatternFill(start_color="007070", end_color="007070", fill_type="solid") # Deep Teal
fill_sheet3 = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid") # Steel Blue
fill_sheet4 = PatternFill(start_color="0B5394", end_color="0B5394", fill_type="solid") # Cobalt Blue
fill_sheet5 = PatternFill(start_color="2D6A4F", end_color="2D6A4F", fill_type="solid") # Forest Green

zebra_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

align_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
align_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

def format_sheet(ws, title, subtitle, headers, data, header_fill, col_widths):
    ws.views.sheetView[0].showGridLines = True
    ws.cell(row=2, column=1, value=title).font = title_font
    ws.cell(row=3, column=1, value=subtitle).font = subtitle_font
    
    row_idx = 5
    ws.row_dimensions[row_idx].height = 28
    for col_idx, h in enumerate(headers, 1):
        c = ws.cell(row=row_idx, column=col_idx, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = align_center
        
    for row_data in data:
        row_idx += 1
        ws.row_dimensions[row_idx].height = 85
        is_even = (row_idx % 2 == 0)
        current_fill = zebra_fill if is_even else white_fill
        for col_idx, val in enumerate(row_data, 1):
            c = ws.cell(row=row_idx, column=col_idx, value=val)
            c.font = cell_font
            c.fill = current_fill
            c.border = table_border
            if col_idx in [1, 2]:
                c.font = bold_font
                c.alignment = align_left
            elif "★" in str(val):
                c.alignment = align_center
                c.font = Font(name=font_family, size=10, bold=True, color="C00000")
            elif col_idx in [3, len(row_data) - 2]: # Titularidad o Teléfono
                c.alignment = align_center
            else:
                c.alignment = align_left

    last_col_letter = get_column_letter(len(headers))
    ws.auto_filter.ref = f"A5:{last_col_letter}{row_idx}"
    ws.freeze_panes = "A6"
    
    for col_idx, width in enumerate(col_widths, 1):
        letter = get_column_letter(col_idx)
        ws.column_dimensions[letter].width = width

# =============================================================
# SHEET 0: INTRODUCCIÓN Y GUÍA
# =============================================================
ws0 = wb.active
ws0.title = "Guía y Canales de Acceso"
ws0.views.sheetView[0].showGridLines = True

ws0.cell(row=2, column=2, value="GUÍA INTEGRAL DE RECURSOS PARA PERSONAS CON DISCAPACIDAD - COMUNIDAD DE MADRID").font = title_font
ws0.cell(row=3, column=2, value="Enfoque especializado en Centros Ocupacionales (CO), alternativas formativas, habilidades sociales, medicina/TIC y software libre").font = subtitle_font

guide_content = [
    ("1. Vías de Acceso y Solicitud de Plaza en Centros Ocupacionales (CO)",
     "• Grado de Discapacidad: Requisito imprescindible (>= 33%) tramitado en los Centros Base de la Comunidad de Madrid.\n"
     "• Programa Individual de Atención (PIA): A través de los Servicios Sociales Municipales bajo el marco de la Ley de Dependencia se solicita plaza pública en Centro Ocupacional.\n"
     "• AMAPAD: Agencia Madrileña para el Apoyo a las Personas Adultas con Discapacidad (asesoramiento y medidas judiciales de apoyo).\n"
     "• Plazas Privadas: La mayoría de fundaciones concertadas disponen también de un cupo de plazas privadas de acceso directo."),
    
    ("2. Titularidad: ¿Público (del Estado / CAM), Concertado o Privado?",
     "• Público Autonómico / Estatal: Centros de titularidad y gestión directa de la Comunidad de Madrid (ej. CO Valdelatas, CO Barajas). El acceso laboral es vía Oposiciones y Bolsas de Contratación de la Administración Pública.\n"
     "• Concertado / Tercer Sector: Centros Ocupacionales de fundaciones y asociaciones sin ánimo de lucro (Juan XXIII, A LA PAR, Down Madrid, Aprocor, AFANIAS, Grupo AMÁS) con plazas públicas concertadas con la CAM. El envío de CV se realiza de forma directa a sus Departamentos de Selección / RRHH.\n"
     "• Privado Sanitario / Libre: Entidades que operan con gestión privada directa o convenios específicos."),

    ("3. Centros Ocupacionales (CO) y Habilidades Sociales (Hoja 2)",
     "Todos los CO en Madrid cuentan obligatoriamente con el Área de Ajuste Personal y Social (APS). Los centros seleccionados destacan por trabajar de forma intensiva la superación de la timidez, asertividad, resolución pacífica de conflictos y el 'tratar con gente' mediante asambleas de autogestores, programas de radio comunitaria, simulaciones laborales y salidas al entorno natural."),

    ("4. Centros Ocupacionales (CO) con Buen Ambiente y Trato Humano (Hoja 3)",
     "Selección de Centros Ocupacionales con excelentes valoraciones de familias, usuarios y trabajadores por su clima afectivo, cercano y familiar ('como en casa'), donde se enseña activamente la empatía, el respeto mutuo, la sonrisa y la cortesía hacia los demás.")
]

row_idx = 5
for section_title, section_text in guide_content:
    ws0.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=9)
    cell_t = ws0.cell(row=row_idx, column=2, value=section_title)
    cell_t.font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    cell_t.fill = fill_sheet0
    cell_t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws0.row_dimensions[row_idx].height = 25
    row_idx += 1
    
    ws0.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=9)
    cell_b = ws0.cell(row=row_idx, column=2, value=section_text)
    cell_b.font = cell_font
    cell_b.alignment = align_left
    cell_b.border = table_border
    ws0.row_dimensions[row_idx].height = 75
    row_idx += 2

for col_l in ["B", "C", "D", "E", "F", "G", "H", "I"]:
    ws0.column_dimensions[col_l].width = 24

# =============================================================
# SHEET 1: ALTERNATIVAS A CURSOS
# =============================================================
ws1 = wb.create_sheet(title="Alternativas a Cursos")
headers_sheet1 = [
    "Nombre de la Entidad / Centro",
    "Tipo de Recurso / Modalidad",
    "Titularidad (Público / Concertado / Privado)",
    "Perfil / Destinatarios",
    "¿En qué consiste la alternativa?",
    "Talleres Prácticos y Actividades",
    "Ventaja frente a un curso convencional",
    "Requisitos y Vía de Acceso",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono",
    "Email / Web"
]

data_sheet1 = [
    (
        "Fundación A LA PAR (Centro Ocupacional)",
        "Centro Ocupacional y Talleres Prelaborales",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Discapacidad intelectual ligera y moderada (18-65 años)",
        "Estructura de talleres productivos reales donde no hay exámenes teóricos, sino aprendizaje vivencial adaptado al ritmo de cada usuario.",
        "Carpintería artesanal, pintura industrial, huerto ecológico, lavado de vehículos (FundaCars), diseño textil y floristería.",
        "Sin presión evaluativa; adquisición de destrezas manuales reales, hábitos laborales y trabajo en equipo seguro.",
        "Plazas públicas mediante derivación de Servicios Sociales (CAM) o plaza privada directa.",
        "Web: alapar.ong/trabaja-con-nosotros\nEmail RRHH: rrhh@alapar.ong / seleccion@alapar.ong\nPortal InfoJobs corporativo",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid (Montecarmelo)",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional Concertado (Red Pública CAM)",
        "Concertado (Red Pública CAM / Gestión Fundación SER)",
        "Personas con discapacidad intelectual en edad laboral",
        "Atención diurna enfocada en laborterapia y habilitación ocupacional, dividida en ajuste personal/social y actividades prácticas continuas.",
        "Talleres manipulativos y de reciclaje, artesanía en madera, jardinería, podcast y radio inclusiva ('Échale Papas') y deporte.",
        "Aprendizaje 100% práctico y relacional; proyecto de radio comunitaria que estimula la expresión libre sin temarios rígidos.",
        "Derivación oficial de la Dirección General de Atención a Personas con Discapacidad (CAM).",
        "Email RRHH: rrhh@fundacion-ser.org\nFormulario de empleo en web oficial: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46 / C/ Marqués de Urquijo, 47, 28008 Madrid",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    ),
    (
        "Fundación Capacis (Aula Laboral y Profesional)",
        "Programa Prelaboral y Empleo con Apoyo",
        "Privado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Jóvenes con Inteligencia Límite (IL) y discapacidad intelectual ligera",
        "Metodología de 'Aprender Haciendo' para jóvenes que no encajan en cursos reglados por exceso de carga teórica.",
        "Módulos prácticos de digitalización básica, administración auxiliar, comercio, logística y proyectos de aula.",
        "Itinerario hiper-personalizado sin la frustración de suspensos académicos; preparador laboral individual para empresa.",
        "Acceso directo contactando con la entidad; entrevista previa y valoración pedagógica del perfil.",
        "Email Selección: capacis@fundacioncapacis.org (Asunto: 'CV - Candidatura Selección')\nLinkedin de la Fundación",
        "C/ Agustín de Iturbide, 14, 28043 Madrid (Hortaleza)",
        "91 931 34 48",
        "capacis@fundacioncapacis.org\nhttps://www.fundacioncapacis.org"
    ),
    (
        "Fundación Juan XXIII (Centro Ocupacional e Inserción)",
        "Centro Ocupacional y Empleo Protegido",
        "Concertado / Tercer Sector (Fundación de iniciativa social)",
        "Personas con discapacidad intelectual y/o psicosocial",
        "Campus ocupacional donde las personas aprenden tareas reales en unidades productivas con apoyo multidisciplinar permanente.",
        "Horticultura y agroecología urbana, digitalización documental, catering/cocina adaptada, logística y manipulados industriales.",
        "Combina producción real con ajuste psicosocial, deporte, desarrollo cognitivo y vida independiente.",
        "Plazas públicas a través de la Red de Atención a la Discapacidad de la CAM o plaza privada.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Fundación Aprocor (Centros Ocupacionales y Hortaleza)",
        "Centro Ocupacional y Espacio de Inclusión",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Personas con discapacidad intelectual y del desarrollo",
        "Enfoque de Planificación Centrada en la Persona (PCP). Cada usuario define sus metas en lugar de someterse a un programa cerrado.",
        "El Huerto de Aprocor (jardinería comunitaria), manipulación de productos, reciclaje, eventos en Begonia's Garden.",
        "Elimina las metodologías escolásticas; fomenta la presencia en el barrio y la autonomía comunitaria real.",
        "Coordinación con Servicios Sociales de la Comunidad de Madrid o contacto con su Área Social.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org / agenciadecolocacion@fundacionaprocor.com",
        "C/ Vicente Morales, 5 / C/ Esteban Palacios, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Grupo Envera (Centro Ocupacional Colmenar Viejo)",
        "Centro Integral Ocupacional y Prelaboral",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Personas con discapacidad intelectual y necesidades de apoyo",
        "Centro diurno que utiliza tareas ocupacionales y proyectos comunicativos como motor de autonomía.",
        "Emisora comunitaria 'Radio Terrícola', talleres de jardinería, ensamblaje y manipulado, encuadernación artesanal.",
        "Proyecto de radio donde entrevistan a personalidades reales, desarrollando fluidez verbal y seguridad sin exámenes.",
        "Derivación de la Consejería de Asuntos Sociales de la CAM o contacto directo.",
        "Portal de Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. de Colmenar Viejo a Miraflores, Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    ),
    (
        "Down Madrid (Centro 3 Olivos - Proyecto FOCUS)",
        "Proyecto de Transición al Empleo y Centro Ocupacional",
        "Concertado / Tercer Sector (Fundación de utilidad pública)",
        "Jóvenes y adultos con síndrome de Down y discapacidad intelectual",
        "Formación para la vida adulta que sustituye los temarios rígidos por competencias sociolaborales vivenciales.",
        "Simulaciones de entornos laborales de oficina y atención al cliente, arte y creatividad, cocina para la autonomía.",
        "Enfoque en soft skills, resolución de problemas prácticos y desarrollo personal, evitando la frustración académica formal.",
        "Entrevista de acogida en Down Madrid y valoración del equipo psicopedagógico.",
        "Web Empleo: downmadrid.org/trabaja-con-nosotros\nEmail RRHH: rrhh@downmadrid.org / seleccion@downmadrid.org",
        "C/ Cueva de Montesinos, 45, 28034 Madrid (Fuencarral - Valverde)",
        "91 387 67 90",
        "downmadrid@downmadrid.org\nhttps://downmadrid.org"
    ),
    (
        "Fundación Prodis (Programa Empresa con Futuro)",
        "Capacitación Ocupacional y Empleo con Apoyo",
        "Privado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Jóvenes con discapacidad intelectual",
        "Modelo formativo adaptado que entrena hábitos laborales y competencias mediante metodologías prácticas en empresa.",
        "Digitalización, apoyo en tareas auxiliares de servicios, reprografía, preparación de pedidos, comunicación básica.",
        "Acompañamiento por mediadores laborales 'in situ' que adaptan puestos sin obligar al usuario a exámenes teóricos.",
        "Solicitud directa en la Fundación Prodis tras etapa escolar o derivación pública.",
        "Email Selección: seleccion@fundacionprodis.org / fundacionprodis@fundacionprodis.org\nWeb: fundacionprodis.org",
        "Bulevar Indalecio Prieto, 2, 28032 Madrid (Vicálvaro / San Blas)",
        "91 371 53 51",
        "fundacionprodis@fundacionprodis.org\nhttps://www.fundacionprodis.org"
    ),
    (
        "Red de Centros de Rehabilitación Laboral - CRL (CAM)",
        "Dispositivos Públicos de Rehabilitación Psicosocial y Laboral",
        "Público Autonómico (Red de Salud Mental CAM / Gestión concertada)",
        "Personas con enfermedad mental / discapacidad psicosocial (18-65 años)",
        "Red pública que prepara para el mundo laboral sin la rigidez de una academia de cursos mediante talleres y ajuste prelaboral.",
        "Talleres de mantenimiento, administración básica, informática adaptada, diseño gráfico, restauración y tolerancia al estrés.",
        "El objetivo no es aprobar un examen, sino recuperar ritmos, hábitos y confianza para volver a trabajar.",
        "Acceso exclusivo mediante propuesta y derivación del Centro de Salud Mental (CSM) de distrito público.",
        "Canal CV: A través de las entidades gestoras adjudicatarias (ej. grupo5.net/empleo, intress.org/empleo, fundacionmanantial.org)",
        "Red distribuida en distritos de Madrid capital y municipios de la región",
        "91 413 72 40 (CRL Juan XXIII) / Consultar CSM",
        "https://www.comunidad.madrid"
    ),
    (
        "Fundación Randstad (Hub de Innovación Social)",
        "Itinerarios Individualizados de Transición al Empleo",
        "Privada (Fundación corporativa Randstad)",
        "Cualquier tipo de discapacidad (física, sensorial, intelectual o psíquica)",
        "Capacitación personalizada que huye del formato tradicional de aula para centrarse en un itinerario a medida con tutor.",
        "Entrenamiento en entrevistas de trabajo, herramientas digitales, role-playing de situaciones laborales, intermediación.",
        "Flexibilidad absoluta: no exige un número cerrado de horas lectivas rígidas; se avanza según los progresos individuales.",
        "Inscripción directa a través del portal web o solicitando cita en el Hub.",
        "Web Empleo: randstad.es/fundacion-randstad\nEmail Selección: seleccion@fundacionrandstad.es / hub@fundacionrandstad.es",
        "C/ Raimundo Fernández Villaverde, 57 Bis, 28003 Madrid (Cuatro Caminos)",
        "91 490 62 88",
        "hub@fundacionrandstad.es\nhttps://www.randstad.es/fundacion-randstad"
    ),
    (
        "Inserta Empleo / Fundación ONCE (Centro Madrid)",
        "Programas Prelaborales y Plataforma Por Talento",
        "Tercer Sector (Fundación ONCE / Corporación Social)",
        "Personas con certificado de discapacidad (>= 33%) de cualquier tipología",
        "Plataforma de capacitación activa y prelaboral adaptada con seguimiento de orientadores especializados.",
        "Módulos de alfabetización digital adaptada, búsqueda activa de empleo, talleres de motivación y autoconocimiento.",
        "Orientación personalizada uno a uno, adaptada a barreras específicas (físicas, cognitivas o sensoriales).",
        "Inscripción gratuita presentando el certificado de discapacidad en la sede o vía web.",
        "Web Empleo: empleo.fundaciononce.es / portalentodigital.fundaciononce.es\nEmail RRHH: rrhh@fundaciononce.es",
        "C/ Sebastián Herrera, 15, 28012 Madrid (Arganzuela)",
        "91 713 15 50",
        "candidatos.madrid.inserta@fundaciononce.es\nhttps://www.insertaempleo.es"
    ),
    (
        "AFANIAS (Centros Ocupacionales Pozuelo y Canillejas)",
        "Red de Centros Ocupacionales Especializados",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Personas con discapacidad intelectual en etapa adulta",
        "Centros diurnos centrados en dar una ocupación digna y significativa a través de talleres de producción artesanal y artística.",
        "Cerámica creativa, encuadernación, confección y costura, jardinería, artes gráficas, cocina autónoma y multideporte.",
        "Prioriza la satisfacción personal y el aprendizaje sensorial y manual por encima de cualquier exigencia de rendimiento cuantitativo.",
        "A través del circuito de plazas públicas de Servicios Sociales de la Comunidad de Madrid.",
        "Web Empleo: afanias.org/trabaja-con-nosotros\nEmail Selección: empleo@afanias.org",
        "C/ Isaac Peral, 1, Pozuelo de Alarcón / Av. Canillejas a Vicálvaro, Madrid",
        "91 512 01 00",
        "info@afanias.org\nhttps://afanias.org"
    ),
    (
        "Fundación Dan Zass (Talleres Expresivos)",
        "Formación Expresiva, Ocio Ocupacional y Artes Escénicas",
        "Privado / Tercer Sector (Asociación cultural sin ánimo de lucro)",
        "Personas con diversidad funcional física, intelectual o del desarrollo",
        "Alternativa artística y corporal a los cursos tradicionales, utilizando el movimiento y el cuerpo como canal de crecimiento.",
        "Danza inclusiva, expresión corporal, teatro gestual, psicomotricidad relacional, improvisación escénica y montajes.",
        "Estimula la mente, la disciplina, la memoria motriz y el trabajo colectivo desde un formato lúdico, físico y altamente motivador.",
        "Contacto directo por correo o teléfono; bienvenida adaptada para conocer las necesidades de la persona.",
        "Email directo Selección: asociacion.dan.zass@gmail.com (Asunto: 'CV - Docencia Danza / Terapia Ocupacional')",
        "C/ Manuel Galindo, 13, 28025 Madrid (Marqués de Vadillo)",
        "646 51 59 54",
        "asociacion.dan.zass@gmail.com\nhttps://danzass.com"
    ),
    (
        "Grupo AMÁS (Centros Ocupacionales Los Pinos y Suigé)",
        "Centros Ocupacionales y de Ajuste Personal",
        "Concertado / Tercer Sector (Red social del sur de Madrid)",
        "Personas con discapacidad intelectual (Leganés, Alcorcón, Móstoles)",
        "Inserción mediante talleres ocupacionales productivos vinculados al tejido asociativo y municipal de la zona sur.",
        "Montajes electrónicos ligeros, manipulado de paquetería, horticultura, lavandería industrial adaptada y desarrollo comunitario.",
        "Fomenta la convivencia y el sentido de utilidad social en la comunidad local sin exámenes teóricos desmotivantes.",
        "Gestión de plaza pública a través de Servicios Sociales de los municipios o la Comunidad de Madrid.",
        "Web Empleo: grupoamas.org/trabaja-con-nosotros\nEmail RRHH: seleccion@grupoamas.org",
        "Av. de la Libertad, 39, Alcorcón / C/ Pintor Ribera, 15, Leganés",
        "91 694 53 10",
        "info@grupoamas.org\nhttps://www.grupoamas.org"
    ),
    (
        "Fundación Raíles (Centros Ocupacionales)",
        "Centro Ocupacional y Apoyo a la Autonomía",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Discapacidad intelectual y personas con necesidades de apoyo extenso",
        "Habilitación ocupacional práctica, desarrollo de capacidades artísticas y participación ciudadana plena.",
        "Encuadernación artística, artesanía de reciclaje, cocina funcional, mantenimiento y autogestión de actividades diarias.",
        "Ambiente centrado en las preferencias individuales del usuario, favoreciendo un ritmo pausado sin exigencias academicistas.",
        "Derivación por la red pública de atención a la discapacidad de la CAM.",
        "Web Empleo: fundacionrailes.org\nEmail RRHH: rrhh@fundacionrailes.org",
        "C/ Eras, 15, 28043 Madrid (Hortaleza)",
        "91 388 02 81",
        "info@fundacionrailes.org\nhttps://fundacionrailes.org"
    )
]

col_widths_sheet1 = [28, 24, 25, 24, 34, 30, 32, 26, 32, 26, 16, 26]
format_sheet(ws1, "ALTERNATIVAS A LA FORMACIÓN TRADICIONAL Y CURSOS REGLADOS EN LA COMUNIDAD DE MADRID",
             "Centros ocupacionales, prelaborales y empleo con apoyo con datos de Titularidad y Vías de Envío de CV",
             headers_sheet1, data_sheet1, fill_sheet1, col_widths_sheet1)

# =============================================================
# SHEET 2: CO HABILIDADES SOCIALES Y TRATO
# =============================================================
ws2 = wb.create_sheet(title="CO Habilidades y Trato")
headers_sheet2 = [
    "Nombre del Centro Ocupacional (CO)",
    "Entidad Gestora / Tipo de Centro",
    "Titularidad (Público / Concertado / Privado)",
    "Perfil Atendido / Destinatarios",
    "Programa de Habilidades Sociales en el CO",
    "¿Cómo trabajan el 'Tratar con Gente' en los Talleres?",
    "Metodología Práctica y Dinámicas",
    "Objetivos Relacionales y de Convivencia",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Contacto"
]

data_sheet2 = [
    (
        "Centro Ocupacional Fundación Juan XXIII",
        "Centro Ocupacional y Campus de Inclusión Sociolaboral",
        "Concertado / Tercer Sector (Fundación de iniciativa social)",
        "Personas con discapacidad intelectual y del desarrollo en edad adulta",
        "Módulo de Habilidades Sociales y Trato al Público en Unidades Productivas",
        "Role-playing de atención a clientes y visitas, resolución de quejas, asambleas de convivencia y trato respetuoso entre compañeros de cadena productiva.",
        "Práctica en catering para eventos externos, comedor laboral y visitas guiadas al campus; simulaciones de situaciones de tensión y asertividad.",
        "Aprender a presentarse, modular el tono de voz, escuchar sin interrumpir, aceptar correcciones laborales y trabajar en equipo solidario.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Centro Ocupacional Montecarmelo (Fundación A LA PAR)",
        "Centro Ocupacional y Parque Inclusivo",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Discapacidad intelectual ligera y moderada con dificultades relacionales",
        "Programa de Habilidades Interpersonales y Atención al Cliente Abierto",
        "Los usuarios atienden diariamente a clientes reales que acuden al lavadero FundaCars o compran en la huerta, practicando el trato educado y directo.",
        "Atención al público en entorno real protegido: saludo cordial, recepción de vehículos, cobro en caja y resolución calmada de dudas de clientes.",
        "Superar la vergüenza, vencer la timidez frente a personas desconocidas y adquirir saber estar en entornos laborales normalizados.",
        "Web Empleo: alapar.ong/trabaja-con-nosotros\nEmail Selección: seleccion@alapar.ong / rrhh@alapar.ong",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid (Montecarmelo)",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional Concertado (Red Pública CAM)",
        "Concertado (Red Pública CAM / Gestión Fundación SER)",
        "Personas con discapacidad intelectual con timidez, fobia social o retraimiento",
        "Programa de Comunicación Interpersonal y Asambleas de Autogestores",
        "El programa de radio comunitaria 'Échale Papas' y las asambleas semanales son el eje para entrenar el diálogo, la escucha activa y la empatía.",
        "Talleres de debate donde no se puede interrumpir al compañero; entrevistas a invitados externos y dinámicas para pactar turnos y normas.",
        "Aprender a manifestar opiniones personales con educación, aceptar puntos de vista contrarios y perder el miedo a hablar ante otras personas.",
        "Email Selección: rrhh@fundacion-ser.org\nFormulario de empleo en web oficial: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46, 28008 Madrid (Argüelles)",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    ),
    (
        "Centro Ocupacional Las Fuentes / Hortaleza (Fundación Aprocor)",
        "Centro Ocupacional de Desarrollo Comunitario",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Personas con discapacidad intelectual y necesidades de apoyo social",
        "Programa de Habilidades Sociales en Entornos Naturales Comunitarios",
        "El aprendizaje de 'tratar con gente' se realiza en la calle y el barrio: cafeterías, transporte público, mercadillos y asociaciones vecinales.",
        "Cuadrillas de apoyo mutuo guiadas por mediadores; dinámicas para pedir en bares, preguntar direcciones y mantener conversaciones informales con vecinos.",
        "Construir relaciones de amistad reales fuera del centro cerrado y desenvolverse con autonomía y soltura ante desconocidos.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Vicente Morales, 5 / C/ Esteban Palacios, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Centro Ocupacional 3 Olivos (Down Madrid)",
        "Centro Ocupacional y Formación para la Vida Adulta",
        "Concertado / Tercer Sector (Fundación de utilidad pública)",
        "Jóvenes y adultos con síndrome de Down y discapacidad intelectual",
        "Programa de Asertividad, Inteligencia Emocional y Relaciones Interpersonales",
        "Enseñan habilidades explícitas de convivencia: modular el volumen de voz, respetar el espacio vital, evitar el contacto físico invasivo y saber decir 'no'.",
        "Talleres psicopedagógicos de educación afectiva, role-playing de resolución de conflictos entre compañeros y dinámicas de grupo de risoterapia.",
        "Adquirir pautas de cortesía indispensables para la inclusión laboral y aprender a construir relaciones de amistad y pareja sanas y respetuosas.",
        "Web Empleo: downmadrid.org/trabaja-con-nosotros\nEmail Selección: rrhh@downmadrid.org",
        "C/ Cueva de Montesinos, 45, 28034 Madrid (Fuencarral)",
        "91 387 67 90",
        "downmadrid@downmadrid.org\nhttps://downmadrid.org"
    ),
    (
        "Centro Ocupacional Colmenar Viejo (Grupo Envera)",
        "Centro Integral Ocupacional y de Habilitación",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Personas con discapacidad intelectual con dificultades de comunicación",
        "Programa de Mediación Social, Expresión y Habilidades de Relación",
        "A través de talleres compartidos de jardinería y la emisora Radio Terrícola, se entrena la espontaneidad, la sonrisa y la cercanía al interactuar.",
        "Los usuarios ejercen de periodistas entrevistando a visitantes y personalidades, lo que desinhibe el miedo social y fortalece la seguridad personal.",
        "Vencer el aislamiento y la timidez severa, aprender a presentarse y adquirir soltura conversacional en cualquier entorno.",
        "Web Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. Colmenar Viejo a Miraflores, Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    ),
    (
        "Centro Ocupacional Canillejas / Pozuelo (AFANIAS)",
        "Red de Centros Ocupacionales de Atención Diurna",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Personas con discapacidad intelectual en etapa adulta",
        "Taller de Ajuste Personal y Social: Convivencia y Regulación Relacional",
        "Abordan los conflictos de convivencia cotidianos: celos entre compañeros, tolerancia a la frustración, reparto de tareas y colaboración grupal.",
        "Dinámicas grupales de expresión de sentimientos guiadas por psicólogos y educadores; asambleas de taller para consensuar normas de convivencia.",
        "Aprender a pedir ayuda con amabilidad, dar las gracias, respetar el turno de palabra y controlar impulsos verbales en momentos de enfado.",
        "Web Empleo: afanias.org/trabaja-con-nosotros\nEmail Selección: empleo@afanias.org",
        "Av. de Canillejas a Vicálvaro, 82, 28022 Madrid / Pozuelo de Alarcón",
        "91 512 01 00",
        "info@afanias.org\nhttps://afanias.org"
    ),
    (
        "Centro Ocupacional Móstoles / Los Pinos (Grupo AMÁS)",
        "Centros Ocupacionales y de Ajuste Personal",
        "Concertado / Tercer Sector (Red social sur de Madrid)",
        "Personas con discapacidad intelectual del sur de Madrid",
        "Programa de Habilidades Sociales Comunitarias y Autogestión Relacional",
        "Entrenan la interacción social vinculada a los recursos del barrio (polideportivos, centros culturales, comercios) y la convivencia entre compañeros.",
        "Espacios de debate horizontal donde los propios usuarios votan decisiones de los talleres y aprenden a negociar y ceder ante posturas opuestas.",
        "Fomentar la madurez relacional, evitar el aislamiento social en el hogar y aprender a establecer límites personales claros y asertivos.",
        "Web Empleo: grupoamas.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoamas.org",
        "Av. de la Libertad, 39, Alcorcón / C/ Pintor Ribera, 15, Leganés",
        "91 694 53 10",
        "info@grupoamas.org\nhttps://www.grupoamas.org"
    ),
    (
        "Centro Ocupacional Valdelatas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Consejería de Familia, Juventud y Asuntos Sociales - CAM)",
        "Adultos con discapacidad intelectual con plaza pública de la CAM",
        "Área de Ajuste Personal y Social – Módulo de Relaciones Interpersonales",
        "Intervención sistemática individual y grupal para tratar el aislamiento, la timidez extrema y los problemas de relación interpersonal en talleres.",
        "Talleres semanales de habilidades sociales dirigidos por psicólogos y trabajadores sociales de la CAM; actividades de convivencia en comedor y transporte.",
        "Aprender a relacionarse sin agresividad ni sumisión, pedir las cosas por favor, resolver desacuerdos cotidianos y convivir en grupo amplio.",
        "Canal Empleo Público: Bolsas de trabajo y oposiciones de personal laboral de la Comunidad de Madrid (comunidad.madrid/servicios/empleo)",
        "Ctra. Colmenar Viejo, Km 15, 28108 Alcobendas / Madrid",
        "91 653 43 00",
        "https://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Barajas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Comunidad de Madrid)",
        "Personas con discapacidad intelectual en régimen diurno",
        "Módulo de Entrenamiento en Competencias Sociales y Comunicación",
        "Se trabaja la conversación cotidiana: iniciar una charla informal, mantener el contacto visual, saber escuchar y despedirse de forma correcta.",
        "Role-playing de situaciones cotidianas (hacer una compra, acudir al médico, hablar con un compañero de ruta); dinámicas de grupo de cohesión.",
        "Reducir la ansiedad ante situaciones sociales novedosas y fomentar un trato educado y autónomo con la comunidad.",
        "Canal Empleo Público: Procesos selectivos y listas de contratación temporal de la CAM (comunidad.madrid)",
        "C/ Playa de Riazor, 12, 28042 Madrid (Barajas)",
        "91 741 08 00",
        "https://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Marcelino Camacho / Ángel de la Guarda (APANID)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado / Tercer Sector (Asociación APANID)",
        "Personas con discapacidad intelectual y necesidades de apoyo extenso",
        "Programa de Ajuste Social y Habilidades de Relación Adaptadas",
        "Foco en la comunicación funcional y el trato respetuoso no verbal: respetar el espacio del compañero, sonreír, pedir objetos sin quitarlos.",
        "Mediación conductual positiva durante tareas de taller manipulativo; apoyo emocional individualizado ante crisis de ansiedad relacional.",
        "Aprender a tolerar la presencia de otros compañeros sin frustración y construir lazos de afecto y compañerismo en el centro.",
        "Email Selección: rrhh@apanid.es / apanid@apanid.es\nWeb: apanid.es",
        "Camino del Prado s/n, 28905 Getafe, Madrid",
        "91 683 88 11",
        "apanid@apanid.es\nhttps://www.apanid.es"
    ),
    (
        "Centro Ocupacional Cíclope (Fundación Raíles)",
        "Centro Ocupacional de Habilitación y Participación",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Adultos con discapacidad intelectual y dificultades de integración",
        "Taller de Habilidades para la Vida en Comunidad y Trato Social",
        "Trabajan la asertividad y la cortesía en tareas reales: trato con proveedores de materiales, visitas a bibliotecas y compras del taller.",
        "Asambleas diarias de acogida para hablar de cómo se siente cada uno; dinámicas de trabajo cooperativo donde el éxito depende de colaborar.",
        "Sentirse miembros valiosos de un grupo, aprender a empatizar con el compañero que tiene un mal día y tratar a todos con consideración.",
        "Web Empleo: fundacionrailes.org\nEmail RRHH: rrhh@fundacionrailes.org",
        "C/ Eras, 15, 28043 Madrid (Hortaleza)",
        "91 388 02 81",
        "info@fundacionrailes.org\nhttps://fundacionrailes.org"
    )
]

col_widths_sheet2 = [28, 24, 25, 24, 32, 36, 32, 32, 32, 26, 16, 26]
format_sheet(ws2, "CENTROS OCUPACIONALES QUE TRATAN HABILIDADES SOCIALES Y TRATO CON PERSONAS",
             "Centros Ocupacionales (CO) con programas específicos de asertividad, convivencia y trato con gente en talleres y comunidad",
             headers_sheet2, data_sheet2, fill_sheet2, col_widths_sheet2)

# =============================================================
# SHEET 3: CO BUEN AMBIENTE Y TRATO HUMANO
# =============================================================
ws3 = wb.create_sheet(title="CO Buen Ambiente y Trato")
headers_sheet3 = [
    "Nombre del Centro Ocupacional (CO)",
    "Entidad Gestora / Tipo de Centro",
    "Titularidad (Público / Concertado / Privado)",
    "Valoración / Reputación de Familias",
    "¿Por qué destacan las opiniones sobre el Buen Ambiente?",
    "¿Cómo inciden en el trato respetuoso y humano con personas?",
    "Atmósfera y Clima del Centro Ocupacional",
    "Puntos Fuertes Destacados por Familias y Usuarios",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Contacto"
]

data_sheet3 = [
    (
        "Centro Ocupacional Montecarmelo (Fundación A LA PAR)",
        "Centro Ocupacional y Parque Inclusivo",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "★★★★☆ (4.5/5 en valoraciones)",
        "Reseñas de empleados y visitantes destacan una filosofía 'distendida, de gran compañerismo y cultura alegre' en un entorno de parque natural.",
        "Se enseña a tratar a compañeros y clientes con educación, cortesía y sonrisa en el lavadero FundaCars y huerta. La dignidad del usuario es primordial.",
        "Familiar, laborioso, optimista y rodeado de amplias zonas verdes que transmiten paz.",
        "La convivencia normalizada con público externo en talleres productivos abiertos genera un ambiente libre de estigmas y lleno de vitalidad.",
        "Web Empleo: alapar.ong/trabaja-con-nosotros\nEmail Selección: seleccion@alapar.ong",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid (Montecarmelo)",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Centro Ocupacional Fundación Juan XXIII",
        "Centro Ocupacional y Campus Inclusivo",
        "Concertado / Tercer Sector (Fundación social)",
        "★★★★☆ (4.4/5 en plataformas de empleo)",
        "Las opiniones de familias y trabajadores alaban 'el gran ambiente humano, el compañerismo y el orgullo de pertenencia' de los profesionales.",
        "Fomentan activamente el apoyo mutuo en las líneas de trabajo: los usuarios más autónomos cuidan y apoyan a quienes tienen mayores dificultades.",
        "Profesional pero profundamente humano, solidario, diverso y muy activo.",
        "Más de 60 años de experiencia; proyectos de catering y eventos donde los usuarios atienden con simpatía y educación, reforzando su don de gentes.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado (Red Pública CAM / Fundación SER)",
        "★★★★☆ (Alta estima comunitaria)",
        "Reconocido por su ambiente distendido y participativo, especialmente visible en sus talleres creativos y su proyecto radiofónico sin presiones.",
        "A través de su programa de radio 'Échale Papas' y asambleas grupales, entrenan la escucha atenta, no interrumpir y tratar con cariño al compañero.",
        "Creativo, asambleario, acogedor y enfocado en la libre expresión.",
        "El programa de radio ha recibido cobertura en RTVE ('De Seda y Hierro') y es elogiado como modelo de buen rollo y compañerismo sincero.",
        "Email Selección: rrhh@fundacion-ser.org\nWeb: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46, 28008 Madrid",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    ),
    (
        "Centro Ocupacional Las Fuentes / Hortaleza (Fundación Aprocor)",
        "Centro Ocupacional y Espacio de Inclusión",
        "Concertado / Tercer Sector (Sello Madrid Excelente)",
        "★★★★☆ (4.3/5 en portales laborales)",
        "Trabajadores y usuarios coinciden en calificarlo de 'ambiente joven, dinámico, muy humano y gratificante'. Familias destacan la alegría de los chicos.",
        "Aplican la Planificación Centrada en la Persona: no imponen normas rígidas; enseñan a convivir mediante el diálogo cordial y asambleas horizontales.",
        "Abierto, dinámico, comunitario y fuertemente conectado con la naturaleza y el vecindario.",
        "Espacios abiertos como El Huerto y Begonia's Garden donde personas con discapacidad interactúan con vecinos y clientes con cercanía y amabilidad.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Vicente Morales, 5 / C/ Frómista, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Centro Ocupacional 3 Olivos (Down Madrid)",
        "Centro Ocupacional y Formación Integral",
        "Concertado / Tercer Sector (Fundación de utilidad pública)",
        "★★★★★ (Máximo reconocimiento familiar)",
        "Familias y empresas colaboradoras destacan que se respira un clima de 'dignidad, entusiasmo y afecto'. Resaltan cómo cada alumno se siente querido y capaz.",
        "Metodología basada en la inteligencia emocional y la risoterapia. Se entrena exhaustivamente la simpatía, el saludo cordial y el saber agradecer.",
        "Entusiasta, estimulante, respetuoso y muy cálido.",
        "Instalaciones modernas adaptadas a la accesibilidad cognitiva; talleres de risoterapia y habilidades relacionales de primer nivel.",
        "Web Empleo: downmadrid.org/trabaja-con-nosotros\nEmail RRHH: rrhh@downmadrid.org",
        "C/ Cueva de Montesinos, 45, 28034 Madrid",
        "91 387 67 90",
        "downmadrid@downmadrid.org\nhttps://downmadrid.org"
    ),
    (
        "Centro Ocupacional Colmenar Viejo (Grupo Envera)",
        "Centro Integral de Discapacidad y Ocupacional",
        "Concertado / Tercer Sector (Asociación de familias de Iberia)",
        "★★★★☆ (4.2/5 en opiniones y gran arraigo)",
        "Nacida del asociacionismo de padres de Iberia, se percibe un ambiente de 'gran familia'. Familias destacan el compromiso de por vida con los usuarios.",
        "A través de Radio Terrícola y actividades compartidas, los usuarios aprenden a conversar con visitantes sin timidez, tratando a todos con cercanía.",
        "Familiar, comunitario, campestre (rodeado de naturaleza) y muy activo.",
        "El entorno natural en Colmenar Viejo favorece un clima libre de estrés urbano, ideal para personas con sensibilidad o ansiedad social.",
        "Web Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. Colmenar a Miraflores Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    ),
    (
        "Centro Ocupacional Canillejas (AFANIAS)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "★★★★☆ (Alta fidelidad y satisfacción de familias)",
        "Familias destacan la paciencia infinita y vocación de los educadores, resaltando que los usuarios asisten contentos y motivados cada día.",
        "En los talleres artesanales (cerámica, encuadernación) se cultiva el refuerzo positivo mutuo, el elogio al esfuerzo del compañero y la solidaridad.",
        "Tranquilo, vocacional, paciente y enriquecedor.",
        "Dedicación personalizada de los profesionales que conocen en profundidad la historia y necesidades afectivas de cada persona atendida.",
        "Web Empleo: afanias.org/trabaja-con-nosotros\nEmail Selección: empleo@afanias.org",
        "Av. de Canillejas a Vicálvaro, 82, 28022 Madrid",
        "91 512 01 00",
        "info@afanias.org\nhttps://afanias.org"
    ),
    (
        "Centro Ocupacional Móstoles / Los Pinos (Grupo AMÁS)",
        "Centros Ocupacionales de la Red Social Sur",
        "Concertado / Tercer Sector (Red social sur de Madrid)",
        "★★★★☆ (Gran reconocimiento comunitario)",
        "Gran cercanía barrial en Móstoles y Alcorcón; familias destacan el trato accesible y sin barreras de los monitores y trabajadores sociales.",
        "Modelo de apoyo conductual positivo: se refuerzan las conductas de amabilidad y cuidado entre compañeros, desterrando actitudes sancionadoras.",
        "Cercano, popular, participativo y muy arraigado al barrio.",
        "Fuerte implicación en las fiestas, mercados y eventos de la localidad, favoreciendo que los usuarios se sientan queridos por su comunidad.",
        "Web Empleo: grupoamas.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoamas.org",
        "C/ Pintor Ribera, 15, Leganés / Av. Libertad, Alcorcón",
        "91 694 53 10",
        "info@grupoamas.org\nhttps://www.grupoamas.org"
    ),
    (
        "Centro Ocupacional Nazaret (Fundación Nazaret)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "★★★★★ (Elogiado por familias con necesidades extensas)",
        "Familias de personas con grandes necesidades de apoyo destacan el trato dulce, humano y respetuoso que reciben sus hijos.",
        "Se incide minuciosamente en el tono de voz calmado, la mirada afectuosa y la acogida personalizada para transmitir seguridad emocional a cada persona.",
        "Afectuoso, sereno, muy protector y acogedor.",
        "Atención a personas con pluridiscapacidad donde el cariño y el respeto a la dignidad individual marcan la pauta de cada jornada.",
        "Email Selección: seleccion@fundacionnazaret.org\nWeb: fundacionnazaret.org",
        "Av. de los Almendros, s/n, 28522 Rivas-Vaciamadrid / Madrid",
        "91 499 04 20",
        "nazaret@fundacionnazaret.org\nhttps://fundacionnazaret.org"
    ),
    (
        "Centro Ocupacional Cíclope (Fundación Raíles)",
        "Centro Ocupacional de Habilitación y Ajuste",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "★★★★☆ (Ambiente familiar muy valorado)",
        "Familias alaban el ambiente íntimo y sin prisas, donde no existe la presión productiva agresiva y se respeta escrupulosamente el ritmo de cada uno.",
        "Asambleas de taller donde cada usuario expresa cómo se siente antes de iniciar las tareas, enseñando a escuchar con empatía y cuidar al compañero.",
        "Familiar, pausado, respetuoso y solidario.",
        "El tamaño a escala humana del centro facilita que todos los profesionales y usuarios se conozcan estrechamente, generando vínculos casi de hermandad.",
        "Web Empleo: fundacionrailes.org\nEmail RRHH: rrhh@fundacionrailes.org",
        "C/ Eras, 15, 28043 Madrid (Hortaleza)",
        "91 388 02 81",
        "info@fundacionrailes.org\nhttps://fundacionrailes.org"
    ),
    (
        "Centro Ocupacional Marcelino Camacho (APANID)",
        "Centro Ocupacional Especializado de Getafe",
        "Concertado / Tercer Sector (Asociación APANID)",
        "★★★★☆ (Trayectoria histórica reconocida)",
        "Familias de Getafe y municipios del sur resaltan el compromiso vocacional y la dedicación constante de los profesionales hacia los usuarios.",
        "Enfoque en la humanización del trato cotidiano: amabilidad, cercanía física respetuosa y fomento del compañerismo en comidas y talleres.",
        "Comunitario, arraigado, protector y con ambiente de convivencia festiva.",
        "Celebración de jornadas de convivencia, festivales y encuentros de familias que consolidan un sentimiento de comunidad de apoyo mutuo.",
        "Email Selección: rrhh@apanid.es\nWeb: apanid.es",
        "Camino del Prado s/n, 28905 Getafe, Madrid",
        "91 683 88 11",
        "apanid@apanid.es\nhttps://www.apanid.es"
    ),
    (
        "Centro Ocupacional Valdelatas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Consejería de Asuntos Sociales - CAM)",
        "★★★★☆ (Centro público de referencia)",
        "Instalaciones amplias y ajardinadas; valorado por la estabilidad de su plantilla pública y su clima estructurado y sereno.",
        "Normas claras de convivencia positiva que educan en el respeto mutuo, la resolución pacífica de diferencias y el trato cívico y educado.",
        "Espacioso, ordenado, seguro y rodeado de naturaleza.",
        "Amplios jardines y paseos arbolados que permiten pasear y relajarse durante los descansos, favoreciendo un clima libre de tensiones.",
        "Canal Empleo Público: Convocatorias de la CAM en comunidad.madrid/servicios/empleo",
        "Ctra. Colmenar Viejo, Km 15, 28108 Alcobendas / Madrid",
        "91 653 43 00",
        "https://www.comunidad.madrid"
    )
]

col_widths_sheet3 = [28, 25, 25, 20, 36, 36, 28, 34, 32, 26, 16, 26]
format_sheet(ws3, "CENTROS OCUPACIONALES DESTACADOS POR BUEN AMBIENTE Y TRATO HUMANO",
             "Centros Ocupacionales (CO) con las mejores valoraciones de familias por su clima afectivo, cercanía y respeto humano",
             headers_sheet3, data_sheet3, fill_sheet3, col_widths_sheet3)

# =============================================================
# SHEET 4: CO MEDICINA E INFORMÁTICA
# =============================================================
ws4 = wb.create_sheet(title="CO Medicina e Informática")
headers_sheet4 = [
    "Nombre del Centro Ocupacional (CO)",
    "Entidad Gestora / Tipo de Centro",
    "Titularidad (Público / Concertado / Privado)",
    "Personal Médico Especializado",
    "Personal Informático / Técnico TIC",
    "Áreas de Trabajo Conjunto (Medicina + Informática en el CO)",
    "Tecnologías, Software y Equipamiento Adaptado",
    "Perfil de Usuarios en Talleres",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Contacto"
]

data_sheet4 = [
    (
        "Centro Ocupacional Fundación Juan XXIII",
        "Centro Ocupacional y Campus de Inclusión Sociolaboral",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Servicio médico permanente en el centro (médico general/laboral y enfermería DUE).",
        "Equipo de Soluciones Digitales, analistas informáticos y técnicos formadores en TIC adaptadas y digitalización.",
        "Supervisión médica de la salud postural y fatiga visual en talleres de digitalización; adaptación ergonómica de puestos informáticos.",
        "Puestos informáticos con lectores de pantalla, escáneres documentales de alta producción, pantallas táctiles y software de gestión adaptado.",
        "Personas con discapacidad intelectual y del desarrollo con itinerario de capacitación tecnológica.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Centro Ocupacional Montecarmelo (Fundación A LA PAR)",
        "Centro Ocupacional y Talleres de Habilitación",
        "Concertado / Tercer Sector (Fundación de iniciativa social)",
        "Servicio médico propio de atención continuada y enfermería permanente (DUE).",
        "Técnicos de nuevas tecnologías, instructores de diseño digital, impresión 3D y soporte de sistemas.",
        "Adaptación médica de interfaces táctiles y conmutadores según el diagnóstico motor y neurológico del usuario.",
        "Impresoras 3D adaptadas, ordenadores con ratones ergonómicos de bola, pulsadores de acceso y pantallas interactivas.",
        "Personas con discapacidad intelectual ligera o moderada con necesidades de apoyo intermitente.",
        "Web Empleo: alapar.ong/trabaja-con-nosotros\nEmail Selección: seleccion@alapar.ong / rrhh@alapar.ong",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Centro Ocupacional Colmenar Viejo (Grupo Envera)",
        "Centro Integral de Discapacidad y Ocupacional",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Servicio médico de centro, fisioterapeutas de ajuste y diplomados en enfermería (DUE).",
        "Técnicos de radiodifusión digital, administradores informáticos y formadores de alfabetización tecnológica.",
        "Control médico y terapéutico de niveles de estrés y medicación durante la grabación en radio y talleres de informática.",
        "Consolas de sonido accesibles de Radio Terrícola, software de edición digital, ordenadores adaptados con magnificadores.",
        "Adultos con discapacidad intelectual y pluridiscapacidad en talleres de comunicación y ofimática.",
        "Web Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. Colmenar a Miraflores, Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    ),
    (
        "Centro Ocupacional Marcelino Camacho / Ángel de la Guarda (APANID)",
        "Centro Ocupacional Especializado de Gran Capacidad",
        "Concertado / Tercer Sector (Asociación APANID Getafe)",
        "Servicio médico continuado con médicos de atención primaria/rehabilitadora y equipo de enfermería.",
        "Técnicos de soporte informático de la entidad y dinamizadores de aulas TIC y robótica adaptada.",
        "Protocolos de atención sanitaria y ergonómica para usuarios con afectación motora severa en el uso de ordenadores.",
        "Aulas informáticas multimedia con trackballs, teclados de teclas gigantes con carcasas guía y pantallas táctiles.",
        "Personas con discapacidad intelectual y necesidades de apoyo extenso o generalizado.",
        "Email Selección: rrhh@apanid.es / apanid@apanid.es\nWeb oficial: apanid.es",
        "Camino del Prado s/n, 28905 Getafe, Madrid",
        "91 683 88 11",
        "apanid@apanid.es\nhttps://www.apanid.es"
    ),
    (
        "Centro Ocupacional Canillejas / Pozuelo (AFANIAS)",
        "Red de Centros Ocupacionales de Atención Diurna",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Médicos de centro y diplomados universitarios en enfermería (DUE) asignados al centro.",
        "Técnicos de taller de nuevas tecnologías, instructores de diseño multimedia y formadores TIC.",
        "Prescripción médica y seguimiento de adaptaciones biomecánicas para prevenir contracturas en el aula digital.",
        "Pizarras digitales interactivas, software de estimulación cognitiva adaptado, ratones por conmutador y tabletas accesibles.",
        "Jóvenes y adultos con discapacidad intelectual con interés en adquirir destrezas digitales de comunicación.",
        "Web Empleo: afanias.org/trabaja-con-nosotros\nEmail Selección: empleo@afanias.org",
        "Av. de Canillejas a Vicálvaro, 82, 28022 Madrid / Pozuelo de Alarcón",
        "91 512 01 00",
        "info@afanias.org\nhttps://afanias.org"
    ),
    (
        "Centro Ocupacional Las Fuentes / Hortaleza (Fundación Aprocor)",
        "Centro Ocupacional y Espacio de Inclusión",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Servicio de salud y apoyo conductual con médico/psiquiatra consultor y enfermería.",
        "Técnicos del Área TIC y especialistas en Accesibilidad Cognitiva Digital de la Fundación.",
        "Evaluación interdisciplinar de capacidades sanitarias y cognitivas para el manejo de aplicaciones móviles y ordenadores en el entorno comunitario.",
        "Aplicaciones móviles adaptadas a lectura fácil, agendas visuales digitales, tabletas con síntesis de voz y ordenadores adaptados.",
        "Personas con discapacidad intelectual y del desarrollo orientadas a la inclusión sociocomunitaria.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Vicente Morales, 5 / C/ Esteban Palacios, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Centro Ocupacional Valdelatas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Consejería de Familia, Juventud y Asuntos Sociales - CAM)",
        "Médico de centro oficial de la Comunidad de Madrid y equipo de enfermería (DUE).",
        "Técnicos informáticos de la Dirección General de Atención a Personas con Discapacidad (CAM).",
        "Supervisión médica de tratamientos farmacológicos y adaptación técnica del equipamiento del aula de informática ocupacional.",
        "Puestos informáticos adaptados con software de accesibilidad, pulsadores y periféricos del Programa ALBOR.",
        "Personas adultas con discapacidad intelectual con plaza pública de la Comunidad de Madrid.",
        "Canal Empleo Público: Bolsas de trabajo y oposiciones de personal laboral de la Comunidad de Madrid (comunidad.madrid/servicios/empleo)",
        "Ctra. Colmenar Viejo, Km 15, 28108 Alcobendas / Madrid",
        "91 653 43 00",
        "https://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Barajas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Comunidad de Madrid)",
        "Servicio médico propio de centro y diplomados en enfermería.",
        "Técnicos de informática de la administración pública autonómica asignados al soporte del centro.",
        "Coordinación médico-técnica para la accesibilidad física y cognitiva en el uso de las tecnologías del centro ocupacional.",
        "Equipos informáticos con teclados accesibles, lupas de pantalla, software adaptado y conexión segura de la CAM.",
        "Usuarios con discapacidad intelectual de la zona este y norte de Madrid capital.",
        "Canal Empleo Público: Procesos selectivos y listas de contratación temporal de la CAM (comunidad.madrid)",
        "C/ Playa de Riazor, 12, 28042 Madrid (Barajas)",
        "91 741 08 00",
        "https://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Móstoles / Los Pinos (Grupo AMÁS)",
        "Centros Ocupacionales de Formación y Ajuste",
        "Concertado / Tercer Sector (Red social del sur de Madrid)",
        "Servicio médico de centro y enfermería en coordinación con centros de salud de referencia.",
        "Técnicos informáticos de la entidad y dinamizadores de talleres de informática accesible.",
        "Adaptación de tareas informáticas según la medicación y grado de movilidad articular de los usuarios.",
        "Puestos con ratones de bola, teclados con contraste visual, software ofimático adaptado y tabletas táctiles.",
        "Personas con discapacidad intelectual del sur de Madrid (Móstoles, Alcorcón, Leganés).",
        "Web Empleo: grupoamas.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoamas.org",
        "Av. de la Libertad, 39, Alcorcón / C/ Pintor Ribera, 15, Leganés",
        "91 694 53 10",
        "info@grupoamas.org\nhttps://www.grupoamas.org"
    ),
    (
        "Centro Ocupacional Ciudad Residencial Sonsoles (ATAM)",
        "Centro Ocupacional y Complejo Residencial Sociosanitario",
        "Concertado / Tercer Sector (ATAM - Telefónica)",
        "Equipo médico multidisciplinar propio (médicos generales, rehabilitadores y enfermería permanente).",
        "Ingenieros informáticos y de telecomunicaciones del departamento tecnológico y de I+D de ATAM.",
        "Desarrollo e integración de tecnología asistencial con supervisión médica continua para promover la autonomía en talleres ocupacionales.",
        "Sistemas de teleasistencia inteligente, sensores ergonómicos, pulsadores adaptados y software propio de accesibilidad.",
        "Personas con discapacidad intelectual y física vinculadas a programas integrales de habilitación.",
        "Web Empleo: atam.es/empleo\nEmail Selección: rrhh@atam.es",
        "C/ Via de las Dos Castillas, 33, 28224 Pozuelo de Alarcón, Madrid",
        "91 709 80 00",
        "atam@atam.es\nhttps://atam.es"
    ),
    (
        "Centro Ocupacional Nazaret (Fundación Nazaret)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Servicio médico de centro y enfermería.",
        "Técnicos de aula multimedia e informática adaptada.",
        "Planificación individualizada que aúna las necesidades sanitarias con la estimulación cognitiva a través de la tecnología.",
        "Pantallas táctiles interactivas, ratones de emulación por barbilla o cabeza, software de estimulación sensorial.",
        "Personas con discapacidad intelectual moderada y severa.",
        "Email Selección: seleccion@fundacionnazaret.org\nWeb: fundacionnazaret.org",
        "Av. de los Almendros, s/n, 28522 Rivas-Vaciamadrid / Madrid",
        "91 499 04 20",
        "nazaret@fundacionnazaret.org\nhttps://fundacionnazaret.org"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado (Red Pública CAM / Gestión Fundación SER)",
        "Servicio de atención médico-sanitaria concertada y enfermería.",
        "Técnicos de producción sonora, podcast y aula de estimulación informática.",
        "Cuidado de la fatiga vocal y postural durante las sesiones de radio digital y talleres informáticos.",
        "Equipos de sonido digital adaptados, software sonoro accesible, ordenadores con periféricos ergonómicos.",
        "Personas con discapacidad intelectual en talleres de comunicación, prensa y estimulación digital.",
        "Email Selección: rrhh@fundacion-ser.org\nWeb: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46, 28008 Madrid",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    )
]

col_widths_sheet4 = [28, 24, 25, 26, 26, 34, 34, 26, 34, 26, 16, 26]
format_sheet(ws4, "CENTROS OCUPACIONALES CON PERSONAL ESPECIALIZADO EN MEDICINA E INFORMÁTICA",
             "Centros Ocupacionales (CO) con Servicio Médico y Departamentos Técnicos de Informática / TIC Adaptadas",
             headers_sheet4, data_sheet4, fill_sheet4, col_widths_sheet4)

# =============================================================
# SHEET 5: CO LINUX Y SOFTWARE LIBRE
# =============================================================
ws5 = wb.create_sheet(title="CO Linux y Software Libre")
headers_sheet5 = [
    "Nombre del Centro Ocupacional (CO)",
    "Entidad Gestora / Tipo de Centro",
    "Titularidad (Público / Concertado / Privado)",
    "Uso Específico de Linux y Software Libre en el CO",
    "Distribuciones GNU/Linux y Software Libre Utilizado",
    "¿Cómo beneficia el Software Libre a los Usuarios del CO?",
    "Talleres Ocupacionales que Emplean Software Libre",
    "Proyectos Libres Destacados en el Centro",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Enlace al Proyecto"
]

data_sheet5 = [
    (
        "Centro Ocupacional Valdelatas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Consejería de Familia, Juventud y Asuntos Sociales - CAM)",
        "Implantación de la distribución oficial 'MAX' (MAdrid_linuX) y herramientas de accesibilidad libre en el aula informática.",
        "MAX GNU/Linux (versiones 11/12 basadas en Ubuntu), lector de pantalla Orca, teclado virtual Caribou, Dasher, LibreOffice.",
        "Permite que los usuarios accedan a puestos informáticos estables, sin costes de licencias privativas y con herramientas adaptadas de por vida.",
        "Taller de alfabetización digital básica, navegación web accesible, redacción de documentos y correspondencia ocupacional.",
        "Integración del Programa ALBOR (Acceso Libre de Barreras al Ordenador) con adaptaciones libres de software educativo.",
        "Canal Empleo Público: Bolsas de contratación temporal y oposiciones de personal laboral de la CAM (comunidad.madrid/servicios/empleo)",
        "Ctra. Colmenar Viejo, Km 15, 28108 Alcobendas / Madrid",
        "91 653 43 00",
        "https://max.educa.madrid.org\nhttps://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Barajas (CAM)",
        "Centro Ocupacional Público de la Comunidad de Madrid",
        "Público Autonómico (Comunidad de Madrid)",
        "Aulas de informática ocupacional configuradas con MAX Linux y paquetes de accesibilidad del entorno MATE/GNOME.",
        "MAX Linux, suite ofimática LibreOffice, navegador Firefox adaptado con extensiones de lectura fácil, KMouth/eSpeak.",
        "Facilita un entorno digital libre de virus y de distracciones publicitarias comerciales, adaptado al ritmo cognitivo de cada persona.",
        "Taller de prensa y boletín ocupacional interno, diseño de horarios en tablas ofimáticas libres y búsqueda de recursos locales.",
        "Adaptación de periféricos especiales bajo controladores libres de Linux (pulsadores USB y pantallas táctiles).",
        "Canal Empleo Público: Procesos selectivos y bolsas de empleo de la CAM en comunidad.madrid",
        "C/ Playa de Riazor, 12, 28042 Madrid (Barajas)",
        "91 741 08 00",
        "https://max.educa.madrid.org\nhttps://www.comunidad.madrid"
    ),
    (
        "Centro Ocupacional Colmenar Viejo (Grupo Envera)",
        "Centro Integral Ocupacional y de Habilitación",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Uso intensivo de software libre de edición y procesado de sonido para la producción de su emisora comunitaria 'Radio Terrícola'.",
        "Audacity (editor de audio libre multiplataforma), reproductores y conversores multimedia abiertos VLC, LibreOffice.",
        "Los usuarios aprenden a cortar, montar y editar sus propias entrevistas radiofónicas usando un programa libre que pueden tener gratis en sus casas.",
        "Taller ocupacional de Radio Terrícola, taller de redacción de guiones de entrevistas y locución digital comunitaria.",
        "Producción de podcasts en formatos de audio libres accesibles emitidos en internet por personas con discapacidad intelectual.",
        "Web Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. Colmenar Viejo a Miraflores, Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    ),
    (
        "Centro Ocupacional Fundación Juan XXIII",
        "Centro Ocupacional y Campus de Inclusión Sociolaboral",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Puestos de reacondicionamiento informático donde instalan distribuciones GNU/Linux y software libre en talleres de digitalización.",
        "Distribuciones Linux Ubuntu y Linux Mint, LibreOffice, GIMP (diseño gráfico libre), gestores de bases de datos de código abierto.",
        "Capacita a los usuarios en tareas reales de ofimática y formateo técnico, mejorando su empleabilidad en empresas que usan código abierto.",
        "Taller de digitalización documental, escaneo masivo, clasificación de datos y taller ocupacional de reciclaje de hardware informático.",
        "Recuperación y puesta a punto de ordenadores donados mediante la instalación de sistemas operativos libres GNU/Linux.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Centro Ocupacional Montecarmelo (Fundación A LA PAR)",
        "Centro Ocupacional y Talleres Productivos",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Uso de herramientas de diseño y laminado 3D libres en sus talleres de reprografía, etiquetado y producción artesanal.",
        "Inkscape (diseño vectorial libre), GIMP, Cura/PrusaSlicer (software libre de impresión 3D), LibreOffice.",
        "Permite el diseño y personalización de cartelería, vinilos y piezas artesanales sin depender de costosas licencias propietarias.",
        "Taller ocupacional de imprenta y reprografía, taller de corte y diseño digital, etiquetado de productos de huerta y artesanía.",
        "Modelado de accesorios y productos de apoyo impresos en 3D bajo licencias Creative Commons de código abierto.",
        "Web Empleo: alapar.ong/trabaja-con-nosotros\nEmail Selección: seleccion@alapar.ong",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado (Red Pública CAM / Fundación SER)",
        "Implementación de comunicadores aumentativos libres y software libre de edición sonora para el programa de radio 'Échale Papas'.",
        "Suite libre ARASAAC / AraWord, Audacity, comunicadores de código abierto Cboard y AsTeRICS Grid.",
        "Garantiza que usuarios no verbales o con dificultades de lectoescritura participen en igualdad de condiciones en guiones y debates.",
        "Taller de radio comunitaria inclusiva 'Échale Papas', asamblea ocupacional de usuarios y taller de estimulación digital.",
        "Elaboración de escaletas y guiones de radio adaptados con pictogramas de licencia libre Creative Commons de ARASAAC.",
        "Email Selección: rrhh@fundacion-ser.org\nWeb: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46, 28008 Madrid",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    ),
    (
        "Centro Ocupacional Las Fuentes / Hortaleza (Fundación Aprocor)",
        "Centro Ocupacional y Espacio de Inclusión",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Uso de herramientas de accesibilidad cognitiva abiertas y sistemas aumentativos libres en talleres ocupacionales y comunitarios.",
        "Pictogramas libres de ARASAAC (CC BY-NC-SA), comunicador web libre Cboard, navegador Mozilla Firefox accesible.",
        "Proporciona herramientas de comunicación alternativas gratuitas que los usuarios pueden llevar en sus teléfonos sin pagar licencias.",
        "Taller de jardinería comunitaria (El Huerto de Aprocor), preparación de recetas en cocina ocupacional y señalización comunitaria.",
        "Creación de guías de tareas y calendarios en lectura fácil apoyados con software de pictogramas de código abierto.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Vicente Morales, 5 / C/ Esteban Palacios, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Centro Ocupacional Canillejas (AFANIAS)",
        "Centro Ocupacional de Habilitación y Ajuste",
        "Concertado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Uso de software libre para la comunicación aumentativa, expresión escrita y tableros interactivos.",
        "Plaphoons (comunicador dinámico libre para personas con discapacidad motriz), AraWord, LibreOffice Writer adaptado.",
        "Permite que personas con dificultades en el habla construyan frases mediante barrido o pulsador con un software libre y modificable.",
        "Taller ocupacional de comunicación y expresión, taller de creación de cuentos visuales y actividades de ajuste social.",
        "Tableros de comunicación personalizados basados en Plaphoons adaptados a las necesidades motrices de cada usuario.",
        "Web Empleo: afanias.org/trabaja-con-nosotros\nEmail Selección: empleo@afanias.org",
        "Av. de Canillejas a Vicálvaro, 82, 28022 Madrid",
        "91 512 01 00",
        "info@afanias.org\nhttps://afanias.org"
    ),
    (
        "Centro Ocupacional Cíclope (Fundación Raíles)",
        "Centro Ocupacional de Capacitación y Autonomía",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Taller de reacondicionamiento informático e instalación de distribuciones Linux ligeras en equipos reutilizados.",
        "Lubuntu, Xubuntu, Linux Mint, utilidades de formateo y diagnóstico de hardware libre (GParted, Memtest86).",
        "Los usuarios adquieren habilidades manuales y lógicas de ensamblaje, instalación de sistemas operativos y reutilización ecológica.",
        "Taller ocupacional de informática verde, reciclaje de componentes electrónicos y mantenimiento de equipos.",
        "Proyecto de donación de ordenadores recuperados con GNU/Linux para familias de personas con discapacidad del distrito de Hortaleza.",
        "Web Empleo: fundacionrailes.org\nEmail RRHH: rrhh@fundacionrailes.org",
        "C/ Eras, 15, 28043 Madrid (Hortaleza)",
        "91 388 02 81",
        "info@fundacionrailes.org\nhttps://fundacionrailes.org"
    ),
    (
        "Centro Ocupacional Ciudad Residencial Sonsoles (ATAM)",
        "Centro Ocupacional y Residencial Sociosanitario",
        "Concertado / Tercer Sector (ATAM - Telefónica)",
        "Sistemas de domótica accesible y control de entornos ocupacionales basados en servidores y protocolos libres.",
        "GNU/Linux Debian en servidores locales, Home Assistant de código abierto, protocolos abiertos MQTT, comunicadores libres.",
        "Permite que los usuarios controlen puertas, luces y persianas de los talleres ocupacionales desde sus sillas mediante software abierto.",
        "Taller de autonomía en el hogar, control de entornos accesibles y actividades ocupacionales de la vida diaria.",
        "Desarrollo de módulos de control de entorno accesibles bajo hardware abierto (Arduino/ESP32) y software libre.",
        "Web Empleo: atam.es/empleo\nEmail Selección: rrhh@atam.es",
        "C/ Via de las Dos Castillas, 33, 28224 Pozuelo de Alarcón, Madrid",
        "91 709 80 00",
        "atam@atam.es\nhttps://atam.es"
    ),
    (
        "Centro Ocupacional Móstoles (Grupo AMÁS)",
        "Centro Ocupacional y de Ajuste Personal",
        "Concertado / Tercer Sector (Red social sur de Madrid)",
        "Aulas de capacitación informática ocupacional equipadas con software educativo libre y herramientas ofimáticas abiertas.",
        "LibreOffice, AraWord, teclado en pantalla Onboard, suite educativa interactiva GCompris (código abierto).",
        "Entrena la coordinación ojo-mano, la discriminación visual y la mecanografía a través de juegos interactivos libres sin coste.",
        "Taller de estimulación cognitiva digital, taller de mecanografía y competencias básicas de oficina.",
        "Guías didácticas adaptadas para el manejo autónomo de herramientas ofimáticas libres en el puesto de trabajo.",
        "Web Empleo: grupoamas.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoamas.org",
        "C/ Pintor Ribera, 15, Leganés / C/ Pintor Velázquez, Móstoles",
        "91 694 53 10",
        "info@grupoamas.org\nhttps://www.grupoamas.org"
    ),
    (
        "Centro Ocupacional Nazaret (Fundación Nazaret)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Uso de comunicadores web de código abierto y plataformas interactivas libres en el aula multimedia.",
        "AsTeRICS Grid (comunicador web libre multiplataforma), Plaphoons, AraWord, navegadores de código abierto.",
        "Ofrece a los usuarios un sistema de comunicación aumentativa que funciona tanto en ordenadores del taller como en sus tabletas personales.",
        "Taller de estimulación multimedia, taller de expresión comunicativa y asambleas de autogestores.",
        "Plantillas de comunicación personalizadas de código abierto exportables para su uso en el hogar de las familias.",
        "Email Selección: seleccion@fundacionnazaret.org\nWeb: fundacionnazaret.org",
        "Av. de los Almendros, s/n, 28522 Rivas-Vaciamadrid / Madrid",
        "91 499 04 20",
        "nazaret@fundacionnazaret.org\nhttps://fundacionnazaret.org"
    )
]

col_widths_sheet5 = [28, 24, 25, 30, 32, 34, 26, 32, 34, 26, 16, 26]
format_sheet(ws5, "CENTROS OCUPACIONALES QUE USAN LINUX Y SOFTWARE LIBRE EN LA COMUNIDAD DE MADRID",
             "Centros Ocupacionales (CO) que implementan GNU/Linux, MAX y herramientas de código abierto en sus talleres",
             headers_sheet5, data_sheet5, fill_sheet5, col_widths_sheet5)

output_path = "/home/bender/Descargas/Recursos_Discapacidad_Comunidad_de_Madrid.xlsx"
wb.save(output_path)
print(f"Successfully generated final updated workbook: {output_path}")

