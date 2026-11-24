import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Color Palette: Elegant Corporate Navy / Slate / Emerald
NAVY_HEADER = "1B365D"       # Dark Navy for main headers
SLATE_HEADER = "335C67"      # Slate Teal for secondary
LIGHT_BLUE = "EBF2F7"        # Alternating row fill light
LIGHT_GREEN = "EAF5EA"       # Soft green for free/approved
ACCENT_GREEN = "2E7D32"      # Green text for free
ACCENT_RED = "C62828"        # Red for paid / alerts
ACCENT_BLUE = "1565C0"       # Blue for links/totals
GRAY_BORDER = "D3D3D3"       # Soft border
DARK_GRAY_BORDER = "7F7F7F"
TOTAL_FILL = "D9E1F2"        # Total row background

thin_border = Border(
    left=Side(style='thin', color=GRAY_BORDER),
    right=Side(style='thin', color=GRAY_BORDER),
    top=Side(style='thin', color=GRAY_BORDER),
    bottom=Side(style='thin', color=GRAY_BORDER)
)

header_border = Border(
    left=Side(style='thin', color="FFFFFF"),
    right=Side(style='thin', color="FFFFFF"),
    top=Side(style='medium', color=NAVY_HEADER),
    bottom=Side(style='medium', color=NAVY_HEADER)
)

total_border = Border(
    left=Side(style='thin', color=DARK_GRAY_BORDER),
    right=Side(style='thin', color=DARK_GRAY_BORDER),
    top=Side(style='thin', color=DARK_GRAY_BORDER),
    bottom=Side(style='double', color=DARK_GRAY_BORDER)
)

font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
font_subtitle = Font(name="Calibri", size=10, italic=True, color="333333")
font_tbl_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_data = Font(name="Calibri", size=10, color="000000")
font_data_bold = Font(name="Calibri", size=10, bold=True, color="000000")
font_total = Font(name="Calibri", size=11, bold=True, color="1B365D")
font_link = Font(name="Calibri", size=10, color="004B91", underline="single")
font_alert = Font(name="Calibri", size=10, bold=True, color="C62828")
font_free = Font(name="Calibri", size=10, bold=True, color="2E7D32")

# ==============================================================================
# HOJA 1: MODALIDAD A
# ==============================================================================
ws1 = wb.create_sheet(title="Modalidad A")
ws1.views.sheetView[0].showGridLines = True

