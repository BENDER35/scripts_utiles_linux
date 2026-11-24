import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Datos recopilados de Integradores de TI y Servicios de Asistencia Técnica (SAT) en la Comunidad de Madrid
data = [
    {
        "Empresa": "Seidor España (Seidor S.A.)",
        "Teléfono": "+34 911 274 100",
        "WhatsApp": "No publicado (Atención vía centralita / portal)",
        "Correo General": "info@seidor.com / marketing@seidor.com",
        "Correo / Canal RRHH (Curriculum)": "seidor.com/es/es/talento",
        "Cómo Enviar el CV": "Registro en el portal oficial seidor.com/es/es/talento o postulación en las ofertas activas de InfoJobs.",
        "Dirección Postal": "Plaza Pablo Ruiz Picasso, 11, Edificio RP11, Planta 2, 28020 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Tetuán - Azca)",
        "Sitio Web": "https://www.seidor.com",
        "Servicios y Especialidad": "Integrador de TI, servicios gestionados, cloud, ciberseguridad, mantenimiento de infraestructuras y soluciones ERP."
    },
    {
        "Empresa": "Inetum España S.A.",
        "Teléfono": "+34 913 874 700",
        "WhatsApp": "No publicado (Atención telefónica corporativa)",
        "Correo General": "mkt-es@inetum.world",
        "Correo / Canal RRHH (Curriculum)": "inetum.com/es/carrera",
        "Cómo Enviar el CV": "Inscripción en el portal de empleo inetum.com/es/carrera o postulaciones en InfoJobs / LinkedIn.",
        "Dirección Postal": "Calle María de Portugal, 9-11, Edificio 1, 28050 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Hortaleza - Sanchinarro)",
        "Sitio Web": "https://www.inetum.com/es",
        "Servicios y Especialidad": "Integración de sistemas TI, soporte de campo (SAT), servicios gestionados, infraestructura y consultoría tecnológica."
    },
    {
        "Empresa": "Minsait (Indra Group)",
        "Teléfono": "+34 914 805 000",
        "WhatsApp": "No publicado (Portal oficial de talento)",
        "Correo General": "candidatos@minsait.com",
        "Correo / Canal RRHH (Curriculum)": "minsait.com/es/talento",
        "Cómo Enviar el CV": "Registro e inscripción en el portal de empleo oficial minsait.com/es/talento o perfil corporativo de InfoJobs.",
        "Dirección Postal": "Avenida de Bruselas, 35, 28108 Alcobendas, Madrid",
        "Municipio / Zona": "Alcobendas (Zona Norte)",
        "Sitio Web": "https://www.minsait.com",
        "Servicios y Especialidad": "Integración TI global, asistencia técnica SAT, gestión de infraestructuras, ciberseguridad y transformación digital."
    },
    {
        "Empresa": "NTT DATA España",
        "Teléfono": "+34 917 490 000",
        "WhatsApp": "No publicado (Portal corporativo)",
        "Correo General": "infoweb@nttdata.com",
        "Correo / Canal RRHH (Curriculum)": "nttdata.com/careers",
        "Cómo Enviar el CV": "Postulación en nttdata.com (sección Careers) o perfil en InfoJobs / LinkedIn.",
        "Dirección Postal": "Camino Fuente de la Mora, 1, 28050 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Hortaleza - Sanchinarro)",
        "Sitio Web": "https://www.nttdata.com/es/es/",
        "Servicios y Especialidad": "Integración de sistemas TI, desarrollo, cloud, ciberseguridad y mantenimiento informático especializado."
    },
    {
        "Empresa": "Logicalis España S.L.",
        "Teléfono": "+34 917 669 069",
        "WhatsApp": "No publicado (Atención directa email)",
        "Correo General": "info@es.logicalis.com",
        "Correo / Canal RRHH (Curriculum)": "seleccion@es.logicalis.com",
        "Cómo Enviar el CV": "Envío directo de currículum al correo oficial de selección: seleccion@es.logicalis.com.",
        "Dirección Postal": "Calle Ribera del Loira, 38, Edificio 4, 28042 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Barajas - Campo de las Naciones)",
        "Sitio Web": "https://www.es.logicalis.com",
        "Servicios y Especialidad": "Integrador tecnológico global, redes, ciberseguridad, cloud, servicios gestionados y soporte SAT in-situ."
    },
    {
        "Empresa": "Econocom España S.A.",
        "Teléfono": "+34 914 119 120",
        "WhatsApp": "No publicado",
        "Correo General": "marketingycomunicacion@econocom.com",
        "Correo / Canal RRHH (Curriculum)": "econocom.es (Candidatura espontánea)",
        "Cómo Enviar el CV": "Formulario de candidatura espontánea en econocom.es o inscripción mediante vacantes publicadas en InfoJobs.",
        "Dirección Postal": "Calle Cardenal Marcelo Spínola, 4, 28016 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Chamartín)",
        "Sitio Web": "https://www.econocom.es",
        "Servicios y Especialidad": "Integración de soluciones digitales, soporte y asistencia técnica (SAT), mantenimiento de equipamiento TI e infraestructuras."
    },
    {
        "Empresa": "Axians España (VINCI Energies)",
        "Teléfono": "+34 914 560 008",
        "WhatsApp": "No publicado",
        "Correo General": "marketing@axians.es",
        "Correo / Canal RRHH (Curriculum)": "axians.es/unete-a-nosotros",
        "Cómo Enviar el CV": "Formulario 'Únete a nosotros' en axians.es adjuntando CV e indicando la oficina de Madrid.",
        "Dirección Postal": "Calle Quintanavides, 15, Edificio 2, Parque Vía Norte, 28050 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Hortaleza - Las Tablas)",
        "Sitio Web": "https://www.axians.es",
        "Servicios y Especialidad": "Integración de redes de telecomunicaciones, ciberseguridad, data centers, soporte SAT y mantenimiento técnico."
    },
    {
        "Empresa": "Bechtle Direct España S.A.",
        "Teléfono": "+34 913 640 234",
        "WhatsApp": "No publicado",
        "Correo General": "bechtle@bechtle.es",
        "Correo / Canal RRHH (Curriculum)": "bechtle@bechtle.es / bechtle.com/empleo",
        "Cómo Enviar el CV": "Portal de empleo bechtle.com/es/es/empleo o envío directo de CV a bechtle@bechtle.es.",
        "Dirección Postal": "Calle Vía de los Poblados, 3 (Parque Ind. Cristalia, Edif. 1), 28033 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Hortaleza)",
        "Sitio Web": "https://www.bechtle.com/es/es",
        "Servicios y Especialidad": "Proveedor e integrador de soluciones TI, microinformática, servicios gestionados y SAT corporativo."
    },
    {
        "Empresa": "Devoteam España S.A.",
        "Teléfono": "+34 913 768 820",
        "WhatsApp": "No publicado",
        "Correo General": "info@devoteam.com",
        "Correo / Canal RRHH (Curriculum)": "es.devoteam.com/carreras",
        "Cómo Enviar el CV": "Postulación en el portal de empleo es.devoteam.com/carreras o mediante InfoJobs / LinkedIn.",
        "Dirección Postal": "Calle María de Molina, 37 Bis, 28006 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Salamanca)",
        "Sitio Web": "https://es.devoteam.com",
        "Servicios y Especialidad": "Consultoría e integración de sistemas TI, cloud, soporte técnico especializado y transformación de datos."
    },
    {
        "Empresa": "Kyndryl España S.A.",
        "Teléfono": "+34 910 628 000",
        "WhatsApp": "No publicado",
        "Correo General": "noticias@kyndryl.com",
        "Correo / Canal RRHH (Curriculum)": "kyndryl.com/careers",
        "Cómo Enviar el CV": "Registro en el portal global de empleo kyndryl.com/es/es/about-us/careers.",
        "Dirección Postal": "Calle Albacete, 5, 28027 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Ciudad Lineal)",
        "Sitio Web": "https://www.kyndryl.com/es/es",
        "Servicios y Especialidad": "Integrador de infraestructuras críticas TI, cloud híbrido, soporte de campo SAT y mantenimiento de sistemas."
    },
    {
        "Empresa": "Nunsys Group (Sede Madrid)",
        "Teléfono": "+34 960 500 631 / +34 911 238 900",
        "WhatsApp": "No publicado",
        "Correo General": "info@nunsys.com",
        "Correo / Canal RRHH (Curriculum)": "nunsys.com (Trabaja con Nosotros)",
        "Cómo Enviar el CV": "Envío de candidatura espontánea en la web nunsys.com (sección Empleo) o email a info@nunsys.com.",
        "Dirección Postal": "Calle Ramírez de Arellano, 29, 7ª pl. (Edificio Merrimack II), 28043 Madrid",
        "Municipio / Zona": "Madrid Capital (Distrito Ciudad Lineal - Arturo Soria)",
        "Sitio Web": "https://www.nunsys.com",
        "Servicios y Especialidad": "Integración de sistemas TI, telecomunicaciones, ciberseguridad, software y soporte de asistencia técnica SAT."
    },
    {
        "Empresa": "Tecnozero Soluciones Informáticas",
        "Teléfono": "+34 916 872 523",
        "WhatsApp": "+34 916 872 523 (Atención / WhatsApp Empresa)",
        "Correo General": "tecnozero@tecnozero.com",
        "Correo / Canal RRHH (Curriculum)": "sat@tecnozero.com",
        "Cómo Enviar el CV": "Envío de CV directo a sat@tecnozero.com o tecnozero@tecnozero.com con el asunto 'Candidatura Técnico SAT'.",
        "Dirección Postal": "Calle San José, 16, Local 2, 28921 Alcorcón, Madrid",
        "Municipio / Zona": "Alcorcón (Zona Sur)",
        "Sitio Web": "https://www.tecnozero.com",
        "Servicios y Especialidad": "Servicio de Asistencia Técnica (SAT) informático, mantenimiento de redes, servidores y soporte TI in-situ para pymes."
    },
    {
        "Empresa": "SAT Tecnología",
        "Teléfono": "+34 692 270 000 / +34 911 460 030",
        "WhatsApp": "+34 692 270 000 (Atención directa WhatsApp)",
        "Correo General": "comercial@sat-tecnologia.com",
        "Correo / Canal RRHH (Curriculum)": "comercial@sat-tecnologia.com",
        "Cómo Enviar el CV": "Envío directo de correo electrónico con CV adjunto a comercial@sat-tecnologia.com.",
        "Dirección Postal": "Calle Pedroches, 58, 28915 Leganés, Madrid",
        "Municipio / Zona": "Leganés (Zona Sur)",
        "Sitio Web": "http://www.sat-tecnologia.com",
        "Servicios y Especialidad": "Asistencia técnica informática (SAT), mantenimiento de servidores, instalación de redes y soporte remoto/presencial."
    },
    {
        "Empresa": "OVERTI (Overti Soluciones TI)",
        "Teléfono": "+34 911 460 030",
        "WhatsApp": "No publicado",
        "Correo General": "info@overti.es",
        "Correo / Canal RRHH (Curriculum)": "info@overti.es",
        "Cómo Enviar el CV": "Formulario web en overti.es o envío de email con CV adjunto a info@overti.es.",
        "Dirección Postal": "Calle Margarita Salas, 16, 28919 Leganés, Madrid",
        "Municipio / Zona": "Leganés (Zona Sur - Leganés Tecnológico)",
        "Sitio Web": "https://www.overti.es",
        "Servicios y Especialidad": "Integración TI, mantenimiento informático para empresas, infraestructuras, redes y soporte técnico SAT."
    }
]

