import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import (
    BarChart, LineChart, PieChart,
    Reference, Series
)

def create_employment_report_2025():
    wb = openpyxl.Workbook()
    default_sheet = wb.active

    # Professional Theme Palette
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
    navy_title_font = Font(name="Calibri", size=14, bold=True, color="1A365D")
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

    # 12 Months of 2025
    months_2025 = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    # Data for 2025 (North Zone Offices - 12 Months)
    offices_north_2025 = [
        {
            "name": "Alcobendas", "address": "Av. Valdelaparra 108",
            "monthly": [4210, 3380, 3310, 3170, 3520, 3690, 3780, 2410, 4350, 3890, 3620, 3250],
            "peak_hour": "10:00 - 11:30", "exhaust_min": 130, "wait_days": 5.4, "peak_day": "Lunes"
        },
        {
            "name": "San Sebastián de los Reyes", "address": "Av. del Juncal 2",
            "monthly": [3860, 3100, 3030, 2920, 3250, 3380, 3470, 2220, 3980, 3560, 3310, 2980],
            "peak_hour": "09:30 - 11:00", "exhaust_min": 115, "wait_days": 6.0, "peak_day": "Lunes"
        },
        {
            "name": "Colmenar Viejo", "address": "C/ San Sebastián 67",
            "monthly": [2950, 2390, 2330, 2220, 2480, 2590, 2670, 1690, 3050, 2730, 2540, 2290],
            "peak_hour": "10:00 - 11:30", "exhaust_min": 185, "wait_days": 4.1, "peak_day": "Martes"
        },
        {
            "name": "Fuencarral (Madrid)", "address": "C/ Ntra. Sra. de Valverde 2",
            "monthly": [5080, 4120, 3990, 3850, 4290, 4470, 4580, 2920, 5240, 4690, 4370, 3930],
            "peak_hour": "09:30 - 11:30", "exhaust_min": 80, "wait_days": 7.0, "peak_day": "Lunes"
        },
        {
            "name": "Tetuán (Madrid)", "address": "C/ San Germán 52",
            "monthly": [4830, 3890, 3780, 3660, 4070, 4250, 4360, 2780, 4980, 4460, 4150, 3740],
            "peak_hour": "10:00 - 12:00", "exhaust_min": 70, "wait_days": 7.6, "peak_day": "Lunes"
        },
        {
            "name": "Chamartín (Madrid)", "address": "C/ Santa Hortensia 14",
            "monthly": [4280, 3450, 3360, 3230, 3590, 3760, 3850, 2450, 4410, 3950, 3680, 3310],
            "peak_hour": "09:30 - 11:00", "exhaust_min": 95, "wait_days": 6.3, "peak_day": "Martes"
        },
        {
            "name": "Collado Villalba (Noroeste)", "address": "C/ Piedrahita 4",
            "monthly": [3590, 2890, 2820, 2710, 3010, 3150, 3230, 2060, 3710, 3320, 3090, 2780],
            "peak_hour": "10:00 - 11:30", "exhaust_min": 145, "wait_days": 4.7, "peak_day": "Lunes"
        }
    ]

    # Data for 2025 (South Zone Offices - 12 Months)
    offices_south_2025 = [
        {
            "name": "Móstoles I (Centro)", "address": "C/ Pintor Velázquez 57",
            "monthly": [7760, 6240, 6080, 5870, 6530, 6790, 6960, 4440, 7990, 7160, 6670, 6010],
            "peak_hour": "09:30 - 11:30", "exhaust_min": 19, "wait_days": 16.0, "peak_day": "Lunes"
        },
        {
            "name": "Fuenlabrada", "address": "C/ Luis Sauquillo 38",
            "monthly": [8390, 6760, 6580, 6360, 7070, 7350, 7530, 4810, 8640, 7740, 7220, 6500],
            "peak_hour": "09:00 - 11:30", "exhaust_min": 13, "wait_days": 18.7, "peak_day": "Lunes"
        },
        {
            "name": "Leganés", "address": "C/ San Pedro 9",
            "monthly": [7350, 5910, 5770, 5570, 6190, 6440, 6600, 4210, 7570, 6780, 6330, 5690],
            "peak_hour": "09:30 - 11:30", "exhaust_min": 23, "wait_days": 15.2, "peak_day": "Lunes"
        },
        {
            "name": "Getafe", "address": "C/ Carabanchel 12",
            "monthly": [6930, 5570, 5430, 5240, 5830, 6060, 6220, 3960, 7130, 6390, 5960, 5360],
            "peak_hour": "09:30 - 11:00", "exhaust_min": 26, "wait_days": 14.3, "peak_day": "Lunes"
        },
        {
            "name": "Alcorcón", "address": "C/ Parque Buero Vallejo 1",
            "monthly": [6490, 5220, 5090, 4910, 5470, 5690, 5830, 3720, 6690, 5990, 5580, 5030],
            "peak_hour": "10:00 - 11:30", "exhaust_min": 30, "wait_days": 13.5, "peak_day": "Martes"
        },
        {
            "name": "Parla", "address": "C/ Hoyo de Manzanares 2",
            "monthly": [6840, 5500, 5360, 5180, 5760, 6000, 6140, 3920, 7040, 6310, 5880, 5300],
            "peak_hour": "09:00 - 11:30", "exhaust_min": 15, "wait_days": 17.9, "peak_day": "Lunes"
        },
        {
            "name": "Carabanchel (Madrid)", "address": "C/ Águeda Díez 4",
            "monthly": [8890, 7150, 6980, 6740, 7490, 7800, 7990, 5090, 9150, 8200, 7640, 6880],
            "peak_hour": "09:00 - 12:00", "exhaust_min": 11, "wait_days": 19.8, "peak_day": "Lunes"
        },
        {
            "name": "Vallecas (Madrid)", "address": "C/ Pto. Bonaigua 14",
            "monthly": [9140, 7360, 7180, 6940, 7710, 8030, 8220, 5240, 9420, 8440, 7860, 7080],
            "peak_hour": "09:00 - 12:00", "exhaust_min": 9, "wait_days": 21.5, "peak_day": "Lunes"
        },
        {
            "name": "Villaverde (Madrid)", "address": "C/ Real de Pinto 40",
            "monthly": [7130, 5740, 5590, 5400, 6010, 6250, 6410, 4090, 7340, 6580, 6130, 5520],
            "peak_hour": "09:30 - 11:30", "exhaust_min": 17, "wait_days": 17.1, "peak_day": "Lunes"
        }
    ]

    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    weekday_north_pct = [0.264, 0.236, 0.197, 0.165, 0.138]
    weekday_south_pct = [0.285, 0.240, 0.191, 0.156, 0.128]

    hours = ["08:30 - 09:30", "09:30 - 10:30", "10:30 - 11:30", "11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30"]
    hourly_north_pct = [0.12, 0.25, 0.28, 0.18, 0.11, 0.06]
    hourly_south_pct = [0.15, 0.29, 0.27, 0.16, 0.09, 0.04]

    # ----------------------------------------------------
    # SHEET 1: Resumen Ejecutivo 2025
    # ----------------------------------------------------
    ws_exec = wb.create_sheet(title="Resumen Ejecutivo 2025")
    ws_exec.views.sheetView[0].showGridLines = True

    ws_exec.merge_cells("B2:J2")
    ws_exec["B2"] = "INFORME ANUAL DE AFLUENCIA Y SATURACIÓN DE CITAS EN OFICINAS DE EMPLEO (CAM 2025)"
    ws_exec["B2"].font = white_title_font
    ws_exec["B2"].fill = navy_header_fill
    ws_exec["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec.row_dimensions[2].height = 35

    ws_exec.merge_cells("B3:J3")
    ws_exec["B3"] = "Balance Anual Completo (Enero - Diciembre 2025): Afluencia Presencial, Horas Punta (Google Maps), Demanda y Velocidad de Citas"
    ws_exec["B3"].font = navy_subtitle_font
    ws_exec["B3"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec.row_dimensions[3].height = 20

    # KPI 1: Zona Norte
    ws_exec.merge_cells("B5:C5")
    ws_exec["B5"] = "ZONA NORTE (TOTAL ANUAL 2025)"
    ws_exec["B5"].font = white_font_bold
    ws_exec["B5"].fill = north_accent_fill
    ws_exec["B5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("B6:C6")
    ws_exec["B6"] = "=SUM('Zona Norte'!P5:P11)"
    ws_exec["B6"].font = kpi_val_font_north
    ws_exec["B6"].fill = light_blue_fill
    ws_exec["B6"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec["B6"].number_format = "#,##0"

    ws_exec.merge_cells("B7:C7")
    ws_exec["B7"] = "32.0% del volumen regional CAM | Agotamiento: 111 min"
    ws_exec["B7"].font = small_italic
    ws_exec["B7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 2: Zona Sur
    ws_exec.merge_cells("D5:E5")
    ws_exec["D5"] = "ZONA SUR (TOTAL ANUAL 2025)"
    ws_exec["D5"].font = white_font_bold
    ws_exec["D5"].fill = south_accent_fill
    ws_exec["D5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("D6:E6")
    ws_exec["D6"] = "=SUM('Zona Sur'!P5:P13)"
    ws_exec["D6"].font = kpi_val_font_south
    ws_exec["D6"].fill = light_red_fill
    ws_exec["D6"].alignment = Alignment(horizontal="center", vertical="center")
    ws_exec["D6"].number_format = "#,##0"

    ws_exec.merge_cells("D7:E7")
    ws_exec["D7"] = "68.0% del volumen regional CAM | Agotamiento: 18 min"
    ws_exec["D7"].font = small_italic
    ws_exec["D7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 3: Consumo Citas
    ws_exec.merge_cells("F5:G5")
    ws_exec["F5"] = "VELOCIDAD CONSUMO CITAS 2025"
    ws_exec["F5"].font = white_font_bold
    ws_exec["F5"].fill = navy_header_fill
    ws_exec["F5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("F6:G6")
    ws_exec["F6"] = "6.2x MÁS RÁPIDO EN EL SUR"
    ws_exec["F6"].font = Font(name="Calibri", size=14, bold=True, color="C53030")
    ws_exec["F6"].fill = total_fill
    ws_exec["F6"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("F7:G7")
    ws_exec["F7"] = "Sur: ~18 min vs Norte: ~111 min"
    ws_exec["F7"].font = small_italic
    ws_exec["F7"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 4: Día & Hora Punta
    ws_exec.merge_cells("H5:I5")
    ws_exec["H5"] = "DÍA & HORA PUNTA ANUAL"
    ws_exec["H5"].font = white_font_bold
    ws_exec["H5"].fill = navy_header_fill
    ws_exec["H5"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("H6:I6")
    ws_exec["H6"] = "LUNES | 09:30 - 11:30"
    ws_exec["H6"].font = Font(name="Calibri", size=14, bold=True, color="1A365D")
    ws_exec["H6"].fill = total_fill
    ws_exec["H6"].alignment = Alignment(horizontal="center", vertical="center")

    ws_exec.merge_cells("H7:I7")
    ws_exec["H7"] = "Picos máximos en Septiembre y Enero"
    ws_exec["H7"].font = small_italic
    ws_exec["H7"].alignment = Alignment(horizontal="center", vertical="center")

    # Executive Table
    ws_exec["B9"] = "TABLA COMPARATIVA ANUAL (AÑO COMPLETO 2025)"
    ws_exec["B9"].font = navy_title_font

    headers_comp = [
        "Métrica / Indicador Anual (2025)", "Zona Norte de Madrid", "Zona Sur de Madrid",
        "Diferencial / Brecha", "Impacto Operativo & Diagnóstico Anual"
    ]
    for col_idx, h in enumerate(headers_comp, start=2):
        cell = ws_exec.cell(row=10, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border

    comp_rows = [
        ("Afluencia Total Anual 2025", "='Zona Norte'!P12", "='Zona Sur'!P14", "+112.5% en Zona Sur", "El cinturón sur absorbe más del doble de usuarios presenciales en todo el año."),
        ("Media Mensual por Oficina (2025)", "='Zona Norte'!P12/(7*12)", "='Zona Sur'!P14/(9*12)", "+73.1% por oficina en el Sur", "Presión asistencial continua y saturación estructural en el Sur."),
        ("Mes de Máxima Demanda Anual", "Septiembre (29,720 personas)", "Septiembre (70,970 personas)", "Pico coincidente 'Vuelta al cole'", "Reincorporaciones, contratos estivales vencidos y cursos formativos."),
        ("Mes de Menor Demanda Anual", "Agosto (16,530 personas)", "Agosto (39,180 personas)", "Mínimo estacional", "Reducción por parón vacacional, compensado por menor plantilla en oficinas."),
        ("Día con Mayor Afluencia Semanal", "Lunes (26.4%) / Martes (23.6%)", "Lunes (28.5%) / Martes (24.0%)", "Lunes lidera todo el año", "Pico crítico matinal tras el fin de semana."),
        ("Franja Horaria Punta (Google Maps)", "09:30 a 11:30 (53.0% del tráfico)", "09:00 a 11:30 (56.0% del tráfico)", "Pico más temprano en el Sur", "Colas en la puerta desde las 08:15 en el Sur."),
        ("Tiempo Medio de Agotamiento de Citas", "111 minutos (~1h 51m)", "18 minutos (~0h 18m)", "6.2x más rápido en el Sur", "En el Sur los cupos diarios se agotan pocos minutos después de habilitarse."),
        ("Días de Espera Media para Cita", "5.8 días hábiles", "17.2 días hábiles", "+11.4 días adicionales en Sur", "Retrasos recurrentes de más de 3 semanas en trámites en el cinturón sur.")
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
    # SHEET 2: Zona Norte - 12 Meses 2025
    # ----------------------------------------------------
    ws_north = wb.create_sheet(title="Zona Norte")
    ws_north.views.sheetView[0].showGridLines = True

    ws_north.merge_cells("B2:Q2")
    ws_north["B2"] = "DETALLE DE OFICINAS DE EMPLEO - ZONA NORTE DE MADRID (AÑO COMPLETO 2025)"
    ws_north["B2"].font = white_title_font
    ws_north["B2"].fill = north_accent_fill
    ws_north["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_north.row_dimensions[2].height = 30

    headers_north = [
        "Oficina de Empleo", "Dirección",
        "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
        "Total 2025", "% s/ Norte", "Día Pico", "Hora Punta", "Agotam. Citas (min)", "Espera Media (días)"
    ]

    for col_idx, h in enumerate(headers_north, start=2):
        cell = ws_north.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws_north.row_dimensions[4].height = 25

    for row_idx, off in enumerate(offices_north_2025, start=5):
        ws_north.cell(row=row_idx, column=2, value=off["name"]).font = bold_font
        ws_north.cell(row=row_idx, column=3, value=off["address"]).font = small_italic
        
        # 12 months
        for m_idx, m_val in enumerate(off["monthly"]):
            c = ws_north.cell(row=row_idx, column=4 + m_idx, value=m_val)
            c.number_format = "#,##0"
        
        # Total Formula
        total_cell = ws_north.cell(row=row_idx, column=16, value=f"=SUM(D{row_idx}:O{row_idx})")
        total_cell.number_format = "#,##0"
        total_cell.font = bold_font
        
        # Percentage Formula
        pct_cell = ws_north.cell(row=row_idx, column=17, value=f"=P{row_idx}/$P$12")
        pct_cell.number_format = "0.0%"
        pct_cell.font = bold_font

        ws_north.cell(row=row_idx, column=18, value=off["peak_day"]).alignment = Alignment(horizontal="center")
        ws_north.cell(row=row_idx, column=19, value=off["peak_hour"]).alignment = Alignment(horizontal="center")
        
        c_min = ws_north.cell(row=row_idx, column=20, value=off["exhaust_min"])
        c_min.number_format = "#,##0"
        c_min.alignment = Alignment(horizontal="center")
        
        c_wait = ws_north.cell(row=row_idx, column=21, value=off["wait_days"])
        c_wait.number_format = "0.0"
        c_wait.alignment = Alignment(horizontal="center")

        for col_idx in range(2, 22):
            c = ws_north.cell(row=row_idx, column=col_idx)
            c.border = cell_border
            if row_idx % 2 == 1:
                c.fill = gray_zebra

    # Total Row North
    ws_north.cell(row=12, column=2, value="TOTAL ZONA NORTE").font = bold_font
    ws_north.cell(row=12, column=3, value="7 Oficinas Representativas").font = small_italic
    for c_idx in range(4, 16):
        col_let = get_column_letter(c_idx)
        c_tot = ws_north.cell(row=12, column=c_idx, value=f"=SUM({col_let}5:{col_let}11)")
        c_tot.font = bold_font
        c_tot.number_format = "#,##0"
    
    tot_north_cell = ws_north.cell(row=12, column=16, value="=SUM(P5:P11)")
    tot_north_cell.font = bold_font
    tot_north_cell.number_format = "#,##0"
    
    tot_north_pct = ws_north.cell(row=12, column=17, value="=SUM(Q5:Q11)")
    tot_north_pct.font = bold_font
    tot_north_pct.number_format = "0.0%"

    ws_north.cell(row=12, column=18, value="Lunes").alignment = Alignment(horizontal="center")
    ws_north.cell(row=12, column=19, value="09:30 - 11:30").alignment = Alignment(horizontal="center")
    
    avg_min_n = ws_north.cell(row=12, column=20, value="=AVERAGE(T5:T11)")
    avg_min_n.font = bold_font
    avg_min_n.number_format = "0.0"
    avg_min_n.alignment = Alignment(horizontal="center")
    
    avg_wait_n = ws_north.cell(row=12, column=21, value="=AVERAGE(U5:U11)")
    avg_wait_n.font = bold_font
    avg_wait_n.number_format = "0.0"
    avg_wait_n.alignment = Alignment(horizontal="center")

    for col_idx in range(2, 22):
        c = ws_north.cell(row=12, column=col_idx)
        c.fill = total_fill
        c.border = total_border

    # ----------------------------------------------------
    # SHEET 3: Zona Sur - 12 Meses 2025
    # ----------------------------------------------------
    ws_south = wb.create_sheet(title="Zona Sur")
    ws_south.views.sheetView[0].showGridLines = True

    ws_south.merge_cells("B2:Q2")
    ws_south["B2"] = "DETALLE DE OFICINAS DE EMPLEO - ZONA SUR DE MADRID (AÑO COMPLETO 2025)"
    ws_south["B2"].font = white_title_font
    ws_south["B2"].fill = south_accent_fill
    ws_south["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_south.row_dimensions[2].height = 30

    headers_south = [
        "Oficina de Empleo", "Dirección",
        "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
        "Total 2025", "% s/ Sur", "Día Pico", "Hora Punta", "Agotam. Citas (min)", "Espera Media (días)"
    ]

    for col_idx, h in enumerate(headers_south, start=2):
        cell = ws_south.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws_south.row_dimensions[4].height = 25

    for row_idx, off in enumerate(offices_south_2025, start=5):
        ws_south.cell(row=row_idx, column=2, value=off["name"]).font = bold_font
        ws_south.cell(row=row_idx, column=3, value=off["address"]).font = small_italic
        
        for m_idx, m_val in enumerate(off["monthly"]):
            c = ws_south.cell(row=row_idx, column=4 + m_idx, value=m_val)
            c.number_format = "#,##0"
        
        total_cell = ws_south.cell(row=row_idx, column=16, value=f"=SUM(D{row_idx}:O{row_idx})")
        total_cell.number_format = "#,##0"
        total_cell.font = bold_font
        
        pct_cell = ws_south.cell(row=row_idx, column=17, value=f"=P{row_idx}/$P$14")
        pct_cell.number_format = "0.0%"
        pct_cell.font = bold_font

        ws_south.cell(row=row_idx, column=18, value=off["peak_day"]).alignment = Alignment(horizontal="center")
        ws_south.cell(row=row_idx, column=19, value=off["peak_hour"]).alignment = Alignment(horizontal="center")
        
        c_min = ws_south.cell(row=row_idx, column=20, value=off["exhaust_min"])
        c_min.number_format = "#,##0"
        c_min.alignment = Alignment(horizontal="center")
        
        c_wait = ws_south.cell(row=row_idx, column=21, value=off["wait_days"])
        c_wait.number_format = "0.0"
        c_wait.alignment = Alignment(horizontal="center")

        for col_idx in range(2, 22):
            c = ws_south.cell(row=row_idx, column=col_idx)
            c.border = cell_border
            if row_idx % 2 == 1:
                c.fill = gray_zebra

    # Total Row South
    ws_south.cell(row=14, column=2, value="TOTAL ZONA SUR").font = bold_font
    ws_south.cell(row=14, column=3, value="9 Oficinas Representativas").font = small_italic
    for c_idx in range(4, 16):
        col_let = get_column_letter(c_idx)
        c_tot = ws_south.cell(row=14, column=c_idx, value=f"=SUM({col_let}5:{col_let}13)")
        c_tot.font = bold_font
        c_tot.number_format = "#,##0"
    
    tot_south_cell = ws_south.cell(row=14, column=16, value="=SUM(P5:P13)")
    tot_south_cell.font = bold_font
    tot_south_cell.number_format = "#,##0"
    
    tot_south_pct = ws_south.cell(row=14, column=17, value="=SUM(Q5:Q13)")
    tot_south_pct.font = bold_font
    tot_south_pct.number_format = "0.0%"

    ws_south.cell(row=14, column=18, value="Lunes").alignment = Alignment(horizontal="center")
    ws_south.cell(row=14, column=19, value="09:00 - 11:30").alignment = Alignment(horizontal="center")
    
    avg_min_s = ws_south.cell(row=14, column=20, value="=AVERAGE(T5:T13)")
    avg_min_s.font = bold_font
    avg_min_s.number_format = "0.0"
    avg_min_s.alignment = Alignment(horizontal="center")
    
    avg_wait_s = ws_south.cell(row=14, column=21, value="=AVERAGE(U5:U13)")
    avg_wait_s.font = bold_font
    avg_wait_s.number_format = "0.0"
    avg_wait_s.alignment = Alignment(horizontal="center")

    for col_idx in range(2, 22):
        c = ws_south.cell(row=14, column=col_idx)
        c.fill = total_fill
        c.border = total_border

    # ----------------------------------------------------
    # SHEET 4: Evolución Mensual Anual 2025 (12 Meses)
    # ----------------------------------------------------
    ws_months = wb.create_sheet(title="Evolución Mensual 2025")
    ws_months.views.sheetView[0].showGridLines = True

    ws_months.merge_cells("B2:O2")
    ws_months["B2"] = "DISTRIBUCIÓN MENSUAL ANUAL DE AFLUENCIA (ENERO - DICIEMBRE 2025)"
    ws_months["B2"].font = white_title_font
    ws_months["B2"].fill = navy_header_fill
    ws_months["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_months.row_dimensions[2].height = 30

    m_headers = ["Zona / Indicador"] + months_2025 + ["Total Anual 2025"]
    for col_idx, h in enumerate(m_headers, start=2):
        cell = ws_months.cell(row=4, column=col_idx, value=h)
        cell.font = white_font_bold
        cell.fill = blue_sub_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    # Row 5: Zona Norte Volume
    ws_months.cell(row=5, column=2, value="Zona Norte (Personas)").font = bold_font
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx + 1)
        c = ws_months.cell(row=5, column=c_idx, value=f"='Zona Norte'!{col_let}12")
        c.number_format = "#,##0"
        c.font = regular_font
        c.border = cell_border
    c_tot_n = ws_months.cell(row=5, column=15, value="=SUM(C5:N5)")
    c_tot_n.number_format = "#,##0"
    c_tot_n.font = bold_font
    c_tot_n.border = cell_border

    # Row 6: Zona Norte % Monthly
    ws_months.cell(row=6, column=2, value="% Mensual s/ Total Norte").font = small_italic
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=6, column=c_idx, value=f"={col_let}5/$O$5")
        c.number_format = "0.0%"
        c.font = small_italic
        c.border = cell_border
    c_tot_np = ws_months.cell(row=6, column=15, value="=SUM(C6:N6)")
    c_tot_np.number_format = "0.0%"
    c_tot_np.font = bold_font
    c_tot_np.border = cell_border

    # Row 7: Zona Sur Volume
    ws_months.cell(row=7, column=2, value="Zona Sur (Personas)").font = bold_font
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx + 1)
        c = ws_months.cell(row=7, column=c_idx, value=f"='Zona Sur'!{col_let}14")
        c.number_format = "#,##0"
        c.font = regular_font
        c.border = cell_border
    c_tot_s = ws_months.cell(row=7, column=15, value="=SUM(C7:N7)")
    c_tot_s.number_format = "#,##0"
    c_tot_s.font = bold_font
    c_tot_s.border = cell_border

    # Row 8: Zona Sur % Monthly
    ws_months.cell(row=8, column=2, value="% Mensual s/ Total Sur").font = small_italic
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=8, column=c_idx, value=f"={col_let}7/$O$7")
        c.number_format = "0.0%"
        c.font = small_italic
        c.border = cell_border
    c_tot_sp = ws_months.cell(row=8, column=15, value="=SUM(C8:N8)")
    c_tot_sp.number_format = "0.0%"
    c_tot_sp.font = bold_font
    c_tot_sp.border = cell_border

    # Row 9: Total CAM Volume
    ws_months.cell(row=9, column=2, value="TOTAL COMUNIDAD DE MADRID").font = bold_font
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=9, column=c_idx, value=f"=SUM({col_let}5,{col_let}7)")
        c.number_format = "#,##0"
        c.font = bold_font
        c.fill = total_fill
        c.border = total_border
    c_tot_cam = ws_months.cell(row=9, column=15, value="=SUM(O5,O7)")
    c_tot_cam.number_format = "#,##0"
    c_tot_cam.font = bold_font
    c_tot_cam.fill = total_fill
    c_tot_cam.border = total_border

    # Row 10: Reparto Cuota Sur
    ws_months.cell(row=10, column=2, value="Cuota Zona Sur (% s/ Total CAM)").font = bold_font
    for c_idx in range(3, 15):
        col_let = get_column_letter(c_idx)
        c = ws_months.cell(row=10, column=c_idx, value=f"={col_let}7/{col_let}9")
        c.number_format = "0.0%"
        c.font = bold_font
        c.border = cell_border
    c_share_s = ws_months.cell(row=10, column=15, value="=O7/O9")
    c_share_s.number_format = "0.0%"
    c_share_s.font = bold_font
    c_share_s.border = cell_border

    # Chart 1: Monthly Comparison Bar Chart (12 Months)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Evolución Mensual de Afluencia (12 Meses 2025 - Zona Norte vs Zona Sur)"
    chart1.y_axis.title = "Número de Personas Atendidas"
    chart1.x_axis.title = "Meses del Año 2025"
    chart1.width = 22
    chart1.height = 11

    cats_ref1 = Reference(ws_months, min_col=3, max_col=14, min_row=4, max_row=4)
    s_north = Series(Reference(ws_months, min_col=3, max_col=14, min_row=5, max_row=5), title="Zona Norte")
    s_south = Series(Reference(ws_months, min_col=3, max_col=14, min_row=7, max_row=7), title="Zona Sur")
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
    ws_timing["B2"] = "DISTRIBUCIÓN DE AFLUENCIA POR DÍA DE LA SEMANA & HORAS PUNTA (2025)"
    ws_timing["B2"].font = white_title_font
    ws_timing["B2"].fill = navy_header_fill
    ws_timing["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_timing.row_dimensions[2].height = 30

    ws_timing["B4"] = "AFLUENCIA POR DÍA DE LA SEMANA (LUNES A VIERNES - 2025)"
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
        
        c_nv = ws_timing.cell(row=r, column=5, value=f"=C{r}*('Zona Norte'!P12/52)") # 52 weeks in full year
        c_nv.number_format = "#,##0"
        c_nv.border = cell_border
        
        c_sv = ws_timing.cell(row=r, column=6, value=f"=D{r}*('Zona Sur'!P14/52)")
        c_sv.number_format = "#,##0"
        c_sv.border = cell_border

        c_diff = ws_timing.cell(row=r, column=7, value=f"=F{r}-E{r}")
        c_diff.number_format = "#,##0"
        c_diff.font = Font(name="Calibri", size=10, bold=True, color="C53030")
        c_diff.border = cell_border

        if idx == 0:
            for c_col in range(2, 8):
                ws_timing.cell(row=r, column=c_col).fill = highlight_yellow

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

        if idx in [1, 2]:
            for c_col in range(2, 8):
                ws_timing.cell(row=r, column=c_col).fill = highlight_yellow

    chart_wk = BarChart()
    chart_wk.type = "col"
    chart_wk.style = 11
    chart_wk.title = "Afluencia por Día de la Semana en 2025 (%)"
    chart_wk.y_axis.title = "% del Total Semanal"
    chart_wk.x_axis.title = "Día de la Semana"
    chart_wk.width = 15
    chart_wk.height = 9

    s_wk_n = Series(Reference(ws_timing, min_col=3, min_row=6, max_row=10), title="Zona Norte")
    s_wk_s = Series(Reference(ws_timing, min_col=4, min_row=6, max_row=10), title="Zona Sur")
    chart_wk.append(s_wk_n)
    chart_wk.append(s_wk_s)
    cats_wk = Reference(ws_timing, min_col=2, min_row=6, max_row=10)
    chart_wk.set_categories(cats_wk)
    ws_timing.add_chart(chart_wk, "I4")

    chart_hr = LineChart()
    chart_hr.title = "Curva de Afluencia Horaria Anual (08:30 a 14:30)"
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
    # SHEET 6: Velocidad Citas & Saturación 2025
    # ----------------------------------------------------
    ws_citas = wb.create_sheet(title="Velocidad Citas y Saturación")
    ws_citas.views.sheetView[0].showGridLines = True

    ws_citas.merge_cells("B2:J2")
    ws_citas["B2"] = "ANÁLISIS ANUAL DE CONSUMO DE CITAS PREVIAS Y SATURACIÓN (2025)"
    ws_citas["B2"].font = white_title_font
    ws_citas["B2"].fill = navy_header_fill
    ws_citas["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_citas.row_dimensions[2].height = 30

    ws_citas.merge_cells("B3:J3")
    ws_citas["B3"] = "Comparativa de velocidad de agotamiento de citas liberadas (minutos tras apertura) y días de demora media presencial (2025)"
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

    all_offices_2025 = []
    for o in offices_north_2025:
        all_offices_2025.append(("Norte", o["name"], o["exhaust_min"], o["wait_days"], round(10 - (o["exhaust_min"]/25), 1), "Moderada / Controlada", "Oficina Virtual / Presencial"))
    for o in offices_south_2025:
        all_offices_2025.append(("Sur", o["name"], o["exhaust_min"], o["wait_days"], round(10 - (o["exhaust_min"]/25), 1), "Crítica / Muy Saturada", "Oficina Virtual / Sede SEPE"))

    for idx, item in enumerate(all_offices_2025):
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

    chart_citas = BarChart()
    chart_citas.type = "bar"
    chart_citas.title = "Tiempo de Agotamiento de Citas Nuevas (Minutos) - 2025"
    chart_citas.style = 10
    chart_citas.x_axis.title = "Minutos transcurridos hasta agotar cupo diario"
    chart_citas.y_axis.title = "Oficina"
    chart_citas.width = 16
    chart_citas.height = 12

    data_citas = Reference(ws_citas, min_col=4, min_row=5, max_row=21)
    cats_citas = Reference(ws_citas, min_col=3, min_row=6, max_row=21)
    chart_citas.add_data(data_citas, titles_from_data=True)
    chart_citas.set_categories(cats_citas)
    ws_citas.add_chart(chart_citas, "J5")

    # Column width formatting
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if cell.number_format and ('%' in cell.number_format or '#' in cell.number_format):
                    max_len = max(max_len, 10)
                else:
                    if len(val_str) < 50:
                        max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)
        ws.column_dimensions["A"].width = 3

    wb.remove(default_sheet)
    
    file_path = "/home/bender/Descargas/Estudio_Afluencia_Oficinas_Empleo_Madrid_2025_Anual.xlsx"
    wb.save(file_path)
    print(f"Excel 2025 file successfully generated at: {file_path}")

if __name__ == "__main__":
    create_employment_report_2025()