# Title banner
ws1.merge_cells("A1:K1")
ws1["A1"] = "AYUNTAMIENTOS DE LA COMUNIDAD DE MADRID - MODALIDAD A (SERVICIO 010)"
ws1["A1"].font = font_title
ws1["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 36

# Legal context & info notes
ws1.merge_cells("A2:K2")
ws1["A2"] = "Marco Normativo: Resolución de 31 de julio de 2013 (SETSI - BOE núm. 226/2013). Tarificación ordinaria por tiempo a cargo del llamante."
ws1["A2"].font = Font(name="Calibri", size=10, bold=True, color="1B365D")
ws1["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[2].height = 20

ws1.merge_cells("A3:K3")
ws1["A3"] = "Condiciones de Coste: El abonado abona el precio de establecimiento y precio por minuto de una llamada ordinaria (fijo-fijo provincial o móvil-fijo nacional). Al ser número corto, los operadores suelen EXCLUIRLO de tarifas planas y bonos ilimitados."
ws1["A3"].font = Font(name="Calibri", size=9, italic=True, color="555555")
ws1["A3"].alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[3].height = 18

ws1.merge_cells("A4:K4")
ws1["A4"] = "Recomendación: Para evitar cargos adicionales en factura, se aconseja utilizar el número geográfico provincial alternativo (91...) incluido sin recargo en cualquier tarifa plana."
ws1["A4"].font = Font(name="Calibri", size=9, bold=True, color="C62828")
ws1["A4"].alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[4].height = 18

# Table Headers
headers_ws1 = [
    "Nº", "Ayuntamiento / Municipio", "Código INE", "Población (Hab.)",
    "Número Corto", "Modalidad 010", "Número Geográfico Alternativo (Prefijo 91)",
    "Régimen de Coste al Ciudadano", "Horario Habitual Atención",
    "Sede Electrónica Oficial (Canal Gratuito)", "Observaciones del Servicio"
]
ws1.row_dimensions[6].height = 28
for col_idx, h_text in enumerate(headers_ws1, 1):
    cell = ws1.cell(row=6, column=col_idx, value=h_text)
    cell.font = font_tbl_header
    cell.fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = header_border

# Data Rows for Modalidad A
data_ws1 = [
    (1, "Alcalá de Henares", "28005", 199184, "010", "Modalidad A", "91 880 28 11 / 91 888 33 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 14:00 h", "https://sede.ayto-alcaladehenares.es", "SAC Alcalá. 010 dentro de término municipal."),
    (2, "Alcobendas", "28006", 119496, "010", "Modalidad A", "91 296 90 88", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 14:30 h / 16:00 a 19:00 h", "https://sede.alcobendas.org", "SAC Alcobendas. Modalidad A formalmente regulada."),
    (3, "Alcorcón", "28007", 171772, "010", "Modalidad A", "91 664 81 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 14:30 h", "https://sede.ayto-alcorcon.es", "010 operativo desde fijos locales de Alcorcón."),
    (4, "Arganda del Rey", "28014", 57553, "010", "Modalidad A", "91 871 13 44", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 19:30 h", "https://sede.ayto-arganda.es", "Oficina de Atención a la Ciudadanía 010."),
    (5, "Boadilla del Monte", "28022", 64742, "010", "Modalidad A", "91 634 93 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 9:00 a 14:30 h", "https://sede.ayuntamientoboadilladelmonte.org", "010 dentro de Boadilla; 91 634 93 00 centralita."),
    (6, "Fuenlabrada", "28058", 189891, "010", "Modalidad A", "91 649 70 10", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 19:00 h", "https://sede.ayto-fuenlabrada.es", "010 desde fijo en Fuenlabrada; 91 649 70 10 desde móvil."),
    (7, "Leganés", "28074", 190665, "010", "Modalidad A", "91 248 90 10 / 91 248 90 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 14:30 h", "https://sede.leganes.org", "SAC Leganés. Se recomienda usar 91 248 90 10 sin coste."),
    (8, "Móstoles", "28092", 211265, "010", "Modalidad A", "91 647 17 10 / 91 664 75 00", "Coste ordinario operador (tarificación especial)", "L-V 8:00 a 20:00 h", "https://sede.mostoles.es", "SAC Móstoles. Clasificado de tarificación especial."),
    (9, "Navalcarnero", "28096", 31379, "010", "Modalidad A", "91 810 13 30", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 14:15 h", "https://sede.navalcarnero.es", "Atribuido en BOE 2013; centralita general preferente."),
    (10, "Parla", "28106", 133004, "010", "Modalidad A", "91 624 03 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 14:30 h", "https://sede.ayuntamientoparla.es", "SAC Parla. 010 activo dentro del municipio."),
    (11, "Pinto", "28113", 55209, "010", "Modalidad A", "91 248 37 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 15:00 h", "https://sede.ayto-pinto.es", "Atribuido en BOE 2013; SAC Pinto."),
    (12, "Pozuelo de Alarcón", "28115", 88784, "010", "Modalidad A", "91 217 14 92", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 20:00 h; Sáb 9:00 a 14:00 h", "https://sede.pozuelodealarcon.org", "010 municipal; alternativo fijo gratuito en tarifa plana."),
    (13, "Rivas-Vaciamadrid", "28123", 100270, "010", "Modalidad A", "91 670 00 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:00 a 20:00 h", "https://sede.rivasciudad.es", "SIAC Rivas. 010 en fijos locales; alternativo móvil 91..."),
    (14, "San Sebastián de los Reyes", "28134", 92734, "010", "Modalidad A", "91 659 71 00 / 91 625 88 55", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 14:30 h", "https://sede.ssreyes.org", "SAC Sanse. Clasificado de tarificación especial."),
    (15, "Torrejón de Ardoz", "28148", 137711, "010", "Modalidad A", "91 678 95 00", "Coste ordinario operador (fuera de tarifa plana)", "L-V 8:30 a 14:00 h", "https://sede.ayto-torrejon.es", "010 desde fijos locales; alternativo fijo provincial.")
]

start_row_ws1 = 7
for idx, row_data in enumerate(data_ws1):
    curr_row = start_row_ws1 + idx
    ws1.row_dimensions[curr_row].height = 20
    is_alt = (idx % 2 == 1)
    fill_row = PatternFill(start_color=LIGHT_BLUE, end_color=LIGHT_BLUE, fill_type="solid") if is_alt else PatternFill(fill_type=None)

    for c_idx, val in enumerate(row_data, 1):
        cell = ws1.cell(row=curr_row, column=c_idx, value=val)
        cell.font = font_data
        cell.border = thin_border
        if is_alt:
            cell.fill = fill_row
        
        # Specific alignments & formatting
        if c_idx in (1, 3, 5):
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx == 4:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = "#,##0"
        elif c_idx == 6:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = font_alert
        elif c_idx == 10:
            cell.font = font_link
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

end_row_ws1 = start_row_ws1 + len(data_ws1) - 1

# Total Row for Modalidad A
tot_row_ws1 = end_row_ws1 + 1
ws1.row_dimensions[tot_row_ws1].height = 24

ws1.cell(row=tot_row_ws1, column=1, value="")
ws1.cell(row=tot_row_ws1, column=2, value="TOTAL AYUNTAMIENTOS MODALIDAD A")
ws1.cell(row=tot_row_ws1, column=3, value=f"=COUNTA(B{start_row_ws1}:B{end_row_ws1})")
ws1.cell(row=tot_row_ws1, column=4, value=f"=SUM(D{start_row_ws1}:D{end_row_ws1})")
ws1.cell(row=tot_row_ws1, column=5, value="15 Municipios")
ws1.cell(row=tot_row_ws1, column=6, value="Modalidad A")
ws1.cell(row=tot_row_ws1, column=7, value="15 Números Geográficos Alternativos")
ws1.cell(row=tot_row_ws1, column=8, value="Coste a cargo del usuario llamante")
ws1.cell(row=tot_row_ws1, column=9, value="Población total cubierta:")
ws1.cell(row=tot_row_ws1, column=10, value="100% con Sede Electrónica Gratuita")
ws1.cell(row=tot_row_ws1, column=11, value="Total Consistorios Modalidad A: 15")

for c_idx in range(1, 12):
    cell = ws1.cell(row=tot_row_ws1, column=c_idx)
    cell.font = font_total
    cell.fill = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    cell.border = total_border
    if c_idx in (1, 3, 5, 6):
        cell.alignment = Alignment(horizontal="center", vertical="center")
    elif c_idx == 4:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = "#,##0"
    else:
        cell.alignment = Alignment(horizontal="left", vertical="center")

# ==============================================================================
# HOJA 2: MODALIDAD B
# ==============================================================================
ws2 = wb.create_sheet(title="Modalidad B")
ws2.views.sheetView[0].showGridLines = True

# Title banner
ws2.merge_cells("A1:I1")
ws2["A1"] = "AYUNTAMIENTOS DE LA COMUNIDAD DE MADRID - MODALIDAD B (SERVICIO 010)"
ws2["A1"].font = font_title
ws2["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 36

# Legal context & info notes
ws2.merge_cells("A2:I2")
ws2["A2"] = "Marco Normativo: Resolución de 31 de julio de 2013 (SETSI - BOE núm. 226/2013). Tarificación con recargo compartido a cargo del usuario."
ws2["A2"].font = Font(name="Calibri", size=10, bold=True, color="1B365D")
ws2["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[2].height = 20

ws2.merge_cells("A3:I3")
ws2["A3"] = "Régimen Tarifario Teórico: Establecimiento de llamada al DOBLE del precio ordinario nacional; precio por minuto igual a ordinaria nacional."
ws2["A3"].font = Font(name="Calibri", size=9, italic=True, color="555555")
ws2["A3"].alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[3].height = 18

ws2.merge_cells("A4:I4")
ws2["A4"] = "Requisito Legal Estricto: Obligación ineludible de emitir una locución informativa previa de mínimo 8 segundos + 3 segundos de gracia para colgar sin cargo."
ws2["A4"].font = Font(name="Calibri", size=9, bold=True, color="C62828")
ws2["A4"].alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[4].height = 18

# Table Headers
headers_ws2 = [
    "Nº", "Municipio / Entidad Local", "Código INE", "Población",
    "Estado en Modalidad B", "Causa Administrativa y Técnica",
    "Régimen Real en Vigor", "Coste al Ciudadano", "Observaciones Oficiales"
]
ws2.row_dimensions[6].height = 28
for col_idx, h_text in enumerate(headers_ws2, 1):
    cell = ws2.cell(row=6, column=col_idx, value=h_text)
    cell.font = font_tbl_header
    cell.fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = header_border

# Data Row for Modalidad B (Explanatory real status)
data_ws2 = [
    (1, "Ningún ayuntamiento de la Comunidad de Madrid aplica actualmente la Modalidad B", "-", 0,
     "0 Municipios Adheridos", "Rechazo unánime al sobrecoste del establecimiento doble y dificultad operativa de la locución previa obligatoria de 8+3 segundos",
     "Los consistorios madrileños han optado por Modalidad A (coste ordinario) o Modalidad C (100% gratuito)", "0,00 € (Sin aplicación)",
     "La Modalidad B es una figura legal regulada en el BOE pero sin implementación práctica en la Comunidad de Madrid.")
]

start_row_ws2 = 7
for idx, row_data in enumerate(data_ws2):
    curr_row = start_row_ws2 + idx
    ws2.row_dimensions[curr_row].height = 30
    for c_idx, val in enumerate(row_data, 1):
        cell = ws2.cell(row=curr_row, column=c_idx, value=val)
        cell.font = font_data
        cell.border = thin_border
        if c_idx in (1, 3, 5):
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx == 4:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif c_idx == 5:
            cell.font = font_alert
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

end_row_ws2 = start_row_ws2 + len(data_ws2) - 1

# Total Row for Modalidad B
tot_row_ws2 = end_row_ws2 + 1
ws2.row_dimensions[tot_row_ws2].height = 24

ws2.cell(row=tot_row_ws2, column=1, value="")
ws2.cell(row=tot_row_ws2, column=2, value="TOTAL AYUNTAMIENTOS MODALIDAD B")
ws2.cell(row=tot_row_ws2, column=3, value=0)
ws2.cell(row=tot_row_ws2, column=4, value=0)
ws2.cell(row=tot_row_ws2, column=5, value="0 Municipios")
ws2.cell(row=tot_row_ws2, column=6, value="Sin consistorios en Modalidad B")
ws2.cell(row=tot_row_ws2, column=7, value="Total en la región: 0")
ws2.cell(row=tot_row_ws2, column=8, value="0,00 €")
ws2.cell(row=tot_row_ws2, column=9, value="Total Consistorios Modalidad B: 0")

for c_idx in range(1, 10):
    cell = ws2.cell(row=tot_row_ws2, column=c_idx)
    cell.font = font_total
    cell.fill = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    cell.border = total_border
    if c_idx in (1, 3, 4, 5):
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(horizontal="left", vertical="center")

# ==============================================================================
# HOJA 3: MODALIDAD C
# ==============================================================================
ws3 = wb.create_sheet(title="Modalidad C")
ws3.views.sheetView[0].showGridLines = True

# Title banner
ws3.merge_cells("A1:K1")
ws3["A1"] = "AYUNTAMIENTOS DE LA COMUNIDAD DE MADRID - MODALIDAD C (SERVICIO 010 GRATUITO)"
ws3["A1"].font = font_title
ws3["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 36

# Legal context & info notes
ws3.merge_cells("A2:K2")
ws3["A2"] = "Marco Normativo: Resolución de 31 de julio de 2013 (SETSI - BOE núm. 226/2013). Modalidad C de cobro revertido municipal."
ws3["A2"].font = Font(name="Calibri", size=10, bold=True, color="1B365D")
ws3["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[2].height = 20

ws3.merge_cells("A3:K3")
ws3["A3"] = "Régimen de Gratuidad Universal: La llamada al 010 es 100% GRATUITA para el ciudadano llamante (sin coste de establecimiento ni de minutos)."
ws3["A3"].font = Font(name="Calibri", size=9, bold=True, color="2E7D32")
ws3["A3"].alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[3].height = 18

ws3.merge_cells("A4:K4")
ws3["A4"] = "Financiación Municipal: El coste total del servicio y del tráfico telefónico es asumido íntegramente por el Ayuntamiento con cargo a sus presupuestos."
ws3["A4"].font = Font(name="Calibri", size=9, italic=True, color="555555")
ws3["A4"].alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[4].height = 18

# Table Headers
headers_ws3 = [
    "Nº", "Ayuntamiento / Municipio", "Código INE", "Población (Hab.)",
    "Número Corto Gratuito", "Modalidad 010", "Líneas Gratuitas Especiales (900)",
    "Número Geográfico Alternativo (Prefijo 91)", "Fecha de Gratuidad",
    "Horario de Atención", "Financiación y Sede Oficial"
]
ws3.row_dimensions[6].height = 28
for col_idx, h_text in enumerate(headers_ws3, 1):
    cell = ws3.cell(row=6, column=col_idx, value=h_text)
    cell.font = font_tbl_header
    cell.fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = header_border

# Data Rows for Modalidad C
data_ws3 = [
    (1, "Madrid (Capital)", "28079", 3332035, "010 (100% Gratuito)", "Modalidad C",
     "900 111 065 (Gratuito preferente mayores 65 años)", "915 298 210 / 914 800 010 (Incluido tarifa plana)",
     "01/03/2019 (Decreto Gratuidad)", "24 horas al día, 365 días al año",
     "Financiado 100% Ayto. Madrid. Sede: https://sede.madrid.es"),
    (2, "Las Rozas de Madrid", "28127", 96634, "010 (100% Gratuito)", "Modalidad C",
     "900 153 856 (Gratuito desde fuera y móviles)", "91 757 90 05 / 91 771 40 00 (Incluido tarifa plana)",
     "En vigor (Ordenanza Atención)", "L-V 8:00 a 22:00 h; Sáb 8:00 a 20:00 h",
     "Financiado 100% Ayto. Las Rozas. Sede: https://sede.lasrozas.es")
]

start_row_ws3 = 7
for idx, row_data in enumerate(data_ws3):
    curr_row = start_row_ws3 + idx
    ws3.row_dimensions[curr_row].height = 24
    for c_idx, val in enumerate(row_data, 1):
        cell = ws3.cell(row=curr_row, column=c_idx, value=val)
        cell.font = font_data
        cell.border = thin_border
        if c_idx in (1, 3):
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx == 4:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = "#,##0"
        elif c_idx in (5, 6):
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = font_free
        elif c_idx == 11 and "https://" in str(val):
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

end_row_ws3 = start_row_ws3 + len(data_ws3) - 1

# Total Row for Modalidad C
tot_row_ws3 = end_row_ws3 + 1
ws3.row_dimensions[tot_row_ws3].height = 24

ws3.cell(row=tot_row_ws3, column=1, value="")
ws3.cell(row=tot_row_ws3, column=2, value="TOTAL AYUNTAMIENTOS MODALIDAD C")
ws3.cell(row=tot_row_ws3, column=3, value=f"=COUNTA(B{start_row_ws3}:B{end_row_ws3})")
ws3.cell(row=tot_row_ws3, column=4, value=f"=SUM(D{start_row_ws3}:D{end_row_ws3})")
ws3.cell(row=tot_row_ws3, column=5, value="2 Municipios")
ws3.cell(row=tot_row_ws3, column=6, value="Modalidad C")
ws3.cell(row=tot_row_ws3, column=7, value="Líneas 900 Gratuitas Habilitadas")
ws3.cell(row=tot_row_ws3, column=8, value="Alternativos Geográficos 91...")
ws3.cell(row=tot_row_ws3, column=9, value="100% Gratuito Ciudadano")
ws3.cell(row=tot_row_ws3, column=10, value="Atención Continua")
ws3.cell(row=tot_row_ws3, column=11, value="Total Consistorios Modalidad C: 2")

for c_idx in range(1, 12):
    cell = ws3.cell(row=tot_row_ws3, column=c_idx)
    cell.font = font_total
    cell.fill = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    cell.border = total_border
    if c_idx in (1, 3, 5, 6):
        cell.alignment = Alignment(horizontal="center", vertical="center")
    elif c_idx == 4:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = "#,##0"
    else:
        cell.alignment = Alignment(horizontal="left", vertical="center")

# ==============================================================================
# HOJA 4: AYUNTAMIENTOS GRATUITOS Y CANALES DE ATENCIÓN
# ==============================================================================
ws4 = wb.create_sheet(title="Ayuntamientos Gratuitos")
ws4.views.sheetView[0].showGridLines = True

# Title banner
ws4.merge_cells("A1:N1")
ws4["A1"] = "GUÍA INTEGRAL DE AYUNTAMIENTOS Y CANALES DE ATENCIÓN GRATUITOS EN LA COMUNIDAD DE MADRID"
ws4["A1"].font = font_title
ws4["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
ws4["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws4.row_dimensions[1].height = 36

# Subtitle / description
ws4.merge_cells("A2:N2")
ws4["A2"] = "Relación exhaustiva de los canales de contacto 100% gratuitos: teléfonos municipales sin coste (Modalidad C / 900), líneas geográficas provinciales (91...) incluidas en tarifa plana, WhatsApp, correo electrónico, sede electrónica 24/7 y oficinas presenciales."
ws4["A2"].font = Font(name="Calibri", size=10, italic=True, color="333333")
ws4["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws4.row_dimensions[2].height = 20

# Section 1 Header: Modalidad C / 900 Free Municipalities
ws4.merge_cells("A4:N4")
ws4["A4"] = "SECCIÓN 1: MUNICIPIOS CON SERVICIO TELEFÓNICO MUNICIPAL 100% GRATUITO (MODALIDAD C Y LÍNEAS 900)"
ws4["A4"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws4["A4"].fill = PatternFill(start_color=ACCENT_GREEN, end_color=ACCENT_GREEN, fill_type="solid")
ws4["A4"].alignment = Alignment(horizontal="left", vertical="center")
ws4.row_dimensions[4].height = 24

headers_sec1 = [
    "Municipio / Ayuntamiento", "Teléfono 010 Gratuito", "Línea 900 Gratuita",
    "Teléfono Geográfico (Tarifa Plana)", "Canal WhatsApp", "Chat Web en Directo",
    "Correo Electrónico Oficial", "Sede Electrónica (24/7)", "Portal Cita Previa",
    "Buzón / Incidencias", "App Móvil Oficial", "Redes Sociales",
    "Atención Presencial (Oficinas)", "Accesibilidad (LSE / Sordos)"
]

ws4.row_dimensions[5].height = 28
for col_idx, h_text in enumerate(headers_sec1, 1):
    cell = ws4.cell(row=5, column=col_idx, value=h_text)
    cell.font = font_tbl_header
    cell.fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = header_border

data_sec1 = [
    ("Madrid (Capital)",
     "010 (Gratis desde término municipal)",
     "900 111 065 (Gratuito mayores de 65 años 24h)",
     "915 298 210 / 914 800 010 (Incluido en tarifa plana nacional)",
     "620 954 010 (Asistente virtual Línea Madrid)",
     "Chat online en www.madrid.es",
     "linea.madrid@madrid.es / Formulario web",
     "https://sede.madrid.es",
     "https://madrid.es/citaprevia",
     "Sistema Avisos Madrid (avisos.madrid.es)",
     "App Madrid Móvil (iOS / Android)",
     "X / Twitter: @Lineamadrid",
     "26 Oficinas de Atención a la Ciudadanía (OAC) en los 21 distritos",
     "Videollamada en Lengua de Signos Española (LSE) en web y OAC"),
    ("Las Rozas de Madrid",
     "010 (Gratis desde el municipio)",
     "900 153 856 (Gratuito desde fuera y móviles)",
     "91 757 90 05 / 91 771 40 00 (Incluido en tarifa plana nacional)",
     "Canal WhatsApp de avisos e incidencias",
     "Formulario de consulta en lasrozas.es",
     "010@lasrozas.es / incidencias.010@lasrozas.es",
     "https://sede.lasrozas.es",
     "https://lasrozas.es/cita-previa",
     "Buzón del Vecino y portal de incidencias",
     "App municipal 'Las Rozas'",
     "X / Twitter: @Ayto_Las_Rozas",
     "Concejalía Atención Ciudadana (C/ Kálamos 32 y El Cantizal)",
     "Puntos de atención adaptados para personas con discapacidad")
]

for idx, r_data in enumerate(data_sec1):
    r_idx = 6 + idx
    ws4.row_dimensions[r_idx].height = 24
    for c_idx, val in enumerate(r_data, 1):
        cell = ws4.cell(row=r_idx, column=c_idx, value=val)
        cell.font = font_data
        cell.border = thin_border
        cell.fill = PatternFill(start_color=LIGHT_GREEN, end_color=LIGHT_GREEN, fill_type="solid")
        if c_idx in (8, 9):
            cell.font = font_link
        cell.alignment = Alignment(horizontal="left", vertical="center")

# Section 2 Header: Free Channels in Other Major Madrid Municipalities
ws4.merge_cells("A9:N9")
ws4["A9"] = "SECCIÓN 2: CANALES DE CONTACTO GRATUITOS Y SIN SOBRECOSTE EN EL RESTO DE MUNICIPIOS DE MADRID (VÍA PREFIJO 91... EN TARIFA PLANA Y SEDE ELECTRÓNICA)"
ws4["A9"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws4["A9"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
ws4["A9"].alignment = Alignment(horizontal="left", vertical="center")
ws4.row_dimensions[9].height = 24

headers_sec2 = [
    "Municipio / Ayuntamiento", "Teléfono Geográfico Gratuito (en Tarifa Plana)",
    "Canal WhatsApp Municipal", "Correo Electrónico de Atención",
    "Sede Electrónica Oficial (24/7)", "Canal de Cita Previa",
    "Buzón Ciudadano / Incidencias", "Atención Presencial (SAC)",
    "Población (Hab.)", "Situación del Teléfono 010",
    "Horario de Atención", "Recomendación para Evitar Costes", "", ""
]

ws4.row_dimensions[10].height = 28
for col_idx, h_text in enumerate(headers_sec2[:12], 1):
    cell = ws4.cell(row=10, column=col_idx, value=h_text)
    cell.font = font_tbl_header
    cell.fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = header_border

# 22 other major municipalities
data_sec2 = [
    ("Móstoles", "91 647 17 10 / 91 664 75 00", "No habilitado", "sac@mostoles.es", "https://sede.mostoles.es", "https://mostoles.es/citaprevia", "Buzón Ciudadano web", "SAC Plaza de España, 1", 211265, "010 de Pago (Mod. A)", "L-V 8:00 a 20:00 h", "Marcar siempre 91 647 17 10 en vez de 010"),
    ("Alcalá de Henares", "91 880 28 11 / 91 888 33 00", "No habilitado", "010@ayto-alcaladehenares.es", "https://sede.ayto-alcaladehenares.es", "Cita previa telemática", "Buzón en web municipal", "SAC Plaza de Cervantes, 12", 199184, "010 de Pago (Mod. A)", "L-V 8:00 a 14:00 h", "Marcar 91 880 28 11 para no pagar por 010"),
    ("Leganés", "91 248 90 10 / 91 248 90 00", "No habilitado", "uac@leganes.org", "https://sede.leganes.org", "Cita previa en sede", "Buzón de quejas online", "SAC Plaza Mayor, 1", 190665, "010 de Pago (Mod. A)", "L-V 8:30 a 14:30 h", "Marcar 91 248 90 10 incluido en tarifa plana"),
    ("Fuenlabrada", "91 649 70 10", "No habilitado", "info010@ayto-fuenlabrada.es", "https://sede.ayto-fuenlabrada.es", "Cita previa en sede", "Portal de avisos urbanos", "SAC Plaza de la Constitución, 1", 189891, "010 de Pago (Mod. A)", "L-V 8:30 a 19:00 h", "Marcar 91 649 70 10 en lugar de 010"),
    ("Alcorcón", "91 664 81 00", "No habilitado", "info@ayto-alcorcon.es", "https://sede.ayto-alcorcon.es", "Cita previa en sede", "Buzón de sugerencias web", "SAC Plaza de España, 1", 171772, "010 de Pago (Mod. A)", "L-V 8:30 a 14:30 h", "Marcar 91 664 81 00 incluido en tarifa plana"),
    ("Getafe", "91 202 79 11 / 91 202 79 00", "No habilitado", "atencionciudadana@ayto-getafe.org", "https://sede.getafe.es", "https://getafe.es/cita-previa", "Portal de avisos e incidencias", "SAC Plaza de la Constitución, 1", 185816, "Sin 010 (Atención 100% por fijo 91)", "L-J 9:00-19:00, V 9:00-14:00", "Siempre gratuito llamando al 91 202 79 11"),
    ("Torrejón de Ardoz", "91 678 95 00", "No habilitado", "estadistica@ayto-torrejon.es", "https://sede.ayto-torrejon.es", "Cita previa en sede", "Portal de incidencias urbanas", "SAC Plaza Mayor, 1", 137711, "010 de Pago (Mod. A)", "L-V 8:30 a 14:00 h", "Marcar 91 678 95 00 incluido en tarifa plana"),
    ("Parla", "91 624 03 00", "No habilitado", "sac@ayuntamientoparla.es", "https://sede.ayuntamientoparla.es", "Cita previa en sede", "Buzón ciudadano en web", "SAC Plaza de la Constitución, 1", 133004, "010 de Pago (Mod. A)", "L-V 8:00 a 14:30 h", "Marcar 91 624 03 00 incluido en tarifa plana"),
    ("Alcobendas", "91 296 90 88", "No habilitado", "atencionciudadana@alcobendas.org", "https://sede.alcobendas.org", "Cita previa en web SAC", "Portal de quejas y sugerencias", "SAC Plaza Mayor, 1", 119496, "010 de Pago (Mod. A)", "L-V 8:30-14:30 / 16:00-19:00", "Marcar 91 296 90 88 sin sobrecoste"),
    ("Rivas-Vaciamadrid", "91 670 00 00", "No habilitado", "siac@rivasciudad.es", "https://sede.rivasciudad.es", "Cita previa SIAC web", "Portal Rivas Ciudad Avisos", "SIAC Plaza de la Constitución, 1", 100270, "010 de Pago (Mod. A)", "L-V 8:00 a 20:00 h", "Marcar 91 670 00 00 incluido en tarifa plana"),
    ("San Sebastián de los Reyes", "91 659 71 00 / 91 625 88 55", "No habilitado", "sac@ssreyes.org", "https://sede.ssreyes.org", "Cita previa en sede", "Buzón ciudadano online", "SAC Plaza de la Constitución, 1", 92734, "010 de Pago (Mod. A)", "L-V 8:30 a 14:30 h", "Marcar 91 659 71 00 sin recargo telefónico"),
    ("Pozuelo de Alarcón", "91 217 14 92", "No habilitado", "atencionalciudadano@pozuelodealarcon.org", "https://sede.pozuelodealarcon.org", "Cita previa en sede", "Portal de incidencias web", "SAC Plaza Mayor, 1", 88784, "010 de Pago (Mod. A)", "L-V 8:00-20:00, S 9:00-14:00", "Marcar 91 217 14 92 gratuito en tarifa plana"),
    ("Coslada", "91 627 82 00", "676 76 53 07", "informacion@ayto-coslada.es", "https://sede.ayto-coslada.es", "Cita previa en web", "Buzón de incidencias web", "SAC Av. Constitución, 47", 81390, "Sin 010 (Atención por 91 y WhatsApp)", "L-V 8:30 a 14:00 h", "Atención telefónica gratuita vía 91 y WhatsApp"),
    ("Valdemoro", "91 809 98 90", "No habilitado", "ciudadano@valdemoro.es", "https://sede.valdemoro.es", "Cita previa en web", "Buzón del Ciudadano web", "SAC Plaza de la Constitución, 11", 81394, "Sin 010 (Atención directa por fijo 91)", "L-V 8:30 a 14:00 h", "Llamada ordinaria incluida en tarifa plana"),
    ("Majadahonda", "91 634 91 00", "No habilitado", "atencionciudadana@majadahonda.org", "https://sede.majadahonda.org", "Cita previa en sede", "Buzón de sugerencias online", "SAC Plaza Mayor, 3", 72548, "Sin 010 (Centralita telefónica fija)", "L-V 8:30 a 14:30 h", "Llamada sin coste extra vía 91 634 91 00"),
    ("Collado Villalba", "91 856 28 50", "No habilitado", "sac@ayto-colladovillalba.org", "https://sede.colladovillalba.es", "Cita previa en web", "Portal de quejas y avisos", "SAC Plaza de la Constitución, 1", 65654, "Sin 010 (Atención directa por 91)", "L-V 8:30 a 14:00 h", "Llamada ordinaria sin sobrecoste"),
    ("Boadilla del Monte", "91 634 93 00", "No habilitado", "registro@ayuntamientoboadilladelmonte.org", "https://sede.ayuntamientoboadilladelmonte.org", "Cita previa en web", "Buzón de quejas online", "SAC C/ Juan Carlos I, 42", 64742, "010 de Pago (Mod. A)", "L-V 9:00 a 14:30 h", "Marcar 91 634 93 00 incluido en tarifa plana"),
    ("Aranjuez", "91 892 43 86 / 91 809 03 60", "No habilitado", "sac@aranjuez.es", "https://sede.aranjuez.es", "Cita previa en web", "Buzón de reclamaciones web", "SAC Plaza de la Constitución, s/n", 60668, "Sin 010 (Atención directa por 91)", "L-V 8:30 a 14:00 h", "Llamada ordinaria incluida en tarifa plana"),
    ("Arganda del Rey", "91 871 13 44", "No habilitado", "atencionciudadana@ayto-arganda.es", "https://sede.ayto-arganda.es", "Cita previa en web", "Buzón del Ciudadano web", "SAC Plaza de la Constitución, 1", 57553, "010 de Pago (Mod. A)", "L-V 8:30 a 19:30 h", "Marcar 91 871 13 44 sin coste de 010"),
    ("Pinto", "91 248 37 00", "No habilitado", "sac@ayto-pinto.es", "https://sede.ayto-pinto.es", "Cita previa en web", "Buzón ciudadano online", "SAC Plaza de la Constitución, 1", 55209, "010 en Anexo / Uso preferente 91", "L-V 8:00 a 15:00 h", "Marcar 91 248 37 00 sin recargo"),
    ("Colmenar Viejo", "91 845 00 53", "No habilitado", "atencionciudadana@colmenarviejo.com", "https://sede.colmenarviejo.com", "Cita previa en web", "Buzón de sugerencias online", "SAC Plaza del Pueblo, 1", 55198, "Sin 010 (Atención directa por 91)", "L-V 8:30 a 14:00 h", "Llamada sin coste extra vía 91 845 00 53"),
    ("Tres Cantos", "91 293 80 00 / 91 188 33 00", "No habilitado", "sac@trescantos.es", "https://sede.trescantos.es", "Cita previa en web", "Buzón Ciudadano web", "SAC Plaza del Ayuntamiento, 1", 51453, "Cancelado 010 (BOE-A-2020-17260)", "L-V 8:30 a 14:00 h", "Atención telefónica gratuita vía fijo provincial")
]

start_r_sec2 = 11
for idx, r_data in enumerate(data_sec2):
    curr_row = start_r_sec2 + idx
    ws4.row_dimensions[curr_row].height = 20
    is_alt = (idx % 2 == 1)
    fill_row = PatternFill(start_color=LIGHT_BLUE, end_color=LIGHT_BLUE, fill_type="solid") if is_alt else PatternFill(fill_type=None)

    for c_idx, val in enumerate(r_data, 1):
        cell = ws4.cell(row=curr_row, column=c_idx, value=val)
        cell.font = font_data
        cell.border = thin_border
        if is_alt:
            cell.fill = fill_row
        
        if c_idx == 1:
            cell.font = font_data_bold
            cell.alignment = Alignment(horizontal="left", vertical="center")
        elif c_idx in (5, 6):
            if "https://" in str(val):
                cell.font = font_link
            cell.alignment = Alignment(horizontal="left", vertical="center")
        elif c_idx == 9:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = "#,##0"
        elif c_idx == 10:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if "Gratis" in str(val) or "Cancelado" in str(val) or "Sin 010" in str(val):
                cell.font = font_free
            else:
                cell.font = font_alert
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

end_r_sec2 = start_r_sec2 + len(data_sec2) - 1

# Total Summary Row for Sheet 4
tot_row_ws4 = end_r_sec2 + 1
ws4.row_dimensions[tot_row_ws4].height = 26

ws4.cell(row=tot_row_ws4, column=1, value="TOTAL MUNICIPIOS CATALOGADOS")
ws4.cell(row=tot_row_ws4, column=2, value="24 Grandes Municipios de la CAM")
ws4.cell(row=tot_row_ws4, column=3, value="100% Canales Fijos Sin Sobrecoste")
ws4.cell(row=tot_row_ws4, column=4, value="100% Vías de Contacto Gratuito")
ws4.cell(row=tot_row_ws4, column=5, value="100% con Sede Electrónica Gratuita")
ws4.cell(row=tot_row_ws4, column=6, value="100% con Cita Previa Online")
ws4.cell(row=tot_row_ws4, column=7, value="100% con Buzón / Incidencias")
ws4.cell(row=tot_row_ws4, column=8, value="100% con SAC Presencial")
ws4.cell(row=tot_row_ws4, column=9, value=f"=SUM(I{start_r_sec2}:I{end_r_sec2}) + D7 + D8")
ws4.cell(row=tot_row_ws4, column=10, value="2 con 010 C / 15 con 010 A / 7 con Fijo Directo")
ws4.cell(row=tot_row_ws4, column=11, value="Cobertura > 90% población CAM")
ws4.cell(row=tot_row_ws4, column=12, value="Garantía de Acceso Gratuito")

for c_idx in range(1, 13):
    cell = ws4.cell(row=tot_row_ws4, column=c_idx)
    cell.font = font_total
    cell.fill = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    cell.border = total_border
    if c_idx == 9:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = "#,##0"
    elif c_idx in (1, 2, 3, 4):
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(horizontal="left", vertical="center")

# ==============================================================================
# AUTO-FIT COLUMN WIDTHS ACROSS ALL SHEETS
# ==============================================================================
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        # Check non-merged cells from row 5 onwards
        for cell in col:
            if cell.row < 5:
                continue
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        # Apply padding
        sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

# Specific tweaks for sheet 4
ws4.column_dimensions["A"].width = 24
ws4.column_dimensions["B"].width = 30
ws4.column_dimensions["C"].width = 26
ws4.column_dimensions["D"].width = 32
ws4.column_dimensions["E"].width = 24
ws4.column_dimensions["F"].width = 26
ws4.column_dimensions["G"].width = 32
ws4.column_dimensions["H"].width = 32
ws4.column_dimensions["I"].width = 26
ws4.column_dimensions["J"].width = 30
ws4.column_dimensions["K"].width = 28
ws4.column_dimensions["L"].width = 30
ws4.column_dimensions["M"].width = 32
ws4.column_dimensions["N"].width = 32

# Save intermediate XLSX
xlsx_path = "/home/bender/Descargas/Ayuntamientos_Madrid_Modalidades_010_y_Canales_Gratuitos.xlsx"
ods_path = "/home/bender/Descargas/Ayuntamientos_Madrid_Modalidades_010_y_Canales_Gratuitos.ods"

wb.save(xlsx_path)
print(f"XLSX saved successfully at: {xlsx_path}")
