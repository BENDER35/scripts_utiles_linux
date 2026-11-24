import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

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

# Helper function to style sheets
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
            elif col_idx in [3, len(row_data) - 2]: # Titularidad or Teléfono
                c.alignment = align_center
            else:
                c.alignment = align_left

    last_col_letter = openpyxl.utils.get_column_letter(len(headers))
    ws.auto_filter.ref = f"A5:{last_col_letter}{row_idx}"
    ws.freeze_panes = "A6"
    
    for col_idx, width in enumerate(col_widths, 1):
        letter = openpyxl.utils.get_column_letter(col_idx)
        ws.column_dimensions[letter].width = width

# =============================================================
# SHEET 0: INTRODUCCIÓN Y GUÍA
# =============================================================
ws0 = wb.active
ws0.title = "Guía y Canales de Acceso"
ws0.views.sheetView[0].showGridLines = True

ws0.cell(row=2, column=2, value="GUÍA INTEGRAL DE RECURSOS PARA PERSONAS CON DISCAPACIDAD - COMUNIDAD DE MADRID").font = title_font
ws0.cell(row=3, column=2, value="Directorio completo con filtros de Titularidad (Público/Privado/Concertado) y Canales de Envío de CV para Empleo").font = subtitle_font

guide_content = [
    ("1. Vías de Acceso a Recursos Públicos en la CAM",
     "• Grado de Discapacidad: Trámite obligatorio (>= 33%) ante los Centros Base de la Comunidad de Madrid.\n"
     "• AMAPAD: Agencia Madrileña para el Apoyo a las Personas Adultas con Discapacidad (apoyo jurídico y social).\n"
     "• Servicios Sociales Municipales: Tramitación de plazas públicas en Centros Ocupacionales y de Día mediante la Ley de Dependencia.\n"
     "• Centros de Salud Mental (CSM): Puerta médica obligatoria para derivación a la Red de Atención Social a Personas con Enfermedad Mental (CRPS/CRL)."),
    
    ("2. Titularidad: ¿Público (Estado/CAM), Concertado o Privado?",
     "• Público Estatal / Autonómico / Municipal: Dispositivos de titularidad directa del Estado (Imserso), de la Comunidad de Madrid (SERMAS/Consejería de Asuntos Sociales) o Ayuntamientos. El acceso al empleo se realiza mediante Procesos Selectivos, Oposiciones Oficiales o Bolsas de Empleo Temporal del SERMAS o la Administración.\n"
     "• Concertado / Tercer Sector: Centros de titularidad privada sin ánimo de lucro (fundaciones y asociaciones) financiados total o parcialmente con plazas públicas de la Comunidad de Madrid. El envío de CV se realiza de forma directa a sus Departamentos de Selección / RRHH.\n"
     "• Privado Sanitario / Libre: Centros y empresas que operan con contratación directa y admisión privada o con convenios específicos."),

    ("3. Cómo Trabajar en el Sector de la Discapacidad en Madrid",
     "En cada una de las hojas de este archivo se incluye una columna específica con el canal exacto para enviar el currículum:\n"
     "• En entidades sociales y fundaciones: Se detalla el portal de empleo propio ('Trabaja con nosotros') o el buzón de correo de RRHH.\n"
     "• En hospitales públicos y centros estatales: Se indican los enlaces a las Bolsas Oficiales de Trabajo del SERMAS, Fundaciones de Investigación Biomédica o el INAP/Portal del Ciudadano estatal.")
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
# SHEET 2: HABILIDADES SOCIALES Y TRATO
# =============================================================
ws2 = wb.create_sheet(title="Habilidades Sociales y Trato")
headers_sheet2 = [
    "Nombre del Centro / Entidad",
    "Tipo de Dispositivo / Programa",
    "Titularidad (Público / Concertado / Privado)",
    "Perfil Atendido / Diagnóstico",
    "Programa Específico de Habilidades Sociales",
    "¿Cómo trabajan el 'Tratar con Gente'?",
    "Metodología y Formato",
    "Objetivos Terapéuticos Clave",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Contacto"
]

data_sheet2 = [
    (
        "Asociación Asperger Madrid",
        "Asociación Especializada en Neurodiversidad",
        "Privado / Tercer Sector (Asociación de Utilidad Pública)",
        "Personas con Síndrome de Asperger / TEA Nivel 1 (adolescentes, jóvenes y adultos)",
        "Grupos de Entrenamiento en Habilidades Sociales (EHS) y Talleres de Conversación",
        "Entrenan la decodificación de señales no verbales, dobles sentidos, silencios, cómo iniciar y mantener una charla informal (small talk) y modular el contacto visual.",
        "Grupos de iguales de 6 a 8 personas guiados por psicólogos especializados; role-playing, análisis de vídeos y salidas supervisadas a bares, cines y eventos.",
        "Superar el aislamiento social, hacer amigos, aprender a decir 'no' (asertividad), resolver desacuerdos y comprender códigos sociales implícitos.",
        "Email Selección: info@aspergermadrid.org (Asunto: 'CV - Psicología / Área Social / Ocio')\nWeb: aspergermadrid.eu",
        "C/ Bohonal, 15-17, 28053 Madrid (Puente de Vallecas)",
        "91 786 27 28",
        "info@aspergermadrid.org\nhttps://aspergermadrid.eu"
    ),
    (
        "Red de Centros de Rehabilitación Psicosocial - CRPS (CAM)",
        "Dispositivos Públicos de Salud Mental",
        "Público Autonómico (Red Pública CAM / Gestión concertada)",
        "Personas con problemas graves de salud mental, fobia social, aislamiento o psicosis",
        "Módulos Grupales Intensivos de Entrenamiento en Habilidades Sociales y Autonomía",
        "Trabajan específicamente la pérdida del miedo a interactuar con desconocidos, hablar en público, pedir ayuda, realizar trámites cotidianos y mantener relaciones de afecto.",
        "Sesiones grupales semanales con terapeutas ocupacionales, psicólogos y educadores sociales; tareas para casa en entornos reales comunitarios.",
        "Reconectar con el entorno social, reducir la ansiedad interpersonal, aprender a regular emociones frente a otros y reconstruir la red de apoyo social.",
        "Canal CV: A través de los portales de empleo de las entidades adjudicatarias gestoras: grupo5.net/empleo, intress.org/empleo, hospitalarias.es/empleo, fundacionmanantial.org",
        "Centros en Chamartín, Retiro, Latina, Arganzuela, Leganés, Alcalá, Móstoles, etc.",
        "CSM de distrito",
        "https://www.comunidad.madrid"
    ),
    (
        "Clubes Sociales de Salud Mental (CAM / Intress / Manantial)",
        "Espacios Comunitarios de Socialización y Ocio",
        "Público Autonómico (Red de Asuntos Sociales CAM / Gestión ONG)",
        "Personas con dificultades de relación interpersonal y salud mental duradera",
        "Talleres de Encuentro, Club de Ocio y Dinamización de Redes Relacionales",
        "El club funciona como un laboratorio social seguro: los usuarios aprenden a charlar de manera relajada, participar en asambleas, proponer planes y convivir sin sentirse juzgados.",
        "Formato distendido de club social guiado por monitores y educadores; tardes entre semana y fines de semana; meriendas, debates y salidas grupales.",
        "Romper la soledad no deseada, practicar el trato cercano con personas de forma natural y crear vínculos de amistad duraderos.",
        "Canal CV: A través de los portales de selección de las entidades que operan los clubes: intress.org/trabaja-con-nosotros y fundacionmanantial.org/trabaja-con-nosotros",
        "Sedes en Retiro, Hortaleza, Fuencarral, Fuenlabrada, etc. (Comunidad de Madrid)",
        "91 371 72 12",
        "https://www.fundacionmanantial.org"
    ),
    (
        "ALUSAMEN (Asociación en Lucha por la Salud Mental)",
        "Asociación Psicosocial y Club de Ocio",
        "Privado / Tercer Sector (Asociación sin ánimo de lucro)",
        "Personas adultas con dificultades psicosociales, timidez extrema o soledad",
        "Talleres de Habilidades Sociales, Tertulias y Grupo de Autoayuda Mutua",
        "Trabajan la expresión de vivencias personales, la escucha activa, la empatía hacia el compañero y la eliminación de la vergüenza al hablar frente a otros.",
        "Talleres semanales de 1h30m, grupos de conversación, salidas de ocio los fines de semana acompañadas por voluntariado formado y profesionales.",
        "Aprender a relacionarse sin temor al rechazo social, compartir experiencias comunes y recuperar la capacidad de disfrutar del trato humano.",
        "Email Selección: alusamen1990@yahoo.es (Asunto: 'Candidatura de Empleo / Voluntariado Profesional')\nAtención presencial",
        "C/ de Peña Gorbea, 4, 28053 Madrid (Vallecas)",
        "91 477 18 66",
        "alusamen1990@yahoo.es\nhttps://alusamen.org.es"
    ),
    (
        "Fundación Capacis (Área de Habilidades Sociales)",
        "Programa Específico para Inteligencia Límite",
        "Privado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Jóvenes y adultos jóvenes con Inteligencia Límite y discapacidad intelectual ligera",
        "Taller de Inteligencia Social, Asertividad y Relaciones Interpersonales",
        "Diseñado a medida para personas que sufren 'invisibilidad social': se entrenan dilemas morales, relaciones de pareja, evitar situaciones de abuso o engaño y comunicarse en el trabajo.",
        "Talleres teórico-prácticos vivenciales, análisis de situaciones cotidianas, dinámicas de role-playing y actividades de ocio compartido fuera del aula.",
        "Saber cómo tratar a jefes, compañeros de trabajo y amigos; fijar límites personales claros y defender sus derechos de forma asertiva.",
        "Email Selección: capacis@fundacioncapacis.org (Perfiles de educadores sociales, psicólogos y preparadores laborales)\nWeb: fundacioncapacis.org",
        "C/ Agustín de Iturbide, 14, 28043 Madrid (Hortaleza)",
        "91 931 34 48",
        "capacis@fundacioncapacis.org\nhttps://www.fundacioncapacis.org"
    ),
    (
        "Down Madrid (Servicio de Ocio y Habilidades Sociales)",
        "Servicio de Desarrollo Personal y Relacional",
        "Concertado / Tercer Sector (Fundación de utilidad pública)",
        "Personas con síndrome de Down y discapacidad intelectual",
        "Programa de Educación Afectivo-Sexual, Habilidades Sociales y Resolución de Conflictos",
        "Enseñan habilidades de trato interpersonal respetuoso, modulación de la voz, respeto del espacio personal del otro, cortesía, asertividad y comprensión de límites afectivos.",
        "Grupos de edad homogéneos guiados por mediadores; salidas dinámicas a la ciudad (cafeterías, tiendas, museos) para aplicar las destrezas 'in situ'.",
        "Desarrollar relaciones de amistad y pareja sanas, aprender a interactuar de forma educada y segura con desconocidos y en entornos laborales.",
        "Web Empleo: downmadrid.org/trabaja-con-nosotros\nEmail Selección: rrhh@downmadrid.org",
        "C/ Cueva de Montesinos, 45, 28034 Madrid",
        "91 387 67 90",
        "downmadrid@downmadrid.org\nhttps://downmadrid.org"
    ),
    (
        "Fundación Aprocor (Servicio de Ocio y Redes Comunitarias)",
        "Programa de Dinamización Social Comunitaria",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "Personas con discapacidad intelectual y del desarrollo",
        "Programa de Mediación Social, Convivencia y Desarrollo de Redes de Amistad",
        "El entrenamiento se realiza en 'entornos naturales' (el barrio, transporte público, terrazas, asociaciones vecinales), huyendo del aula cerrada para practicar la interacción real.",
        "Apoyos personalizados y cuadrillas de amigos; los profesionales actúan como facilitadores discretos que intervienen solo para orientar la dinámica social.",
        "Crear amistades reales fuera de los centros cerrados, aprender a negociar planes con iguales y desenvolverse en la comunidad con soltura.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Frómista, 13, 28050 Madrid (Las Tablas)",
        "91 843 77 72",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "AMAFE (Asociación de Amigos y Familiares Esquizofrenia)",
        "Asociación de Salud Mental y Apoyo Mutuo",
        "Privado / Tercer Sector (Asociación de Utilidad Pública)",
        "Personas con esquizofrenia o psicosis que presentan retraimiento social",
        "Talleres de Habilidades Relacionales, Club de Ocio y Expresión Emocional",
        "Trabajan la reconexión con el entorno, la gestión de la desconfianza interpersonal en las interacciones y el fomento de conversaciones gratificantes.",
        "Talleres semanales de 1h30 guiados por psicólogos; actividades de club de ocio autogestionado con respaldo técnico.",
        "Recuperar el deseo y la confianza para relacionarse con personas, regular el estrés social y fomentar la autoeficacia relacional.",
        "Email Selección: info@amafe.org (Asunto: 'CV - Selección Profesionales Área Psicosocial')\nWeb: amafe.org",
        "C/ General Aranaz, 31, 28027 Madrid (Ciudad Lineal)",
        "91 361 27 68",
        "info@amafe.org\nhttps://www.amafe.org"
    ),
    (
        "Asociación PAUTA (Área de Personas con TEA)",
        "Entidad Especializada en Espectro Autista",
        "Concertado / Tercer Sector (Asociación de familias)",
        "Personas con TEA con diferentes niveles de necesidad de apoyo",
        "Programas de Comunicación Social, Habilidades de Interacción y Ocio Adaptado",
        "Utilizan sistemas de comunicación aumentativa, historias sociales y guías visuales para enseñar las pautas básicas de interacción humana, turnos de palabra y empatía.",
        "Intervenciones individuales y en pequeño grupo estructurado; uso de agendas visuales y apoyo conductual positivo.",
        "Comprender las intenciones de los demás, expresar deseos y emociones sin frustración y tolerar los cambios en dinámicas grupales.",
        "Web Empleo: asociacionpauta.org/trabaja-con-nosotros\nEmail Selección: rrhh@asociacionpauta.org",
        "C/ Juana Doña, 4, 28022 Madrid (San Blas - Canillejas)",
        "91 743 08 26",
        "pauta@asociacionpauta.org\nhttps://asociacionpauta.org"
    ),
    (
        "Centros Municipales de Salud Comunitaria - CMSc (Ayto Madrid)",
        "Red Municipal de Salud Comunitaria y Promoción",
        "Público Municipal (Ayuntamiento de Madrid - Madrid Salud)",
        "Población general y personas con dificultades de adaptación social o aislamiento",
        "Talleres Grupales Gratuitos de 'Habilidades para la Vida' y Bienestar Emocional",
        "Módulos formativos basados en las 10 Habilidades para la Vida de la OMS: comunicación asertiva, empatía, manejo de emociones y tensiones, y relaciones interpersonales.",
        "Ciclos de 8 a 10 sesiones grupales impartidas por psicólogos clínicos y trabajadores sociales de Madrid Salud en cada distrito.",
        "Entrenamiento práctico y accesible en habilidades sociales básicas sin coste económico y en el propio barrio de residencia.",
        "Canal Empleo Público: Bolsas de trabajo temporal y oposiciones del Ayuntamiento de Madrid en madrid.es/empleopublico y convocatorias de Madrid Salud",
        "Centros en todos los distritos de Madrid (Arganzuela, Centro, Tetuán, Vallecas, Latina...)",
        "010 (Línea Ayto)",
        "https://madridsalud.es"
    ),
    (
        "Fundación Dan Zass (Danza Inclusiva)",
        "Pedagogía Inclusiva y Terapia Corporal",
        "Privado / Tercer Sector (Asociación cultural sin ánimo de lucro)",
        "Personas con diversidad funcional y dificultades de contacto social o timidez",
        "Talleres de Psicomotricidad Relacional, Contact Improvisation y Danza Inclusiva",
        "El trato con el otro se trabaja a través del cuerpo antes que con la palabra: contacto físico respetuoso, sincronización, miradas, confianza ciega y escucha motriz.",
        "Sesiones semanales de danza-teatro e improvisación en grupo guiadas por coreógrafos y terapeutas corporales especializados.",
        "Desbloquear el miedo al rechazo físico y social, mejorar la autoestima y generar un sentimiento inmediato de pertenencia al grupo.",
        "Email directo Selección: asociacion.dan.zass@gmail.com (Asunto: 'Candidatura de Empleo / Formación')",
        "C/ Manuel Galindo, 13, 28025 Madrid",
        "646 51 59 54",
        "asociacion.dan.zass@gmail.com\nhttps://danzass.com"
    )
]

col_widths_sheet2 = [28, 24, 25, 24, 30, 36, 30, 30, 32, 26, 16, 26]
format_sheet(ws2, "CENTROS Y ASOCIACIONES QUE TRATAN PROBLEMAS DE HABILIDADES SOCIALES Y TRATO CON PERSONAS",
             "Entidades especializadas en asertividad y socialización con datos de Titularidad y Canales de Envío de CV",
             headers_sheet2, data_sheet2, fill_sheet2, col_widths_sheet2)

# =============================================================
# SHEET 3: CENTROS CON BUEN AMBIENTE
# =============================================================
ws3 = wb.create_sheet(title="Centros con Buen Ambiente")
headers_sheet3 = [
    "Nombre del Centro / Entidad",
    "Tipo de Centro y Especialidad",
    "Titularidad (Público / Concertado / Privado)",
    "Valoración / Reputación",
    "¿Por qué destacan las opiniones sobre el Buen Ambiente?",
    "¿Cómo inciden en el trato con personas?",
    "Atmósfera y Clima",
    "Puntos Fuertes según Familias",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono",
    "Web / Contacto"
]

data_sheet3 = [
    (
        "Fundación Capacis",
        "Centro de Formación e Inserción para Inteligencia Límite",
        "Privado / Tercer Sector (Fundación sin ánimo de lucro)",
        "★★★★★ (Excelente satisfacción familiar)",
        "Los testimonios destacan una 'calidad humana excepcional'. Se describe un ambiente donde los alumnos se sienten queridos, valorados y comprendidos tras años de incomprensión.",
        "Se incide diariamente en la empatía, el respeto a la diversidad de ritmos, la resolución calmada de desacuerdos y la asertividad sin gritos ni presiones. Enseñan a tratar desde la amabilidad.",
        "Cálido, protector pero motivador, libre de etiquetas y con una cercanía casi familiar.",
        "El equipo directivo y docente mantiene una tutoría constante con las familias y un seguimiento afectivo individualizado que cambia vidas.",
        "Email Selección: capacis@fundacioncapacis.org (Asunto: 'CV - Selección')\nContacto web: fundacioncapacis.org",
        "C/ Agustín de Iturbide, 14, 28043 Madrid (Hortaleza)",
        "91 931 34 48",
        "capacis@fundacioncapacis.org\nhttps://www.fundacioncapacis.org"
    ),
    (
        "Fundación Aprocor (Espacio Inclusión / El Huerto)",
        "Centros Ocupacionales y Desarrollo Comunitario",
        "Concertado / Tercer Sector (Sello Madrid Excelente)",
        "★★★★☆ (4.3/5 en portales laborales)",
        "Trabajadores y usuarios coinciden en calificarlo de 'ambiente joven, dinámico, muy humano y gratificante'. Familias destacan la alegría contagiosa de los usuarios.",
        "Aplican la 'Planificación Centrada en la Persona'. No imponen normas rígidas; enseñan a convivir mediante asambleas participativas donde cada voz cuenta.",
        "Abierto, dinámico, comunitario y fuertemente conectado con la naturaleza y el vecindario.",
        "Espacios abiertos como El Huerto y Begonia's Garden donde personas con discapacidad interactúan con vecinos y clientes de forma totalmente normalizada.",
        "Web Empleo: fundacionaprocor.org\nEmail RRHH: rrhh@fundacionaprocor.org",
        "C/ Vicente Morales, 5 / C/ Frómista, 13, 28043 Madrid",
        "91 388 63 67",
        "comunicacion@fundacionaprocor.org\nhttps://fundacionaprocor.org"
    ),
    (
        "Asociación Dan Zass (Danza Inclusiva)",
        "Compañía y Escuela de Expresión y Danza Inclusiva",
        "Privado / Tercer Sector (Asociación cultural sin ánimo de lucro)",
        "★★★★★ (Reconocimiento unánime en el sector)",
        "Las reseñas de alumnos y familias subrayan la 'acogida con los brazos abiertos', la alegría de las clases y la ausencia de prejuicios. Personas con timidez se vuelven sociables.",
        "El trato humano se enseña a través del tacto, la mirada y el contacto corporal respetuoso. Los profesores transmiten que toda persona es un artista valioso.",
        "Extremadamente alegre, desinhibido, cariñoso, vital y lleno de energía positiva.",
        "Protocolo de bienvenida personalizado con fotos de los espacios y monitores antes de empezar para evitar cualquier ansiedad o estrés por lo nuevo.",
        "Email directo Selección: asociacion.dan.zass@gmail.com (Asunto: 'CV Docente / Monitor')",
        "C/ Manuel Galindo, 13, 28025 Madrid (Carabanchel)",
        "646 51 59 54",
        "asociacion.dan.zass@gmail.com\nhttps://danzass.com"
    ),
    (
        "Fundación A LA PAR (Montecarmelo)",
        "Centro Ocupacional y Parque Inclusivo",
        "Concertado / Tercer Sector (Fundación sin ánimo de lucro)",
        "★★★★☆ (4.5/5 en Indeed y portales)",
        "Reseñas de empleados y visitantes destacan una filosofía 'distendida, de gran compañerismo y cultura alegre'. Se valora el ambiente de parque abierto rodeado de verde.",
        "En los talleres (huerto, carpintería, lavado de coches) se enseña a tratar a compañeros y clientes con educación, cortesía y sonrisa.",
        "Familiar, laborioso, optimista y rodeado de amplias zonas verdes que transmiten paz.",
        "La integración de negocios abiertos al público general (como FundaCars o su huerta) permite practicar el trato con gente real a diario en un ambiente protegido.",
        "Web Empleo: alapar.ong/trabaja-con-nosotros\nEmail RRHH: seleccion@alapar.ong",
        "C/ Monasterio de las Huelgas, 15, 28049 Madrid",
        "91 735 57 90",
        "informacion@alapar.ong\nhttps://alapar.ong"
    ),
    (
        "Fundación Juan XXIII (Vicálvaro)",
        "Centro Ocupacional e Inclusión Sociolaboral",
        "Concertado / Tercer Sector (Fundación social)",
        "★★★★☆ (4.4/5 en plataformas de empleo)",
        "Las opiniones de empleados y familias alaban 'el gran ambiente humano, el compañerismo y el orgullo de pertenencia'. Se destaca el compromiso vocacional de los monitores.",
        "Se trabaja profundamente el compañerismo en equipo en unidades de catering y manipulados. Fomentan el apoyo mutuo: los más autónomos ayudan a quienes más lo necesitan.",
        "Profesional pero profundamente humano, solidario, diverso y muy activo.",
        "Más de 60 años de experiencia; proyectos donde los usuarios atienden eventos externos, reforzando su saber estar y don de gentes.",
        "Web Empleo: fundacionjuanxxiii.org/trabaja-con-nosotros\nEmail Selección: seleccion@fundacionjuanxxiii.org",
        "Av. Gran Vía del Este, 1, 28032 Madrid (Vicálvaro)",
        "91 413 73 49",
        "comunicacion@fundacionjuanxxiii.org\nhttps://www.fundacionjuanxxiii.org"
    ),
    (
        "Down Madrid (Centro 3 Olivos)",
        "Centro Ocupacional y Formación Integral",
        "Concertado / Tercer Sector (Fundación de utilidad pública)",
        "★★★★★ (Máximo reconocimiento familiar y social)",
        "Familias y empresas destacan que se respira un clima de 'dignidad, entusiasmo y afecto'. Resaltan la profesionalidad del personal y cómo logran que cada alumno se sienta capaz y feliz.",
        "Metodología basada en la inteligencia emocional y la risoterapia. Se entrena exhaustivamente la simpatía, el saludo cordial, escuchar antes de contestar y saber agradecer con educación.",
        "Entusiasta, estimulante, respetuoso y muy cálido.",
        "Instalaciones modernas adaptadas a la accesibilidad cognitiva y lectura fácil; talleres de risoterapia y habilidades relacionales de primer nivel.",
        "Web Empleo: downmadrid.org/trabaja-con-nosotros\nEmail RRHH: rrhh@downmadrid.org",
        "C/ Cueva de Montesinos, 45, 28034 Madrid",
        "91 387 67 90",
        "downmadrid@downmadrid.org\nhttps://downmadrid.org"
    ),
    (
        "Centro Ocupacional Pintor Rosales (Fundación SER)",
        "Centro Ocupacional de Atención Diurna",
        "Concertado (Red Pública CAM / Gestión Fundación SER)",
        "★★★★☆ (Alta estima comunitaria)",
        "Reconocido por su ambiente distendido y participativo, especialmente visible en sus talleres creativos y su proyecto radiofónico. Los usuarios se sienten escuchados y protagonistas.",
        "A través de su programa de radio 'Échale Papas' y asambleas grupales, entrenan la escucha atenta, no interrumpir al compañero, respetar opiniones divergentes y tratar con soltura.",
        "Creativo, asambleario, acogedor y enfocado en la libre expresión.",
        "El programa de radio ha recibido cobertura en RTVE ('De Seda y Hierro') y es elogiado como modelo de empoderamiento comunicativo y buen rollo entre los participantes.",
        "Email Selección: rrhh@fundacion-ser.org\nWeb: fundacion-ser.org",
        "Paseo del Pintor Rosales, 46, 28008 Madrid",
        "91 533 57 94",
        "fundacionser@fundacion-ser.org\nhttps://fundacion-ser.org"
    ),
    (
        "ALUSAMEN (Vallecas)",
        "Asociación de Salud Mental y Club Social",
        "Privado / Tercer Sector (Asociación sin ánimo de lucro)",
        "★★★★★ (Referente de cercanía y apoyo mutuo)",
        "Los usuarios la describen como 'un salvavidas' y 'una segunda familia'. Resaltan que es de los pocos sitios donde no existe el estigma hacia los problemas mentales y se puede hablar tranquilos.",
        "La base de la entidad es el apoyo mutuo horizontal. Nadie juzga a nadie. Los coordinadores enseñan con paciencia a volver a hablar, sonreír, sentarse en grupo y pedir las cosas con agrado.",
        "Tranquilo, sin prisas, íntimo, familiar y profundamente empático.",
        "Acceso directo y sin trabas administrativas para quien se siente solo y necesita un entorno cálido donde empezar a salir del aislamiento.",
        "Email Selección: alusamen1990@yahoo.es\nContacto presencial en su sede de Vallecas",
        "C/ de Peña Gorbea, 4, 28053 Madrid",
        "91 477 18 66",
        "alusamen1990@yahoo.es\nhttps://alusamen.org.es"
    ),
    (
        "Asociación Asperger Madrid",
        "Entidad de Familias y Personas con Asperger/TEA",
        "Privado / Tercer Sector (Asociación de Utilidad Pública)",
        "★★★★☆ (Muy valorada por adultos y familias)",
        "Muchos adultos y jóvenes con Asperger afirman en sus testimonios que entrar en la asociación fue 'el primer lugar donde encajé en mi vida'. El ambiente de respeto genera un enorme alivio.",
        "Los psicólogos enseñan explícitamente las reglas de cortesía y convivencia que a menudo las personas neurotípicas dan por sentadas, permitiendo relacionarse sin angustia.",
        "Seguro, honesto, libre de burlas, comprensivo y estructurado.",
        "Grupos de ocio donde pueden hablar de sus temas de interés con compañeros que comparten pasiones, favoreciendo amistades profundas y auténticas.",
        "Email Selección: info@aspergermadrid.org\nWeb: aspergermadrid.eu",
        "C/ Bohonal, 15-17, 28053 Madrid",
        "91 786 27 28",
        "info@aspergermadrid.org\nhttps://aspergermadrid.eu"
    ),
    (
        "Grupo Envera (Centro Integral Colmenar Viejo)",
        "Centro Integral de Discapacidad y Ocupacional",
        "Concertado / Tercer Sector (Asociación de familias de Iberia)",
        "★★★★☆ (4.2/5 en opiniones y gran arraigo)",
        "Nacida del asociacionismo de padres y empleados de Iberia, se percibe un ambiente de 'gran familia'. Familias destacan el compromiso de por vida con los usuarios y el cariño en el cuidado.",
        "A través de la emisora Radio Terrícola y actividades compartidas, los usuarios aprenden a conversar con periodistas, políticos y visitantes sin timidez, tratando a todos con cercanía.",
        "Familiar, comunitario, campestre (rodeado de naturaleza) y muy activo.",
        "El entorno natural en Colmenar Viejo favorece un clima libre de estrés urbano, ideal para personas con sensibilidad o ansiedad social.",
        "Web Empleo: grupoenvera.org/trabaja-con-nosotros\nEmail Selección: seleccion@grupoenvera.org",
        "Ctra. Colmenar a Miraflores Km 33,6, 28770 Colmenar Viejo",
        "91 846 34 43",
        "info@grupoenvera.org\nhttps://grupoenvera.org"
    )
]

col_widths_sheet3 = [28, 25, 25, 20, 36, 36, 28, 34, 32, 26, 16, 26]
format_sheet(ws3, "CENTROS DESTACADOS POR OPINIONES FAVORABLES, BUEN AMBIENTE Y ENFOQUE EN EL TRATO HUMANO",
             "Selección de centros con excelente clima humano con datos de Titularidad y Canales de Envío de CV",
             headers_sheet3, data_sheet3, fill_sheet3, col_widths_sheet3)

# =============================================================
# SHEET 4: MEDICINA E INFORMÁTICA
# =============================================================
ws4 = wb.create_sheet(title="Medicina e Informática")
headers_sheet4 = [
    "Nombre del Centro / Institución",
    "Tipo de Dispositivo / Ámbito",
    "Titularidad (Público / Concertado / Privado)",
    "Perfil Médico Especializado",
    "Perfil Informático / Tecnológico",
    "Áreas de Cooperación Medicina + Informática",
    "Tecnologías, Software y Robótica Médica Utilizada",
    "Perfil de Pacientes Atendidos",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Contacto"
]

data_sheet4 = [
    (
        "CEAPAT - IMSERSO (Centro Estatal Autonomía Personal)",
        "Centro de Referencia Estatal de Accesibilidad",
        "Público Estatal (Ministerio de Derechos Sociales / IMSERSO - Estado)",
        "Médicos especialistas en rehabilitación física, terapeutas ocupacionales, psicólogos clínicos.",
        "Ingenieros informáticos, ingenieros industriales, desarrolladores de accesibilidad digital y técnicos TIC.",
        "Diseño, prescripción y adaptación de productos de apoyo informáticos; evaluación médica ergonómica de interfaces digitales; peritaje y catálogo estatal.",
        "Sistemas de seguimiento ocular (Eye-tracking), emuladores de ratón por software, comunicadores aumentativos, conmutadores biomédicos y software de lectura.",
        "Personas con todo tipo de discapacidad motora, sensorial, cognitiva o personas mayores con dependencia.",
        "Canal Empleo Público: Oposiciones y bolsas de interinos del Estado a través del INAP (administracion.gob.es) y convocatorias oficiales de personal laboral del IMSERSO",
        "C/ Los Extremeños, 1, 28018 Madrid (Vallecas)",
        "91 703 31 00",
        "ceapat@imserso.es\nhttps://ceapat.imserso.es"
    ),
    (
        "Hospital Beata María Ana - Red Menni Daño Cerebral",
        "Hospital de Neurorrehabilitación y Daño Cerebral",
        "Concertado / Privado sin ánimo de lucro (Hermanas Hospitalarias)",
        "Médicos rehabilitadores, neurólogos, neurofisiólogos clínicos, psiquiatras.",
        "Ingenieros biomédicos, analistas de sistemas clínicos, técnicos de robótica médica y desarrolladores de telerrehabilitación.",
        "Tratamiento intensivo neuromotor guiado por software biomecánico; prescripción médica de programas robóticos personalizados para brazo, mano y marcha.",
        "Robótica avanzada (Armeo, Amadeo, Pablo), plataformas Balance Tutor/TYMO, neuromodulación (TMS/tDCS), plataformas cognitivas NeuronUP y realidad virtual.",
        "Adultos y niños con daño cerebral adquirido (ictus, TCE, anoxias) y patologías neurológicas complejas.",
        "Web Empleo: hospitalarias.es/empleo\nEmail RRHH: rrhh@hospitalbeata.org / hospital@hospitalbeata.org",
        "C/ del Doctor Esquerdo, 83, 28007 Madrid",
        "91 573 20 22",
        "hospital@hospitalbeata.org\nhttps://fundacionhospitalariasmadrid.org"
    ),
    (
        "Hospital Infantil Universitario Niño Jesús (Unidad Robótica)",
        "Hospital Pediátrico Público / Unidad de Biomecánica y Robótica",
        "Público Autonómico (Servicio Madrileño de Salud - SERMAS / CAM)",
        "Médicos pediatras rehabilitadores, cirujanos ortopédicos infantiles, neuropediatras.",
        "Ingenieros informáticos clínicos, bioingenieros especializados en marcha patológica, programadores de robótica social e IA.",
        "Neurorrehabilitación pediátrica mediante exoesqueletos biónicos e inteligencia artificial; análisis cuantitativo 3D del movimiento.",
        "Exoesqueleto pediátrico ATLAS 2030 (Marsi Bionics), robots sociales 'Robic' (Inrobics con IA), cámaras de fotogrametría Vicon y electromiografía digital.",
        "Niños y adolescentes con parálisis cerebral infantil (PCI), atrofia muscular espinal (AME) y daño cerebral infantil.",
        "Canal Empleo: Bolsa de Trabajo Oficial SERMAS (comunidad.madrid/servicios/salud). Para plazas de investigación/ingeniería: Fundación para la Investigación Biomédica del Hospital Niño Jesús (fibhnj.org)",
        "Av. de Menéndez Pelayo, 65, 28009 Madrid",
        "91 503 59 00",
        "https://www.comunidad.madrid/hospital/ninojesus"
    ),
    (
        "Centro de Daño Cerebral LESCER",
        "Centro Integral de Neurorrehabilitación Avanzada",
        "Privado Sanitario Especializado",
        "Médicos especialistas en Medicina Física y Rehabilitación, neurólogos consultores.",
        "Ingenieros biomédicos, técnicos de soporte informático de neurorrehabilitación, especialistas en software de realidad virtual.",
        "Combinación de tratamiento médico y entrenamiento asistido por ordenador para recuperación de la marcha, miembro superior y memoria.",
        "Sistema robótico de marcha Lokomat, sistemas de equilibrio computarizado, realidad virtual inmersiva y software de estimulación neuropsicológica.",
        "Personas con ictus, traumatismos craneoencefálicos, esclerosis múltiple, lesiones medulares incompletas.",
        "Web Empleo: lescer.es/trabaja-con-nosotros\nEmail Selección: rrhh@lescer.es / informacion@lescer.es",
        "Av. de Fuentelarreyna, 12, 28035 Madrid (Mirasierra)",
        "91 739 81 42",
        "informacion@lescer.es\nhttps://lescer.es"
    ),
    (
        "Hospital Los Madroños (Centro Avanzado Neurorrehabilitación)",
        "Hospital Médico Especializado en Neurorrehabilitación Robótica",
        "Privado Sanitario",
        "Médicos neurólogos, médicos rehabilitadores, intensivistas y neuropsicólogos.",
        "Ingenieros biomédicos 'in-house', técnicos informáticos de sistemas robóticos y análisis de bioseñales.",
        "Pioneros en España en integrar la robótica médica computarizada de miembros superiores e inferiores con monitorización médica continua.",
        "Exoesqueletos Lokomat Pro con 'FreeD', ArmeoSpring, Andago (entrenamiento de marcha libre asistida), sistemas de análisis cinemático computacional.",
        "Pacientes con lesión medular, ictus, traumatismos graves, ataxia y enfermedades neurodegenerativas.",
        "Web Empleo: losmadronos.com/trabaja-con-nosotros\nEmail Selección: recursoshumanos@losmadronos.com / info@losmadronos.com",
        "Ctra. M-501, Km 17,900, 28690 Brunete, Madrid",
        "91 816 35 26",
        "info@losmadronos.com\nhttps://losmadronos.com"
    ),
    (
        "Fundación CIEN / Centro Alzheimer Reina Sofía",
        "Centro de Investigación Médica y Neurológica",
        "Público Estatal (Fundación del Sector Público Estatal / ISCIII)",
        "Neurólogos investigadores, geriatras, neuropatólogos clínicos.",
        "Bioinformáticos, ingenieros informáticos de Big Data médica, analistas de neuroimagen computacional.",
        "Investigación traslacional que conecta el diagnóstico clínico con modelos computacionales de procesamiento de datos neurológicos y seguimiento cognitivo.",
        "Software avanzado de segmentación de resonancia magnética (FreeSurfer, SPM), bases de datos biomédicas en red y plataformas informáticas de evaluación.",
        "Personas con enfermedad de Alzheimer, deterioro cognitivo leve y demencias asociadas.",
        "Canal Convocatorias Oficiales: Portal de empleo público en fundacioncien.es/empleo y avisos de empleo del Instituto de Salud Carlos III (isciii.es)",
        "C/ Valderrebollo, 5, 28031 Madrid (Vallecas)",
        "91 385 22 00",
        "info@fundacioncien.es\nhttps://fundacioncien.es"
    ),
    (
        "Hospital Universitario La Paz (Rehabilitación y Biomecánica)",
        "Hospital Universitario Público / Laboratorio Movimiento",
        "Público Autonómico (Servicio Madrileño de Salud - SERMAS / CAM)",
        "Médicos rehabilitadores, traumatólogos, especialistas en medicina física.",
        "Bioingenieros, ingenieros de telecomunicaciones e informáticos del Instituto de Investigación Sanitaria IdiPAZ.",
        "Evaluación biomecánica informatizada pre y postquirúrgica; diseño de adaptaciones tecnológicas y prótesis computarizadas.",
        "Plataformas dinamométricas, electromiografía de superficie digital, sistemas de análisis computerizado de presiones plantares y telemedicina.",
        "Pacientes con patologías complejas del aparato locomotor, daño neurológico y amputaciones.",
        "Canal Empleo: Bolsa general del SERMAS. Para perfiles de bioingeniería e informática médica: Fundación para la Investigación Biomédica IdiPAZ (idipaz.es/ofertas-empleo)",
        "Paseo de la Castellana, 261, 28046 Madrid",
        "91 727 70 00",
        "https://www.comunidad.madrid/hospital/lapaz"
    ),
    (
        "Fundación Bobath (Centro de Atención Parálisis Cerebral)",
        "Centro Especializado en Tratamiento y Educación Especial",
        "Concertado / Tercer Sector (Fundación de iniciativa social)",
        "Médicos neuropediatras, médicos rehabilitadores, fisioterapeutas neurológicos.",
        "Técnicos especialistas en TIC adaptadas, informáticos de sistemas de comunicación aumentativa (SAAC) y adaptaciones de hardware.",
        "Prescripción médica y configuración informática de sistemas de acceso al ordenador para alumnos sin habla o con movilidad severamente restringida.",
        "Sistemas de mirada Tobii Dynavox, comunicadores de barrido computarizado, conmutadores por presión o soplo, software de teclado virtual adaptado.",
        "Bebés, niños y adultos jóvenes con parálisis cerebral y patologías neuromotoras afines.",
        "Web Empleo: fundacionbobath.org\nEmail Selección: secretaria@fundacionbobath.org / direccion@fundacionbobath.org",
        "C/ Mirador de la Reina, 115, 28035 Madrid (Mirasierra)",
        "91 738 26 27",
        "secretaria@fundacionbobath.org\nhttps://fundacionbobath.org"
    ),
    (
        "ILUNION Accesibilidad (Grupo Social ONCE)",
        "Consultora Tecnológica y Accesibilidad Universal",
        "Privada Empresarial (Grupo Social ONCE)",
        "Médicos del trabajo, técnicos superiores de ergonomía y salud laboral.",
        "Ingenieros de software, analistas de accesibilidad TIC, desarrolladores web y consultores de inteligencia artificial accesible.",
        "Auditoría médica y técnica de puestos de trabajo para personas con discapacidad; desarrollo de software adaptado y accesibilidad digital normativa.",
        "Lectores de pantalla corporativos, validadores automatizados de código accesible (WCAG 2.2), tecnologías hápticas y software de subtitulado/audiodescripción.",
        "Empresas, administraciones públicas y trabajadores con discapacidad física, sensorial o cognitiva.",
        "Web Empleo: ilunion.com/es/trabaja-con-nosotros\nPortal de empleo corporativo en InfoJobs ILUNION y Linkedin Talent",
        "C/ Albacete, 3, 28027 Madrid",
        "91 468 85 00",
        "contacto@ilunion.com\nhttps://ilunionaccesibilidad.com"
    ),
    (
        "Hospital Universitario Fundación Alcorcón (Biomecánica y TIC)",
        "Hospital Universitario Público / Rehabilitación y Telemedicina",
        "Público Autonómico (Fundación Pública Sanitaria - SERMAS)",
        "Médicos rehabilitadores, médicos de medicina preventiva y traumatólogos.",
        "Ingenieros informáticos de la Unidad de Tecnologías de la Información y Bioingeniería.",
        "Proyectos conjuntos de telerrehabilitación monitorizada en domicilio, registro informatizado de evolución funcional y prescripción ortésica digital.",
        "Plataformas seguras de tele-rehabilitación web, software de captura de movimiento por webcam/sensores inerciales y prescripción digital conectada al SERMAS.",
        "Pacientes en proceso de recuperación neurológica o musculoesquelética post-quirúrgica.",
        "Canal Empleo: Convocatorias de selección pública de personal en la web del Hospital (comunidad.madrid/hospital/fundacionalcorcon) y bolsa de empleo temporal del SERMAS",
        "C/ Budapest, 1, 28922 Alcorcón, Madrid",
        "91 621 94 00",
        "https://www.comunidad.madrid/hospital/fundacionalcorcon"
    )
]

col_widths_sheet4 = [28, 24, 25, 26, 26, 34, 34, 26, 34, 26, 16, 26]
format_sheet(ws4, "CENTROS CON PERSONAL ESPECIALIZADO EN MEDICINA E INFORMÁTICA APLICADA A LA DISCAPACIDAD",
             "Entidades hospitalarias y tecnológicas con datos de Titularidad y Vías de Envío de CV",
             headers_sheet4, data_sheet4, fill_sheet4, col_widths_sheet4)

# =============================================================
# SHEET 5: LINUX Y SOFTWARE LIBRE
# =============================================================
ws5 = wb.create_sheet(title="Linux y Software Libre")
headers_sheet5 = [
    "Nombre del Centro / Proyecto / Entidad",
    "Tipo de Dispositivo / Ámbito",
    "Titularidad (Público / Concertado / Privado)",
    "Uso Específico de Linux y Software Libre (FOSS)",
    "Distribuciones, Software y Herramientas Libres",
    "¿Cómo beneficia el Software Libre a los Usuarios?",
    "Perfil / Destinatarios",
    "Proyectos Destacados en Código Abierto",
    "Canal de Empleo / Cómo Enviar el CV",
    "Dirección / Municipio",
    "Teléfono Central",
    "Web Oficial / Enlace al Proyecto"
]

data_sheet5 = [
    (
        "Autofabricantes (Medialab Matadero Madrid)",
        "Laboratorio Ciudadano y Asociación de Investigación Abierta",
        "Privado / Tercer Sector (Asociación cultural en centro cultural municipal)",
        "Uso exclusivo de software libre y código abierto para el diseño, modelado e impresión 3D de prótesis y productos de apoyo biomecánicos.",
        "GNU/Linux en estaciones de diseño, FreeCAD, Blender, licencias Creative Commons / CERN Open Hardware, herramientas de diseño paramétrico.",
        "Democratiza las ayudas técnicas: cualquier familia o terapeuta puede descargar gratis los modelos 3D y modificarlos sin pagar royalties ni licencias.",
        "Niñas, niños y adultos con agenesias o amputaciones en miembros superiores y personas con diversidad funcional física.",
        "SuperGiz (prótesis abierta con accesorios intercambiables para comer, andar en bici o tocar instrumentos) y prótesis mioeléctricas libres.",
        "Email Contacto / Selección: info@autofabricantes.org (Perfiles en diseño 3D biomédico, terapia ocupacional y voluntariado profesional)\nWeb: autofabricantes.org",
        "Plaza de Legazpi, 8 / Paseo de la Chopera, 14, 28045 Madrid (Matadero)",
        "91 318 46 70",
        "info@autofabricantes.org\nhttps://autofabricantes.org"
    ),
    (
        "Colegios de Educación Especial - CEE con MAX (CAM)",
        "Red Pública Educativa / Consejería de Educación",
        "Público Autonómico (Comunidad de Madrid - Consejería de Educación)",
        "Implantación oficial de 'MAX' (MAdrid_linuX), la distribución oficial basada en Ubuntu desarrollada por la Comunidad de Madrid con accesibilidad integrada.",
        "MAX GNU/Linux (versiones 11 y 12), Orca (lector de pantalla), Caribou (teclado virtual), Dasher (escritura predictiva), KMag, KMouth y software ALBOR.",
        "Garantiza puestos informáticos accesibles, estables, libres de virus y sin coste de licencias privativas para los colegios públicos de educación especial.",
        "Alumnado con discapacidad intelectual severa, parálisis cerebral, TEA, sordera o baja visión escolarizado en centros de la CAM.",
        "Programa ALBOR (Acceso Libre de Barreras al Ordenador) con repositorio de adaptaciones TIC libres en Educamadrid.",
        "Canal Empleo Público: Oposiciones al cuerpo docente de maestros (PT/AL) y listas de interinos de la CAM (comunidad.madrid/servicios/educacion). Para personal informático: Oposiciones de la CAM",
        "CEE de la CAM (ej. CEE Ponce de León, CEE Joan Miró, CEE María Soriano)",
        "012 (Atención CAM)",
        "https://max.educa.madrid.org\nhttps://www.educa2.madrid.org"
    ),
    (
        "CEAPAT - Área de Tecnologías Accesibles y FOSS",
        "Centro de Referencia Estatal (IMSERSO)",
        "Público Estatal (Ministerio de Derechos Sociales / IMSERSO - Estado)",
        "Promoción, evaluación, divulgación y catálogo de herramientas de software libre y código abierto destinadas a la comunicación aumentativa y accesibilidad.",
        "Lector de pantalla NVDA (código abierto), Orca (para escritorio Linux GNOME), comunicadores libres Plaphoons, AraWord, Cboard y e-Mintza.",
        "Permite que personas con discapacidad motriz y del habla accedan a comunicadores de calidad sin desembolsar miles de euros en licencias propietarias.",
        "Personas con dificultades de comunicación oral, movilidad reducida, terapeutas ocupacionales y logopedas de toda España.",
        "Catálogo Estatal de Productos de Apoyo con apartado específico de herramientas FOSS y software libre descargable.",
        "Canal Empleo Público: Convocatorias de empleo público del Estado publicadas en administracion.gob.es y procesos selectivos del Imserso",
        "C/ Los Extremeños, 1, 28018 Madrid",
        "91 703 31 00",
        "ceapat@imserso.es\nhttps://ceapat.imserso.es"
    ),
    (
        "CTI de la ONCE (Centro de Tiflotecnología e Innovación)",
        "Centro de Innovación Tecnológica para Discapacidad Visual",
        "Privado Institucional / Corporación de Derecho Público sin ánimo de lucro (ONCE)",
        "Investigación, adaptación y soporte técnico en entornos Linux para personas ciegas o con baja visión severa.",
        "Distribuciones Linux (Ubuntu/Debian), lector de pantalla libre Orca, BRLTTY (controladores libres para líneas braille bajo Linux), Emacspeak.",
        "Asegura que los desarrolladores y usuarios ciegos no dependan exclusivamente de Windows/macOS, permitiéndoles trabajar en servidores y programación Linux.",
        "Afiliados a la ONCE, estudiantes universitarios de informática y profesionales ciegos que utilizan terminales Linux.",
        "Guías oficiales de configuración del lector de pantalla Orca en Linux y soporte para líneas braille USB/Bluetooth de código abierto.",
        "Portal de Empleo: once.es/trabaja-en-la-once\nEmail RRHH: rrhh_dgi@once.es / cti@once.es",
        "Camino de Hormigueras, 172, 28031 Madrid (Vallecas)",
        "91 010 91 11",
        "cti@once.es\nhttps://cti.once.es"
    ),
    (
        "Cátedra de Tecnologías Inclusivas - ETSIT UPM",
        "Universidad Pública / Escuela Técnica Superior de Telecomunicación",
        "Público Estatal / Universitario (Universidad Politécnica de Madrid)",
        "I+D en soluciones de teleasistencia, domótica accesible y bioingeniería utilizando sistemas operativos libres y hardware de código abierto.",
        "Linux embebido, Raspberry Pi OS (Debian), ROS (Robot Operating System - código abierto), bibliotecas OpenCV para seguimiento facial libre y Arduino.",
        "Desarrollo de prototipos de muy bajo coste para control del entorno (luces, puertas, persianas) adaptados a personas con tetraplejia o parálisis cerebral.",
        "Personas con gran discapacidad física y daño cerebral, investigadores y estudiantes de ingeniería de Madrid.",
        "Sistemas abiertos de domótica accesible de bajo coste y desarrollo de algoritmos libres de reconocimiento de gestos para la movilidad.",
        "Canal Convocatorias Oficiales: Portal de contratación de investigadores y técnicos de la UPM en upm.es/investigacion/convocatorias y web de la ETSIT",
        "Av. Complutense, 30, 28040 Madrid (Ciudad Universitaria)",
        "91 067 19 00",
        "director@etsit.upm.es\nhttps://www.etsit.upm.es"
    ),
    (
        "Centro de Accesibilidad Virtual de la UNED (Madrid)",
        "Universidad Nacional de Educación a Distancia / Sede Central",
        "Público Estatal / Universitario (UNED - Estado)",
        "Investigación y aplicación de plataformas web de código abierto y entornos Linux accesibles para estudiantes con discapacidad.",
        "Moodle accesible (código abierto), servidores GNU/Linux Debian, lectores de pantalla libres y estándares abiertos WAI-ARIA.",
        "Garantiza el derecho a la educación universitaria superior sin que la plataforma digital suponga una barrera técnica o económica.",
        "Estudiantes universitarios con discapacidad sensorial, física o del desarrollo de toda la Comunidad de Madrid.",
        "Adaptación de cursos virtuales en plataformas FOSS con validación de accesibilidad integral.",
        "Canal Convocatorias Oficiales: Portal de empleo público y contratación de proyectos de la UNED en uned.es (sección Empleo y Convocatorias)",
        "C/ Juan del Rosal, 16, 28040 Madrid (Ciudad Universitaria)",
        "91 398 66 00",
        "accesibilidad@adm.uned.es\nhttps://www.uned.es"
    ),
    (
        "Por Talento Digital - Fundación ONCE (Aulas Tecnológicas)",
        "Centro de Formación Tecnológica y Empleabilidad",
        "Tercer Sector (Fundación ONCE)",
        "Formación especializada a personas con discapacidad en administración de sistemas Linux, desarrollo de software libre y ciberseguridad.",
        "Distribuciones Linux (Ubuntu Server, Red Hat, Debian), Git, Python, bases de datos PostgreSQL y herramientas de desarrollo libre.",
        "Capacita a personas con discapacidad para trabajar en el sector tecnológico como administradores de sistemas y programadores con alta demanda laboral.",
        "Personas con certificado de discapacidad (>= 33%) con perfil tecnológico o que deseen reciclarse profesionalmente.",
        "Bootcamps tecnológicos gratuitos adaptados en tecnologías abiertas y Linux para la inserción laboral cualificada.",
        "Portal de Empleo: empleo.fundaciononce.es / portalentodigital.fundaciononce.es\nEmail RRHH: rrhh@fundaciononce.es",
        "C/ Fray Luis de León, 11, 28012 Madrid (Atocha)",
        "91 468 85 00",
        "portalentodigital@fundaciononce.es\nhttps://portalentodigital.fundaciononce.es"
    ),
    (
        "Makespace Madrid (Fabricación Social y Hardware Libre)",
        "Taller Maker Colaborativo y FabLab Comunitario",
        "Privado Colaborativo (Asociación cultural sin ánimo de lucro)",
        "Espacio de fabricación comunitaria donde ingenieros y personas con diversidad funcional diseñan adaptaciones usando software libre.",
        "Ubuntu Linux, software de corte e impresión 3D Cura/PrusaSlicer (código abierto), FreeCAD, Kicad para diseño electrónico libre y microcontroladores Arduino.",
        "Posibilidad de reparar, modificar o crear pulsadores adaptados a medida para videojuegos o sillas de ruedas por una fracción del precio comercial.",
        "Makers con y sin discapacidad, terapeutas ocupacionales y personas con necesidades de adaptación ortopédica personalizada.",
        "Adaptadores libres para mandos de videojuegos, conmutadores mecánicos y soportes impresos en 3D bajo licencias abiertas.",
        "Email Contacto / Selección: info@makespacemadrid.org (Proyectos de docencia tecnológica, talleres y coordinación técnica FabLab)",
        "C/ General Lacy, 23, 28045 Madrid (Delicias)",
        "91 539 00 14",
        "info@makespacemadrid.org\nhttps://makespacemadrid.org"
    ),
    (
        "Red ARASAAC / Centros Educativos y Ocupacionales Madrid",
        "Sistemas Aumentativos y Alternativos de Comunicación Libres",
        "Público Autonómico / Proyecto Institucional Abierto",
        "Implantación masiva en centros de día, colegios y asociaciones madrileñas de la suite libre de pictogramas y software de comunicación abierta ARASAAC.",
        "AraWord (procesador de textos con pictogramas libre), AsTeRICS Grid (comunicador web libre multiplataforma), Cboard y pictogramas con licencia CC (BY-NC-SA).",
        "Elimina el monopolio de programas privativos de comunicación que cuestan cientos de euros, permitiendo que cualquier persona tenga voz en una tableta u ordenador.",
        "Personas con autismo no verbal, afasia, parálisis cerebral, discapacidad intelectual o dificultades de comprensión del lenguaje.",
        "Integración de AraWord y AsTeRICS en ordenadores con Linux y dispositivos táctiles comunitarios de la región.",
        "Canal Colaboración Técnica: Contacto directo de aportación de código y colaboración pedagógica en arasaac@aragon.es / arasaac.org",
        "Utilizado activamente en centros ocupacionales y educativos de Madrid",
        "Atención online",
        "arasaac@aragon.es\nhttps://arasaac.org"
    ),
    (
        "Asociación Guifi.net Madrid / Proyectos de Soberanía Digital",
        "Red Ciudadana de Telecomunicaciones y Software Libre",
        "Privado / Tercer Sector (Red ciudadana sin ánimo de lucro)",
        "Proyectos de reducción de la brecha digital para colectivos en riesgo de exclusión y diversidad funcional mediante ordenadores reciclados con Linux.",
        "Distribuciones Linux ligeras (Lubuntu, Linux Mint, Debian), software ofimático LibreOffice, navegadores libres configurados con extensiones de lectura asistida.",
        "Proporciona ordenadores completamente funcionales y libres a familias de personas con discapacidad que no disponen de recursos para comprar licencias comerciales.",
        "Personas con diversidad funcional y familias vulnerables del sur de Madrid y barrios periféricos.",
        "Campañas de donación de equipos informáticos recuperados con GNU/Linux y adaptaciones de accesibilidad básica.",
        "Canal Participación / CV: Asambleas y proyectos de voluntariado e inclusión técnica a través de la web guifi.net",
        "Encuentros en espacios vecinales y asociativos de Madrid",
        "Contacto web",
        "https://guifi.net"
    )
]

col_widths_sheet5 = [28, 24, 25, 30, 32, 34, 26, 32, 34, 26, 16, 26]
format_sheet(ws5, "CENTROS, PROYECTOS Y ENTIDADES QUE USAN LINUX Y SOFTWARE LIBRE EN DISCAPACIDAD",
             "Recursos que implementan GNU/Linux y tecnologías abiertas con datos de Titularidad y Canales de Envío de CV",
             headers_sheet5, data_sheet5, fill_sheet5, col_widths_sheet5)

output_path = "/home/bender/Descargas/Recursos_Discapacidad_Comunidad_de_Madrid.xlsx"
wb.save(output_path)
print(f"Successfully generated updated workbook with ownership and CV columns: {output_path}")

