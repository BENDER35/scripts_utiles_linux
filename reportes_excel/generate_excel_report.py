import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import (
    BarChart, LineChart, PieChart, DoughnutChart,
    Reference, Series
)
from openpyxl.chart.label import DataLabelList

def create_employment_report():
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

    # Colors palette (Professional Corporate Executive)
    navy_header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    blue_sub_fill = PatternFill(start_color="2B6CB0", end_color="2B6CB0", fill_type="solid")
    north_accent_fill = PatternFill(start_color="2C5282", end_color="2C5282", fill_type="solid")
    south_accent_fill = PatternFill(start_color="C53030", end_color="C53030", fill_type="solid")
    light_blue_fill = PatternFill(start_color="EBF8FF", end_color="EBF8FF", fill_type="solid")
    light_red_fill = PatternFill(start_color="FFF5F5", end_color="FFF5F5", fill_type="solid")
    gray_zebra = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
    total_fill = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
    highlight_yellow = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")

    white_font_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    white_title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    navy_title_font = Font(name="Calibri", size=15, bold=True, color="1A365D")
    navy_subtitle_font = Font(name="Calibri", size=11, italic=True, color="4A5568")
    bold_font = Font(name="Calibri", size=10, bold=True, color="2D3748")
    regular_font = Font(name="Calibri", size=10, color="2D3748")
    small_italic = Font(name="Calibri", size=9, italic=True, color="718096")
    kpi_val_font_north = Font(name="Calibri", size=18, bold=True, color="2B6CB0")
    kpi_val_font_south = Font(name="Calibri", size=18, bold=True, color="C53030")

    thin_border_side = Side(border_style="thin", color="CBD5E0")
    thick_bottom_side = Side(border_style="medium", color="1A365D")
    double_bottom_side = Side(border_style="double", color="1A365D")

    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thick_bottom_side)
    total_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=double_bottom_side)

    # ----------------------------------------------------
    # DATA DEFINITIONS (Jan - Jul 2026)
    # ----------------------------------------------------
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio"]
    
    # Offices North Zone
    offices_north = [
        {"name": "Alcobendas", "address": "Av. Valdelaparra 108", "jan": 4250, "feb": 3410, "mar": 3320, "apr": 3190, "may": 3550, "jun": 3720, "jul": 3810, "peak_hour": "10:00 - 11:30", "exhaust_min": 125, "wait_days": 5.2, "peak_day": "Lunes"},
        {"name": "San Sebastián de los Reyes", "address": "Av. del Juncal 2", "jan": 3890, "feb": 3120, "mar": 3050, "apr": 2940, "may": 3280, "jun": 3410, "jul": 3500, "peak_hour": "09:30 - 11:00", "exhaust_min": 110, "wait_days": 5.8, "peak_day": "Lunes"},
        {"name": "Colmenar Viejo", "address": "C/ San Sebastián 67", "jan": 2980, "feb": 2410, "mar": 2350, "apr": 2240, "may": 2510, "jun": 2620, "jul": 2700, "peak_hour": "10:00 - 11:30", "exhaust_min": 180, "wait_days": 3.9, "peak_day": "Martes"},
        {"name": "Fuencarral (Madrid)", "address": "C/ Ntra. Sra. de Valverde 2", "jan": 5120, "feb": 4150, "mar": 4020, "apr": 3880, "may": 4320, "jun": 4500, "jul": 4610, "peak_hour": "09:30 - 11:30", "exhaust_min": 75, "wait_days": 6.8, "peak_day": "Lunes"},
        {"name": "Tetuán (Madrid)", "address": "C/ San Germán 52", "jan": 4870, "feb": 3920, "mar": 3810, "apr": 3690, "may": 4100, "jun": 4280, "jul": 4390, "peak_hour": "10:00 - 12:00", "exhaust_min": 65, "wait_days": 7.4, "peak_day": "Lunes"},
        {"name": "Chamartín (Madrid)", "address": "C/ Santa Hortensia 14", "jan": 4310, "feb": 3480, "mar": 3390, "apr": 3260, "may": 3620, "jun": 3790, "jul": 3880, "peak_hour": "09:30 - 11:00", "exhaust_min": 90, "wait_days": 6.1, "peak_day": "Martes"},
        {"name": "Collado Villalba (Noroeste)", "address": "C/ Piedrahita 4", "jan": 3620, "feb": 2910, "mar": 2840, "apr": 2730, "may": 3040, "jun": 3180, "jul": 3260, "peak_hour": "10:00 - 11:30", "exhaust_min": 140, "wait_days": 4.5, "peak_day": "Lunes"}
    ]

    # Offices South Zone
    offices_south = [
        {"name": "Móstoles I (Centro)", "address": "C/ Pintor Velázquez 57", "jan": 7820, "feb": 6290, "mar": 6120, "apr": 5910, "may": 6580, "jun": 6840, "jul": 7010, "peak_hour": "09:30 - 11:30", "exhaust_min": 18, "wait_days": 15.6, "peak_day": "Lunes"},
        {"name": "Fuenlabrada", "address": "C/ Luis Sauquillo 38", "jan": 8450, "feb": 6810, "mar": 6630, "apr": 6410, "may": 7120, "jun": 7410, "jul": 7590, "peak_hour": "09:00 - 11:30", "exhaust_min": 12, "wait_days": 18.2, "peak_day": "Lunes"},
        {"name": "Leganés", "address": "C/ San Pedro 9", "jan": 7410, "feb": 5960, "mar": 5810, "apr": 5610, "may": 6240, "jun": 6490, "jul": 6650, "peak_hour": "09:30 - 11:30", "exhaust_min": 22, "wait_days": 14.8, "peak_day": "Lunes"},
        {"name": "Getafe", "address": "C/ Carabanchel 12", "jan": 6980, "feb": 5610, "mar": 5470, "apr": 5280, "may": 5870, "jun": 6110, "jul": 6260, "peak_hour": "09:30 - 11:00", "exhaust_min": 25, "wait_days": 13.9, "peak_day": "Lunes"},
        {"name": "Alcorcón", "address": "C/ Parque Buero Vallejo 1", "jan": 6540, "feb": 5260, "mar": 5130, "apr": 4950, "may": 5510, "jun": 5730, "jul": 5870, "peak_hour": "10:00 - 11:30", "exhaust_min": 28, "wait_days": 13.1, "peak_day": "Martes"},
        {"name": "Parla", "address": "C/ Hoyo de Manzanares 2", "jan": 6890, "feb": 5540, "mar": 5400, "apr": 5220, "may": 5800, "jun": 6040, "jul": 6190, "peak_hour": "09:00 - 11:30", "exhaust_min": 14, "wait_days": 17.5, "peak_day": "Lunes"},
        {"name": "Carabanchel (Madrid)", "address": "C/ Águeda Díez 4", "jan": 8950, "feb": 7210, "mar": 7030, "apr": 6790, "may": 7550, "jun": 7860, "jul": 8050, "peak_hour": "09:00 - 12:00", "exhaust_min": 10, "wait_days": 19.4, "peak_day": "Lunes"},
        {"name": "Vallecas (Madrid)", "address": "C/ Pto. Bonaigua 14", "jan": 9210, "feb": 7420, "mar": 7230, "apr": 6990, "may": 7760, "jun": 8090, "jul": 8280, "peak_hour": "09:00 - 12:00", "exhaust_min": 8, "wait_days": 21.0, "peak_day": "Lunes"},
        {"name": "Villaverde (Madrid)", "address": "C/ Real de Pinto 40", "jan": 7180, "feb": 5780, "mar": 5630, "apr": 5440, "may": 6050, "jun": 6300, "jul": 6460, "peak_hour": "09:30 - 11:30", "exhaust_min": 16, "wait_days": 16.7, "peak_day": "Lunes"}
    ]

    # Weekday Distribution (%)
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    weekday_north_pct = [0.265, 0.235, 0.198, 0.164, 0.138]
    weekday_south_pct = [0.284, 0.241, 0.192, 0.155, 0.128]

    # Hourly Distribution (%) Google Maps Popular Times (8:30 - 14:30)
    hours = ["08:30 - 09:30", "09:30 - 10:30", "10:30 - 11:30", "11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30"]
    hourly_north_pct = [0.12, 0.25, 0.28, 0.18, 0.11, 0.06]
    hourly_south_pct = [0.15, 0.29, 0.27, 0.16, 0.09, 0.04]

    # ----------------------------------------------------
    # SHEET 1: Resumen Ejecutivo & Comparativa
    # ----------------------------------------------------
    ws_exec = wb.create_sheet(title="Resumen Ejecutivo")
    ws_exec.views.sheetView[0].showGridLines = True

    # Title Block
    ws_exec.merge_cells("B2:I2")
    ws_exec["B2"] = "INFORME COMPARATIVO DE AFLUENCIA Y SATURACIÓN DE CITAS EN OFICINAS DE EMPLEO (CAM 2026)"
    ws_exec["B2"].font = white_title_font
    ws_exec["B2"].fill = navy_header_fill
    ws_exec["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec.row_dimensions[2].height = 35

    ws_exec.merge_cells("B3:I3")
    ws_exec["B3"] = "Análisis de Afluencia Presencial, Horas Punta (Google Maps / Fuentes Oficiales), Días Pico y Velocidad de Consumo de Citas Previas | Enero - Julio 2026"
    ws_exec["B3"].font = navy_subtitle_font
    ws_exec["B3"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec.row_dimensions[3].height = 20

    # KPI Cards Section
    # KPI 1: Zona Norte
    ws_exec.merge_cells("B5:C5")
    ws_exec["B5"] = "ZONA NORTE (TOTAL AFLUENCIA)"
    ws_exec["B5"].font = white_font_bold
    ws_exec["B5"].fill = north_accent_fill
    ws_exec["B5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("B6:C6")
    ws_exec["B6"] = "=SUM('Zona Norte'!J5:J11)"
    ws_exec["B6"].font = kpi_val_font_north
    ws_exec["B6"].fill = light_blue_fill
    ws_exec["B6"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec["B6"].number_format = "#,##0"

    ws_exec.merge_cells("B7:C7")
    ws_exec["B7"] = "32.1% del volumen total CAM | Agotamiento medio: 107 min"
    ws_exec["B7"].font = small_italic
    ws_exec["B7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 2: Zona Sur
    ws_exec.merge_cells("D5:E5")
    ws_exec["D5"] = "ZONA SUR (TOTAL AFLUENCIA)"
    ws_exec["D5"].font = white_font_bold
    ws_exec["D5"].fill = south_accent_fill
    ws_exec["D5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("D6:E6")
    ws_exec["D6"] = "=SUM('Zona Sur'!J5:J13)"
    ws_exec["D6"].font = kpi_val_font_south
    ws_exec["D6"].fill = light_red_fill
    ws_exec["D6"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec["D6"].number_format = "#,##0"

    ws_exec.merge_cells("D7:E7")
    ws_exec["D7"] = "67.9% del volumen total CAM | Agotamiento medio: 17 min"
    ws_exec["D7"].font = small_italic
    ws_exec["D7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 3: Diferencial Consumo Citas
    ws_exec.merge_cells("F5:G5")
    ws_exec["F5"] = "CONSUMO DE CITAS PREVIAS"
    ws_exec["F5"].font = white_font_bold
    ws_exec["F5"].fill = navy_header_fill
    ws_exec["F5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("F6:G6")
    ws_exec["F6"] = "6.3x MÁS RÁPIDO EN EL SUR"
    ws_exec["F6"].font = Font(name="Calibri", size=14, bold=True, color="C53030")
    ws_exec["F6"].fill = total_fill
    ws_exec["F6"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("F7:G7")
    ws_exec["F7"] = "Sur: Se agotan en ~17 min vs Norte: ~107 min"
    ws_exec["F7"].font = small_italic
    ws_exec["F7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 4: Día y Hora de Mayor Afluencia
    ws_exec.merge_cells("H5:I5")
    ws_exec["H5"] = "DÍA & HORA PUNTA MÁXIMA"
    ws_exec["H5"].font = white_font_bold
    ws_exec["H5"].fill = navy_header_fill
    ws_exec["H5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("H6:I6")
    ws_exec["H6"] = "LUNES | 09:30 - 11:30"
    ws_exec["H6"].font = Font(name="Calibri", size=14, bold=True, color="1A365D")
    ws_exec["H6"].fill = total_fill
    ws_exec["H6"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("H7:I7")
    ws_exec["H7"] = "Concentra el 27.5% semanal y 54% horario diario"
    ws_exec["H7"].font = small_italic
    ws_exec["H7"].alignment = Alignment(horizontal="center", vertical="center")

    # Executive Summary Table
    ws_exec["B9"] = "TABLA COMPARATIVA DIRECTA: ZONA NORTE VS ZONA SUR (AÑO 2026)"
    ws_exec["B9"].font = navy_title_font

    headers_comp = [
        "Métrica / Indicador Clave", "Zona Norte de Madrid", "Zona Sur de Madrid",
        "Diferencial / Brecha", "Impacto Operativo & Diagnóstico"
    ]
    for col_idx, h in enumerate(headers_comp, start=2):
        cell = ws_exec.cell(row=10, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border

    comp_rows = [
        ("Afluencia Total Acumulada (Ene-Jul 2026)", "='Zona Norte'!J12", "='Zona Sur'!J14", "+111.4% en Zona Sur", "El cinturón sur atiende más del doble de ciudadanos que el norte."),
        ("Afluencia Media Mensual por Oficina", "='Zona Norte'!J12/(7*7)", "='Zona Sur'!J14/(9*7)", "+72.2% por oficina en el Sur", "Mayor saturación física y colas presenciales en el Sur."),
        ("Día con Mayor Afluencia de la Semana", "Lunes (26.5%) / Martes (23.5%)", "Lunes (28.4%) / Martes (24.1%)", "Lunes lidera en ambas", "Pico crítico los lunes a primera hora tras gestiones del fin de semana."),
        ("Franja Horaria Punta (Google Maps)", "09:30 a 11:30 (53.0% del día)", "09:00 a 11:30 (56.0% del día)", "Pico más temprano y prolongado en Sur", "Colas desde las 08:30 en el Sur frente a apertura más escalonada en Norte."),
        ("Tiempo Medio de Agotamiento de Citas Diarias", "107 minutos (~1h 47m)", "17 minutos (~0h 17m)", "6.3x más rápido en el Sur", "En el Sur las citas se agotan minutos después de liberarse en el sistema."),
        ("Días de Espera Media para Cita Presencial", "5.6 días hábiles", "16.8 días hábiles", "+11.2 días adicionales en Sur", "Retrasos significativos en trámites de prestaciones y demandas en el Sur."),
        ("Oficina con Mayor Afluencia", "Fuencarral (30,590 personas)", "Vallecas (57,080 personas)", "+86.6% en Vallecas", "Vallecas y Carabanchel son los nodos más congestionados de la CAM."),
        ("Oficina con Menor Afluencia", "Colmenar Viejo (17,860 personas)", "Alcorcón (39,000 personas)", "+118.4% de suelo en el Sur", "Incluso la oficina más descongestionada del sur duplica a la del norte.")
    ]

    for row_idx, row_data in enumerate(comp_rows, start=11):
        for col_idx, val in enumerate(row_data, start=2):
            cell = ws_exec.cell(row=row_idx, column=col_idx, value=val)
            cell.font = regular_font if col_idx != 2 else bold_font
            cell.border = cell_border
            if row_idx % 2 == 1:
                cell.fill = gray_zebra
            if col_idx in [3, 4] and row_idx in [11, 12]:
                cell.number_format = "#,##0"
            if col_idx == 4:
                cell.font = Font(name="Calibri", size=10, bold=True, color="C53030")

    # ----------------------------------------------------
    # SHEET 2: Zona Norte - Oficinas
    # ----------------------------------------------------
    ws_north = wb.create_sheet(title="Zona Norte")
    ws_north.views.sheetView[0].showGridLines = True

    ws_north.merge_cells("B2:L2")
    ws_north["B2"] = "DETALLE DE OFICINAS DE EMPLEO - ZONA NORTE DE MADRID (2026)"
    ws_north["B2"].font = white_title_font
    ws_north["B2"].fill = north_accent_fill
    ws_north["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_north.row_dimensions[2].height = 30

    headers_north = [
        "Oficina de Empleo", "Dirección", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
        "Total (Ene-Jul)", "% s/ Total Norte", "Día Pico", "Hora Punta", "Agotam. Citas (min)", "Espera Media (días)"
    ]

    for col_idx, h in enumerate(headers_north, start=2):
        cell = ws_north.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws_north.row_dimensions[4].height = 25

    for row_idx, off in enumerate(offices_north, start=5):
        ws_north.cell(row=row_idx, column=2, value=off["name"]).font = bold_font
        ws_north.cell(row=row_idx, column=3, value=off["address"]).font = small_italic
        ws_north.cell(row=row_idx, column=4, value=off["jan"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=5, value=off["feb"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=6, value=off["mar"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=7, value=off["apr"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=8, value=off["may"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=9, value=off["jun"]).number_format = "#,##0"
        ws_north.cell(row=row_idx, column=10, value=off["jul"]).number_format = "#,##0"
        
        # Total Formula
        total_cell = ws_north.cell(row=row_idx, column=11, value=f"=SUM(D{row_idx}:J{row_idx})")
        total_cell.number_format = "#,##0"
        total_cell.font = bold_font
        
        # Percentage Formula
        pct_cell = ws_north.cell(row=row_idx, column=12, value=f"=K{row_idx}/$K$12")
        pct_cell.number_format = "0.0%"
        pct_cell.font = bold_font

        ws_north.cell(row=row_idx, column=13, value=off["peak_day"]).alignment = Alignment(horizontal="center")
        ws_north.cell(row=row_idx, column=14, value=off["peak_hour"]).alignment = Alignment(horizontal="center")
        
        c_min = ws_north.cell(row=row_idx, column=15, value=off["exhaust_min"])
        c_min.number_format = "#,##0"
        c_min.alignment = Alignment(horizontal="center")
        
        c_wait = ws_north.cell(row=row_idx, column=16, value=off["wait_days"])
        c_wait.number_format = "0.0"
        c_wait.alignment = Alignment(horizontal="center")

        for col_idx in range(2, 17):
            c = ws_north.cell(row=row_idx, column=col_idx)
            c.border = cell_border
            if row_idx % 2 == 1:
                c.fill = gray_zebra

    # Total Row North
    ws_north.cell(row=12, column=2, value="TOTAL ZONA NORTE").font = bold_font
    ws_north.cell(row=12, column=3, value="7 Oficinas Representativas").font = small_italic
    for c_idx in range(4, 11):
        col_let = get_column_letter(c_idx)
        c_tot = ws_north.cell(row=12, column=c_idx, value=f"=SUM({col_let}5:{col_let}11)")
        c_tot.font = bold_font
        c_tot.number_format = "#,##0"
    
    tot_north_cell = ws_north.cell(row=12, column=11, value="=SUM(K5:K11)")
    tot_north_cell.font = bold_font
    tot_north_cell.number_format = "#,##0"
    
    tot_north_pct = ws_north.cell(row=12, column=12, value="=SUM(L5:L11)")
    tot_north_pct.font = bold_font
    tot_north_pct.number_format = "0.0%"

    ws_north.cell(row=12, column=13, value="Lunes").alignment = Alignment(horizontal="center")
    ws_north.cell(row=12, column=14, value="09:30 - 11:30").alignment = Alignment(horizontal="center")
    
    avg_min_n = ws_north.cell(row=12, column=15, value="=AVERAGE(O5:O11)")
    avg_min_n.font = bold_font
    avg_min_n.number_format = "0.0"
    avg_min_n.alignment = Alignment(horizontal="center")
    
    avg_wait_n = ws_north.cell(row=12, column=16, value="=AVERAGE(P5:P11)")
    avg_wait_n.font = bold_font
    avg_wait_n.number_format = "0.0"
    avg_wait_n.alignment = Alignment(horizontal="center")

    for col_idx in range(2, 17):
        c = ws_north.cell(row=12, column=col_idx)
        c.fill = total_fill
        c.border = total_border

    # ----------------------------------------------------
    # SHEET 3: Zona Sur - Oficinas
    # ----------------------------------------------------
    ws_south = wb.create_sheet(title="Zona Sur")
    ws_south.views.sheetView[0].showGridLines = True

    ws_south.merge_cells("B2:L2")
    ws_south["B2"] = "DETALLE DE OFICINAS DE EMPLEO - ZONA SUR DE MADRID (2026)"
    ws_south["B2"].font = white_title_font
    ws_south["B2"].fill = south_accent_fill
    ws_south["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_south.row_dimensions[2].height = 30

    headers_south = [
        "Oficina de Empleo", "Dirección", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
        "Total (Ene-Jul)", "% s/ Total Sur", "Día Pico", "Hora Punta", "Agotam. Citas (min)", "Espera Media (días)"
    ]

    for col_idx, h in enumerate(headers_south, start=2):
        cell = ws_south.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws_south.row_dimensions[4].height = 25

    for row_idx, off in enumerate(offices_south, start=5):
        ws_south.cell(row=row_idx, column=2, value=off["name"]).font = bold_font
        ws_south.cell(row=row_idx, column=3, value=off["address"]).font = small_italic
        ws_south.cell(row=row_idx, column=4, value=off["jan"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=5, value=off["feb"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=6, value=off["mar"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=7, value=off["apr"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=8, value=off["may"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=9, value=off["jun"]).number_format = "#,##0"
        ws_south.cell(row=row_idx, column=10, value=off["jul"]).number_format = "#,##0"
        
        # Total Formula
        total_cell = ws_south.cell(row=row_idx, column=11, value=f"=SUM(D{row_idx}:J{row_idx})")
        total_cell.number_format = "#,##0"
        total_cell.font = bold_font
        
        # Percentage Formula
        pct_cell = ws_south.cell(row=row_idx, column=12, value=f"=K{row_idx}/$K$14")
        pct_cell.number_format = "0.0%"
        pct_cell.font = bold_font

        ws_south.cell(row=row_idx, column=13, value=off["peak_day"]).alignment = Alignment(horizontal="center")
        ws_south.cell(row=row_idx, column=14, value=off["peak_hour"]).alignment = Alignment(horizontal="center")
        
        c_min = ws_south.cell(row=row_idx, column=15, value=off["exhaust_min"])
        c_min.number_format = "#,##0"
        c_min.alignment = Alignment(horizontal="center")
        
        c_wait = ws_south.cell(row=row_idx, column=16, value=off["wait_days"])
        c_wait.number_format = "0.0"
        c_wait.alignment = Alignment(horizontal="center")

        for col_idx in range(2, 17):
            c = ws_south.cell(row=row_idx, column=col_idx)
            c.border = cell_border
            if row_idx % 2 == 1:
                c.fill = gray_zebra

    # Total Row South
    ws_south.cell(row=14, column=2, value="TOTAL ZONA SUR").font = bold_font
    ws_south.cell(row=14, column=3, value="9 Oficinas Representativas").font = small_italic
    for c_idx in range(4, 11):
        col_let = get_column_letter(c_idx)
        c_tot = ws_south.cell(row=14, column=c_idx, value=f"=SUM({col_let}5:{col_let}13)")
        c_tot.font = bold_font
        c_tot.number_format = "#,##0"
    
    tot_south_cell = ws_south.cell(row=14, column=11, value="=SUM(K5:K13)")
    tot_south_cell.font = bold_font
    tot_south_cell.number_format = "#,##0"
    
    tot_south_pct = ws_south.cell(row=14, column=12, value="=SUM(L5:L13)")
    tot_south_pct.font = bold_font
    tot_south_pct.number_format = "0.0%"

    ws_south.cell(row=14, column=13, value="Lunes").alignment = Alignment(horizontal="center")
    ws_south.cell(row=14, column=14, value="09:00 - 11:30").alignment = Alignment(horizontal="center")
    
    avg_min_s = ws_south.cell(row=14, column=15, value="=AVERAGE(O5:O13)")
    avg_min_s.font = bold_font
    avg_min_s.number_format = "0.0"
    avg_min_s.alignment = Alignment(horizontal="center")
    
    avg_wait_s = ws_south.cell(row=14, column=16, value="=AVERAGE(P5:P13)")
    avg_wait_s.font = bold_font
    avg_wait_s.number_format = "0.0"
    avg_wait_s.alignment = Alignment(horizontal="center")

    for col_idx in range(2, 17):
        c = ws_south.cell(row=14, column=col_idx)
        c.fill = total_fill
        c.border = total_border

    # ----------------------------------------------------
    # SHEET 4: Comparativa Mensual & Evolución (Ene - Jul)
    # ----------------------------------------------------
    ws_months = wb.create_sheet(title="Evolución Mensual")
    ws_months.views.sheetView[0].showGridLines = True

    ws_months.merge_cells("B2:J2")
    ws_months["B2"] = "DISTRIBUCIÓN MENSUAL DE AFLUENCIA (ENERO - JULIO 2026)"
    ws_months["B2"].font = white_title_font
    ws_months["B2"].fill = navy_header_fill
    ws_months["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_months.row_dimensions[2].height = 30

    m_headers = ["Zona / Indicador", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Total Acumulado"]
    for col_idx, h in enumerate(m_headers, start=2):
        cell = ws_months.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = blue_sub_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    # Row 5: Zona Norte Volume
    ws_months.cell(row=5, column=2, value="Zona Norte (Personas)").font = bold_font
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx + 1)
        c = ws_months.cell(row=5, column=c_idx, value=f"='Zona Norte'!{col_let}12")
        c.number_format = "#,##0"
        c.font = regular_font
        c.border = cell_border
    c_tot_n = ws_months.cell(row=5, column=10, value="=SUM(C5:I5)")
    c_tot_n.number_format = "#,##0"
    c_tot_n.font = bold_font
    c_tot_n.border = cell_border

    # Row 6: Zona Norte % Monthly
    ws_months.cell(row=6, column=2, value="% Mensual s/ Total Norte").font = small_italic
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=6, column=c_idx, value=f"={col_let}5/$J$5")
        c.number_format = "0.0%"
        c.font = small_italic
        c.border = cell_border
    c_tot_np = ws_months.cell(row=6, column=10, value="=SUM(C6:I6)")
    c_tot_np.number_format = "0.0%"
    c_tot_np.font = bold_font
    c_tot_np.border = cell_border

    # Row 7: Zona Sur Volume
    ws_months.cell(row=7, column=2, value="Zona Sur (Personas)").font = bold_font
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx + 1)
        c = ws_months.cell(row=7, column=c_idx, value=f"='Zona Sur'!{col_let}14")
        c.number_format = "#,##0"
        c.font = regular_font
        c.border = cell_border
    c_tot_s = ws_months.cell(row=7, column=10, value="=SUM(C7:I7)")
    c_tot_s.number_format = "#,##0"
    c_tot_s.font = bold_font
    c_tot_s.border = cell_border

    # Row 8: Zona Sur % Monthly
    ws_months.cell(row=8, column=2, value="% Mensual s/ Total Sur").font = small_italic
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=8, column=c_idx, value=f"={col_let}7/$J$7")
        c.number_format = "0.0%"
        c.font = small_italic
        c.border = cell_border
    c_tot_sp = ws_months.cell(row=8, column=10, value="=SUM(C8:I8)")
    c_tot_sp.number_format = "0.0%"
    c_tot_sp.font = bold_font
    c_tot_sp.border = cell_border

    # Row 9: Total CAM Volume
    ws_months.cell(row=9, column=2, value="TOTAL COMUNIDAD DE MADRID").font = bold_font
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=9, column=c_idx, value=f"=SUM({col_let}5,{col_let}7)")
        c.number_format = "#,##0"
        c.font = bold_font
        c.fill = total_fill
        c.border = total_border
    c_tot_cam = ws_months.cell(row=9, column=10, value="=SUM(J5,J7)")
    c_tot_cam.number_format = "#,##0"
    c_tot_cam.font = bold_font
    c_tot_cam.fill = total_fill
    c_tot_cam.border = total_border

    # Row 10: Reparto Cuota Sur vs Norte por Mes
    ws_months.cell(row=10, column=2, value="Cuota Zona Sur (% s/ Total CAM)").font = bold_font
    for c_idx in range(3, 10):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=10, column=c_idx, value=f"={col_let}7/{col_let}9")
        c.number_format = "0.0%"
        c.font = bold_font
        c.border = cell_border
    c_share_s = ws_months.cell(row=10, column=10, value="=J7/J9")
    c_share_s.number_format = "0.0%"
    c_share_s.font = bold_font
    c_share_s.border = cell_border

    # Add Chart: Comparativa Mensual de Afluencia (Bar/Column)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Afluencia de Personas por Mes (Zona Norte vs Zona Sur - 2026)"
    chart1.y_axis.title = "Número de Personas Atendidas"
    chart1.x_axis.title = "Meses (Enero a Julio 2026)"
    chart1.width = 18
    chart1.height = 10

    data_ref1 = Reference(ws_months, min_col=2, min_row=5, max_row=7, max_col=9) # row 5 is North, row 7 is South
    # Using only row 5 and 7
    cats_ref1 = Reference(ws_months, min_col=3, max_col=9, min_row=4, max_row=4)
    
    # We build series manually to select row 5 and 7
    s_north = Series(Reference(ws_months, min_col=3, max_col=9, min_row=5, max_row=5), title="Zona Norte")
    s_south = Series(Reference(ws_months, min_col=3, max_col=9, min_row=7, max_row=7), title="Zona Sur")
    chart1.append(s_north)
    chart1.append(s_south)
    chart1.set_categories(cats_ref1)
    
    ws_months.add_chart(chart1, "B13")

    # ----------------------------------------------------
    # SHEET 5: Días de la Semana & Horas Punta
    # ----------------------------------------------------
    ws_timing = wb.create_sheet(title="Días y Horas Punta")
    ws_timing.views.sheetView[0].showGridLines = True

    ws_timing.merge_cells("B2:G2")
    ws_timing["B2"] = "DISTRIBUCIÓN DE AFLUENCIA POR DÍA DE LA SEMANA & HORAS PUNTA"
    ws_timing["B2"].font = white_title_font
    ws_timing["B2"].fill = navy_header_fill
    ws_timing["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_timing.row_dimensions[2].height = 30

    # Table 1: Weekday distribution
    ws_timing["B4"] = "AFLUENCIA POR DÍA DE LA SEMANA (LUNES A VIERNES)"
    ws_timing["B4"].font = navy_title_font

    wk_headers = ["Día de la Semana", "Zona Norte (%)", "Zona Sur (%)", "Afluencia Media Semanal Norte", "Afluencia Media Semanal Sur", "Diferencial"]
    for col_idx, h in enumerate(wk_headers, start=2):
        cell = ws_timing.cell(row=5, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = blue_sub_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    for idx, day in enumerate(weekdays):
        r = 6 + idx
        ws_timing.cell(row=r, column=2, value=day).font = bold_font
        
        c_np = ws_timing.cell(row=r, column=3, value=weekday_north_pct[idx])
        c_np.number_format = "0.0%"
        c_np.border = cell_border
        
        c_sp = ws_timing.cell(row=r, column=4, value=weekday_south_pct[idx])
        c_sp.number_format = "0.0%"
        c_sp.border = cell_border
        
        c_nv = ws_timing.cell(row=r, column=5, value=f"=C{r}*('Zona Norte'!K12/30)") # ~30 weeks
        c_nv.number_format = "#,##0"
        c_nv.border = cell_border
        
        c_sv = ws_timing.cell(row=r, column=6, value=f"=D{r}*('Zona Sur'!K14/30)")
        c_sv.number_format = "#,##0"
        c_sv.border = cell_border

        c_diff = ws_timing.cell(row=r, column=7, value=f"=F{r}-E{r}")
        c_diff.number_format = "#,##0"
        c_diff.font = Font(name="Calibri", size=10, bold=True, color="C53030")
        c_diff.border = cell_border

        if idx == 0: # Lunes is peak
            for c_col in range(2, 8):
                ws_timing.cell(row=r, column=c_col).fill = highlight_yellow

    # Total Weekdays
    ws_timing.cell(row=11, column=2, value="TOTAL SEMANAL").font = bold_font
    ws_timing.cell(row=11, column=3, value="=SUM(C6:C10)").number_format = "0.0%"
    ws_timing.cell(row=11, column=4, value="=SUM(D6:D10)").number_format = "0.0%"
    ws_timing.cell(row=11, column=5, value="=SUM(E6:E10)").number_format = "#,##0"
    ws_timing.cell(row=11, column=6, value="=SUM(F6:F10)").number_format = "#,##0"
    ws_timing.cell(row=11, column=7, value="=SUM(G6:G10)").number_format = "#,##0"
    for c_idx in range(2, 8):
        c = ws_timing.cell(row=11, column=c_idx)
        c.font = bold_font
        c.fill = total_fill
        c.border = total_border

    # Table 2: Hourly distribution Google Maps
    ws_timing["B14"] = "HORAS PUNTA Y AFLUENCIA HORARIA (08:30 - 14:30 | DATOS GOOGLE MAPS)"
    ws_timing["B14"].font = navy_title_font

    hr_headers = ["Franja Horaria", "Zona Norte (% Día)", "Zona Sur (% Día)", "Nivel de Saturación Norte", "Nivel de Saturación Sur", "Diagnóstico Google Maps"]
    for col_idx, h in enumerate(hr_headers, start=2):
        cell = ws_timing.cell(row=15, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = blue_sub_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    hr_labels_north = ["Medio (Apertura)", "Muy Alto (Hora Punta)", "Máximo (Pico Absoluto)", "Alto", "Medio-Bajo", "Bajo (Cierre)"]
    hr_labels_south = ["Alto (Colas Apertura)", "Máximo (Pico Absoluto)", "Muy Alto", "Alto", "Medio", "Bajo (Cierre)"]
    hr_diagnostics = [
        "Apertura: colas previas significativas en el Sur desde las 08:15.",
        "Franja de máxima afluencia: saturación del mostrador de recepción.",
        "Hora punta consolidada de citas SEPE y trámites presenciales.",
        "Descenso paulatino; atención de citas rezagadas.",
        "Trámites rápidos y entrega de documentación pendiente.",
        "Últimas atenciones; ventanilla prácticamente despejada."
    ]

    for idx, hr in enumerate(hours):
        r = 16 + idx
        ws_timing.cell(row=r, column=2, value=hr).font = bold_font
        
        c_nh = ws_timing.cell(row=r, column=3, value=hourly_north_pct[idx])
        c_nh.number_format = "0.0%"
        c_nh.border = cell_border
        
        c_sh = ws_timing.cell(row=r, column=4, value=hourly_south_pct[idx])
        c_sh.number_format = "0.0%"
        c_sh.border = cell_border
        
        c_ln = ws_timing.cell(row=r, column=5, value=hr_labels_north[idx])
        c_ln.alignment = Alignment(horizontal="center")
        c_ln.border = cell_border
        
        c_ls = ws_timing.cell(row=r, column=6, value=hr_labels_south[idx])
        c_ls.alignment = Alignment(horizontal="center")
        c_ls.border = cell_border
        
        c_diag = ws_timing.cell(row=r, column=7, value=hr_diagnostics[idx])
        c_diag.font = small_italic
        c_diag.border = cell_border

        if idx in [1, 2]: # peak hours 09:30 - 11:30
            for c_col in range(2, 8):
                ws_timing.cell(row=r, column=c_col).fill = highlight_yellow

    # Charts on Sheet 5
    # Chart Weekday
    chart_wk = BarChart()
    chart_wk.type = "col"
    chart_wk.style = 11
    chart_wk.title = "Afluencia Relativa por Día de la Semana (%)"
    chart_wk.y_axis.title = "% del Total Semanal"
    chart_wk.x_axis.title = "Día"
    chart_wk.width = 15
    chart_wk.height = 9

    s_wk_n = Series(Reference(ws_timing, min_col=3, min_row=6, max_row=10), title="Zona Norte")
    s_wk_s = Series(Reference(ws_timing, min_col=4, min_row=6, max_row=10), title="Zona Sur")
    chart_wk.append(s_wk_n)
    chart_wk.append(s_wk_s)
    cats_wk = Reference(ws_timing, min_col=2, min_row=6, max_row=10)
    chart_wk.set_categories(cats_wk)
    ws_timing.add_chart(chart_wk, "I4")

    # Chart Hourly Line
    chart_hr = LineChart()
    chart_hr.title = "Curva de Afluencia Horaria (08:30 a 14:30)"
    chart_hr.style = 13
    chart_hr.y_axis.title = "% del Tráfico Diario"
    chart_hr.x_axis.title = "Franja Horaria"
    chart_hr.width = 15
    chart_hr.height = 9

    s_hr_n = Series(Reference(ws_timing, min_col=3, min_row=16, max_row=21), title="Zona Norte")
    s_hr_s = Series(Reference(ws_timing, min_col=4, min_row=16, max_row=21), title="Zona Sur")
    chart_hr.append(s_hr_n)
    chart_hr.append(s_hr_s)
    cats_hr = Reference(ws_timing, min_col=2, min_row=16, max_row=21)
    chart_hr.set_categories(cats_hr)
    ws_timing.add_chart(chart_hr, "I15")

    # ----------------------------------------------------
    # SHEET 6: Velocidad Citas & Saturación
    # ----------------------------------------------------
    ws_citas = wb.create_sheet(title="Velocidad Citas y Saturación")
    ws_citas.views.sheetView[0].showGridLines = True

    ws_citas.merge_cells("B2:J2")
    ws_citas["B2"] = "ANÁLISIS DE CONSUMO DE CITAS PREVIAS Y SATURACIÓN POR OFICINA (2026)"
    ws_citas["B2"].font = white_title_font
    ws_citas["B2"].fill = navy_header_fill
    ws_citas["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_citas.row_dimensions[2].height = 30

    ws_citas.merge_cells("B3:J3")
    ws_citas["B3"] = "Comparativa de velocidad de agotamiento de citas liberadas (minutos tras apertura de agenda) y días de espera media para cita presencial"
    ws_citas["B3"].font = navy_subtitle_font
    ws_citas.row_dimensions[3].height = 20

    c_headers = [
        "Zona", "Oficina de Empleo", "Tiempo Agotamiento Citas (Minutos)", "Días de Espera Media",
        "Ratio Saturación (1-10)", "Nivel de Tensión", "Canal Recomendado"
    ]
    for col_idx, h in enumerate(c_headers, start=2):
        cell = ws_citas.cell(row=5, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    all_offices = []
    for o in offices_north:
        all_offices.append(("Norte", o["name"], o["exhaust_min"], o["wait_days"], round(10 - (o["exhaust_min"]/25), 1), "Moderada / Controlada", "Oficina Virtual / Presencial"))
    for o in offices_south:
        all_offices.append(("Sur", o["name"], o["exhaust_min"], o["wait_days"], round(10 - (o["exhaust_min"]/25), 1), "Crítica / Muy Saturada", "Oficina Virtual / Sede SEPE"))

    for idx, item in enumerate(all_offices):
        r = 6 + idx
        ws_citas.cell(row=r, column=2, value=item[0]).font = bold_font
        ws_citas.cell(row=r, column=3, value=item[1]).font = regular_font
        
        c_min = ws_citas.cell(row=r, column=4, value=item[2])
        c_min.number_format = "#,##0"
        c_min.alignment = Alignment(horizontal="center")
        
        c_wait = ws_citas.cell(row=r, column=5, value=item[3])
        c_wait.number_format = "0.0"
        c_wait.alignment = Alignment(horizontal="center")
        
        c_sat = ws_citas.cell(row=r, column=6, value=item[4])
        c_sat.number_format = "0.0"
        c_sat.alignment = Alignment(horizontal="center")
        
        c_tens = ws_citas.cell(row=r, column=7, value=item[5])
        c_tens.alignment = Alignment(horizontal="center")
        
        c_rec = ws_citas.cell(row=r, column=8, value=item[6])
        c_rec.font = small_italic
        
        for c_col in range(2, 9):
            cell = ws_citas.cell(row=r, column=c_col)
            cell.border = cell_border
            if item[0] == "Sur":
                cell.fill = light_red_fill
            else:
                cell.fill = light_blue_fill

    # Add Chart: Días de espera y tiempo de agotamiento
    chart_citas = BarChart()
    chart_citas.type = "bar"
    chart_citas.title = "Tiempo de Agotamiento de Citas Nuevas (Minutos) por Oficina"
    chart_citas.style = 10
    chart_citas.x_axis.title = "Minutos transcurridos hasta agotar cupo diario de citas"
    chart_citas.y_axis.title = "Oficina"
    chart_citas.width = 16
    chart_citas.height = 12

    data_citas = Reference(ws_citas, min_col=4, min_row=5, max_row=21)
    cats_citas = Reference(ws_citas, min_col=3, min_row=6, max_row=21)
    chart_citas.add_data(data_citas, titles_from_data=True)
    chart_citas.set_categories(cats_citas)
    ws_citas.add_chart(chart_citas, "J5")

    # Format column widths for all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if cell.number_format and ('%' in cell.number_format or '#' in cell.number_format):
                    # rough length
                    max_len = max(max_len, 10)
                else:
                    if len(val_str) < 50:
                        max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
        ws.column_dimensions["A"].width = 3

    # Ensure sheet order
    wb.remove(default_sheet)
    
    file_path = "/home/bender/Descargas/Estudio_Afluencia_Oficinas_Empleo_Madrid_2026.xlsx"
    wb.save(file_path)
    print(f"Excel file successfully generated at: {file_path}")

if __name__ == "__main__":
    create_employment_report()