df = pd.DataFrame(data)

file_path = "/home/bender/Descargas/integradores_ti_sat_madrid.xlsx"

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Integradores TI y SAT Madrid"

ws.views.sheetView[0].showGridLines = True

# Paleta de colores
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
ZEBRA_FILL = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Calibri", size=10, color="000000")
TITLE_FONT = Font(name="Calibri", size=16, bold=True, color="1F4E78")
SUBTITLE_FONT = Font(name="Calibri", size=10, italic=True, color="595959")

THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# Encabezado del documento
ws.cell(row=1, column=1, value="LISTADO DE INTEGRADORES DE TI Y EMPRESAS DE SAT EN MADRID").font = TITLE_FONT
ws.cell(row=2, column=1, value="Contactos corporativos, WhatsApp, canales de RRHH / Envío de CV, dirección y especialidad técnica").font = SUBTITLE_FONT

headers = list(df.columns)
start_row = 4

# Escribir cabeceras de tabla
for col_num, header_title in enumerate(headers, 1):
    cell = ws.cell(row=start_row, column=col_num, value=header_title)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = THIN_BORDER

ws.row_dimensions[start_row].height = 30

# Escribir filas de datos
for row_idx, row_data in enumerate(df.to_dict('records'), start=start_row + 1):
    fill = ZEBRA_FILL if row_idx % 2 == 0 else WHITE_FILL
    for col_idx, col_name in enumerate(headers, start=1):
        cell_value = row_data[col_name]
        cell = ws.cell(row=row_idx, column=col_idx, value=cell_value)
        cell.fill = fill
        cell.font = REGULAR_FONT
        cell.border = THIN_BORDER
        
        if col_name in ["Teléfono", "WhatsApp"]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    ws.row_dimensions[row_idx].height = 48

# Ajuste dinámico de columnas
col_widths = {
    "Empresa": 28,
    "Teléfono": 22,
    "WhatsApp": 28,
    "Correo General": 26,
    "Correo / Canal RRHH (Curriculum)": 32,
    "Cómo Enviar el CV": 45,
    "Dirección Postal": 38,
    "Municipio / Zona": 25,
    "Sitio Web": 22,
    "Servicios y Especialidad": 45
}

for col_idx, col_name in enumerate(headers, start=1):
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = col_widths.get(col_name, 25)

wb.save(file_path)
print(f"Archivo Excel generado con éxito en: {file_path}")
