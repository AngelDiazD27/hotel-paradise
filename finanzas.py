import sys
import os
import json
import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment


def estado_resultados():
    print("\n--- INGRESO DE DATOS: ESTADO DE RESULTADOS ---")
  
    print("\n[ SECCIÓN: INGRESOS Y COSTOS ]")
    ventas = float(input("Ventas Totales: "))
    costo_ventas = float(input("Costo de Ventas: "))
    utilidad_bruta = ventas - costo_ventas
    print(f"Utilidad Bruta: $ {utilidad_bruta:,.2f}")


    print("\n[ SECCIÓN: GASTOS DE OPERACIÓN ]")
    
    gasto_ventas = float(input("Gastos de Ventas: "))
    gasto_admin = float(input("Gastos de Administración: "))
    gasto_depreciacion = float(input("Gastos de Depreciación: "))
    
    total_gastos_op = gasto_ventas + gasto_admin + gasto_depreciacion
    utilidad_operacion = utilidad_bruta - total_gastos_op
    print(f"Total Gastos Operación: $ {total_gastos_op:,.2f}")
    print(f"Utilidad de Operación: $ {utilidad_operacion:,.2f}")

  
    print("\n[ SECCIÓN: RIF ]")
    gasto_financiero = float(input("Gasto Financiero: "))
    producto_financiero = float(input("Producto Financiero: "))
    # El RIF es la diferencia. Si el gasto es mayor, resta a la utilidad.
    resultado_integral = gasto_financiero - producto_financiero
    print(f"Resultado Integral (RIF): $ {resultado_integral:,.2f}")


    print("\n[ SECCIÓN: OTROS GASTOS Y PRODUCTOS ]")
    otros_gastos = float(input("Otros Gastos: "))
    otros_productos = float(input("Otros Productos: "))
    partidas_discontinuas = otros_gastos - otros_productos
    
    utilidad_antes_impuestos = utilidad_operacion - (resultado_integral + partidas_discontinuas)
    print(f"Utilidad Antes de Impuestos: $ {utilidad_antes_impuestos:,.2f}")

 
    print("\n[ SECCIÓN: IMPUESTOS ]")
    
    porcentaje_isr = float(input("Ingrese porcentaje de ISR: ")) / 100
    porcentaje_ptu = float(input("Ingrese porcentaje de PTU : ")) / 100
    
    monto_isr = utilidad_antes_impuestos * porcentaje_isr
    monto_ptu = utilidad_antes_impuestos * porcentaje_ptu
    
    utilidad_neta = utilidad_antes_impuestos - monto_isr - monto_ptu

    print("\n-------------------------------------------")
    print(f"(-) ISR ({porcentaje_isr*100}%):      $ {monto_isr:,.2f}")
    print(f"(-) PTU ({porcentaje_ptu*100}%):      $ {monto_ptu:,.2f}")
    print(f"(=) UTILIDAD NETA:       $ {utilidad_neta:,.2f}")
    print("-------------------------------------------")

    datos_ER = {
        "Ventas": ventas,
        "Costo de Ventas": costo_ventas,
        "Utilidad Bruta": utilidad_bruta,
        "Gasto de Ventas": gasto_ventas,
        "Gasto Administrativo": gasto_admin,
        "Gasto de Depreciación": gasto_depreciacion,
        "Utilidad de Operación": utilidad_operacion,
        "Gasto Financiero": gasto_financiero,
        "Productos Financieros": producto_financiero,
        "Resultado Integral": resultado_integral,
        "Otros Gastos": otros_gastos,
        "Otros Productos": otros_productos,
        "Partidas Descontinuas": partidas_discontinuas,
        "Utilidad Antes de Impuestos": utilidad_antes_impuestos,
        "ISR Pagado": monto_isr,
        "PTU Pagado": monto_ptu,
        "Utilidad Neta": utilidad_neta
    }
    return datos_ER

def ER_tabla(datos_ER):
    print("-" * 50)
    print(("-"*15) + "ESTADO DE RESULTADOS" + ("-"*15))
    print("-" * 50)
    print("{:<30} {:>18,.2f}".format("Ventas", datos_ER["Ventas"]))
    print("{:<30} {:>18,.2f}".format("Costo de Ventas", datos_ER["Costo de Ventas"]))
    
    print("-" * 50)
    print("{:>35} {:>12,.2f}".format("Utilidad Bruta", datos_ER["Utilidad Bruta"]))
    print("-" * 50)

    print("{:<30} {:>18,.2f}".format("Gasto de Ventas", datos_ER["Gasto de Ventas"]))
    print("{:<30} {:>18,.2f}".format("Gasto Administrativo", datos_ER["Gasto Administrativo"]))
    print("{:<30} {:>18,.2f}".format("Gasto de Depreciación", datos_ER["Gasto de Depreciación"]))

    print("-" * 50)
    print("{:>35} {:>12,.2f}".format("Utilidad de Operación", datos_ER["Utilidad de Operación"]))
    print("-" * 50)   

    print("\nResultado Integral de financiamiento:")
    print("-" * 50)
    print("{:<30} {:>18,.2f}".format("Gasto Financiero", datos_ER["Gasto Financiero"]))
    print("{:<30} {:>18,.2f}".format("Producto Financiero", datos_ER["Productos Financieros"])) 
    print("-" * 50)
    
    print("\nPartidas Discontinuas:")
    print("-" * 50)
    print("{:<30} {:>18,.2f}".format("Otros Gastos", datos_ER["Otros Gastos"]))
    print("{:<30} {:>18,.2f}".format("Otros Productos", datos_ER["Otros Productos"]))
    print("{:>35} {:>12,.2f}".format("Utilidad antes de impuestos", datos_ER["Utilidad Antes de Impuestos"]))

    print("-" * 50)
    print("{:<30} {:>18,.2f}".format("ISR Pagado", datos_ER["ISR Pagado"]))
    print("{:<30} {:>18,.2f}".format("PTU Pagado", datos_ER["PTU Pagado"]))
    print("{:>35} {:>12,.2f}".format("Utilidad neta", datos_ER["Utilidad Neta"]))
    print("-" * 50)

def exportar_excel_estado_resultados(datos_ER):
    try:
        archivo = "EstadoResultados.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Estado de Resultados"

        titulo_font = Font(bold=True, size=14)
        subtitulo_font = Font(bold=True, size=12)
        bold_font = Font(bold=True)

        borde = Border(
            bottom=Side(style="thin", color="000000")
        )

        centro = Alignment(horizontal="center")
        derecha = Alignment(horizontal="right")


        ws.column_dimensions["A"].width = 5
        ws.column_dimensions["B"].width = 35
        ws.column_dimensions["C"].width = 18
        ws.column_dimensions["D"].width = 18

        ws.merge_cells("B2:D2")
        ws["B2"] = "Estado de Resultados"
        ws["B2"].font = subtitulo_font
        ws["B2"].alignment = centro

        fila = 4

        ws[f"B{fila}"] = "Ventas"
        ws[f"D{fila}"] = datos_ER["Ventas"]

        fila += 2

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Costo de ventas"
        ws[f"D{fila}"] = datos_ER["Costo de Ventas"]

        fila += 1

        ws[f"C{fila}"] = "Utilidad Bruta"
        ws[f"D{fila}"] = datos_ER["Utilidad Bruta"]

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3

        ws[f"B{fila}"] = "Gastos de operación"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Gastos de ventas"
        ws[f"D{fila}"] = datos_ER["Gasto de Ventas"]

        fila += 1

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Gastos de Administración"
        ws[f"D{fila}"] = datos_ER["Gasto Administrativo"]

        fila += 1

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Gastos de depreciación"
        ws[f"D{fila}"] = datos_ER["Gasto de Depreciación"]

        fila += 1

        total_gastos = (
            datos_ER["Gasto de Ventas"] +
            datos_ER["Gasto Administrativo"] +
            datos_ER["Gasto de Depreciación"]
        )

        ws[f"C{fila}"] = "Utilidad de Operación"
        ws[f"D{fila}"] = datos_ER["Utilidad de Operación"]

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3

        ws[f"B{fila}"] = "Resultado Integral de Financiamiento"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Gastos financieros"
        ws[f"D{fila}"] = datos_ER["Gasto Financiero"]

        fila += 1

        ws[f"B{fila}"] = "Producto financiero"
        ws[f"D{fila}"] = datos_ER["Productos Financieros"]

        fila += 3

        ws[f"B{fila}"] = "Partidas Discontinuas"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        ws[f"B{fila}"] = "Otros gastos"
        ws[f"D{fila}"] = datos_ER["Otros Gastos"]

        fila += 1

        ws[f"A{fila}"] = "(-)"
        ws[f"B{fila}"] = "Otros productos"
        ws[f"D{fila}"] = datos_ER["Otros Productos"]

        fila += 2

        ws[f"C{fila}"] = "Utilidad antes de impuestos"
        ws[f"D{fila}"] = datos_ER["Utilidad Antes de Impuestos"]

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 2

        ws[f"B{fila}"] = "ISR"
        ws[f"C{fila}"] = "30%"
        ws[f"D{fila}"] = datos_ER["ISR Pagado"]

        fila += 1

        ws[f"B{fila}"] = "PTU"
        ws[f"C{fila}"] = "10%"
        ws[f"D{fila}"] = datos_ER["PTU Pagado"]

        fila += 2

        ws[f"C{fila}"] = "Utilidad neta"
        ws[f"D{fila}"] = datos_ER["Utilidad Neta"]

        ws[f"C{fila}"].font = Font(bold=True, size=12)
        ws[f"D{fila}"].font = Font(bold=True, size=12)


        for row in ws.iter_rows(min_row=1, max_row=fila, min_col=4, max_col=4):
            for cell in row:
                cell.number_format = '$ #,##0.00'
                cell.alignment = derecha

        for row in range(1, fila + 1):
            ws[f"D{row}"].border = borde

        wb.save(archivo)

        print(f"\nEstado de Resultados exportado correctamente a {archivo}")

    except Exception:
        print(f"\nError al guardar Excel: {sys.exc_info()[0:2]}\n")


def balance_general():
    print("\n--- INGRESO DE DATOS: BALANCE GENERAL ---")
    
    datos_BG = {}

    datos_BG["Bancos"] = float(input("Bancos: "))
    datos_BG["Clientes"] = float(input("Clientes: "))
    datos_BG["Inventarios"] = float(input("Inventarios: "))
    datos_BG["Papelería y útiles"] = float(input("Papelería y útiles: "))

    total_circulante = sum([datos_BG["Bancos"], datos_BG["Clientes"], datos_BG["Inventarios"], datos_BG["Papelería y útiles"]])
    print(f"Total Activo Circulante: $ {total_circulante:,.2f}")

    datos_BG["Terrenos y edificios"] = float(input("Terreno y edificios: "))
    datos_BG["Maquinaria y equipo"] = float(input("Maquinaria y equipo: "))
    datos_BG["Depreciación acumulada (maquinaria)"] = float(input("Dep. Acumulada Maquinaria: "))
    datos_BG["Mobiliario y equipo de oficina"] = float(input("Mobiliario y accesorios: "))
    datos_BG["Equipo de transporte"] = float(input("Equipo de transporte: "))
    datos_BG["Equipo de cómputo"] = float(input("Equipo de cómputo: "))
    datos_BG["Depreciación acumulada (activo fijo)"] = float(input("Dep. Acumulada Activos Fijos: "))
    datos_BG["Inversiones permanentes"] = float(input("Inversiones permanentes: "))

    total_fijo = ((datos_BG["Terrenos y edificios"] + datos_BG["Maquinaria y equipo"] + 
                   datos_BG["Mobiliario y equipo de oficina"] + datos_BG["Equipo de cómputo"] + 
                   datos_BG["Equipo de transporte"] + datos_BG["Inversiones permanentes"]) - 
                  (datos_BG["Depreciación acumulada (maquinaria)"] + 
                   datos_BG["Depreciación acumulada (activo fijo)"]))
    print(f"Subtotal Activo No Circulante: $ {total_fijo:,.2f}")

    datos_BG["Otros activos (Gastos inst.)"] = float(input("Gastos de instalación: "))
    
    total_activos = sum([total_circulante, total_fijo, datos_BG["Otros activos (Gastos inst.)"]])
    print(f"Total Activo: $ {total_activos:,.2f}")

    datos_BG["Proveedores"] = float(input("Proveedores: "))
    datos_BG["Acreedores"] = float(input("Acreedores diversos: "))
    datos_BG["Impuestos por pagar"] = float(input("Impuestos por pagar: "))
    datos_BG["Anticipo por pagar"] = float(input("Anticipo de clientes: "))
    datos_BG["Gastos por pagar"] = float(input("Gastos por pagar: "))
    datos_BG["Hipotecas"] = float(input("Hipotecas por pagar cp: "))
    datos_BG["Préstamos bancarios"] = float(input("Préstamos bancarios cp: "))

    total_pasivo_cp = sum([datos_BG["Proveedores"], datos_BG["Acreedores"], datos_BG["Impuestos por pagar"],
                            datos_BG["Anticipo por pagar"], datos_BG["Gastos por pagar"], datos_BG["Hipotecas"], datos_BG["Préstamos bancarios"]])
    print(f"Subtotal Pasivo Corto Plazo: $ {total_pasivo_cp:,.2f}  ")

    
    datos_BG["Hipotecas lp"] = float(input("Hipotecas por pagar lp: "))
    datos_BG["Préstamos bancarios lp"] = float(input("Préstamos bancarios lp: "))
    
    total_pasivo_lp = datos_BG["Hipotecas lp"] + datos_BG["Préstamos bancarios lp"]
    total_pasivos = total_pasivo_cp + total_pasivo_lp
    print(f"Subtotal Pasivo Largo Plazo: $ {total_pasivo_lp:,.2f}")
    print(f"TOTAL PASIVOS: $ {total_pasivos:,.2f}")

    datos_BG["Capital social"] = float(input("Capital Social: "))
    datos_BG["Utilidades retenidas"] = float(input("Utilidades ejercicios anteriores: "))
    datos_BG["Reserva legal"] = float(input("Reserva legal: "))
    datos_BG["Utilidad del ejercicio"] = float(input("Utilidad del ejercicio: "))
    
    total_capital = (datos_BG["Capital social"] + datos_BG["Utilidades retenidas"] + 
                     datos_BG["Reserva legal"] + datos_BG["Utilidad del ejercicio"])
    print(f"Subtotal Capital Contable: $ {total_capital:,.2f}")

    pasivo_mas_capital = total_pasivos + total_capital
    print("\n-------------------------------------------")
    print(f"TOTAL PASIVO + CAPITAL: $ {pasivo_mas_capital:,.2f}")
    print(f"TOTAL ACTIVOS:          $ {total_activos:,.2f}")

    if total_activos == pasivo_mas_capital:
        print("EL BALANCE CUADRA PERFECTAMENTE.")
    else:
        print(f"EL BALANCE NO CUADRA. Diferencia: $ {abs(total_activos - pasivo_mas_capital):,.2f}")
    print("-------------------------------------------")

    return datos_BG

def BG_tabla(datos_BG):
    print("-" * 70)
    print((" " * 20) + "BALANCE GENERAL")
    print("-" * 70)

    print("\nACTIVO CIRCULANTE")
    print("-" * 70)

    activos_circulantes = [
        ("Bancos", datos_BG["Bancos"]),
        ("Clientes", datos_BG["Clientes"]),
        ("Inventarios", datos_BG["Inventarios"]),
        ("Papelería y útiles", datos_BG["Papelería y útiles"])
    ]

    total_activo_circulante = 0

    for nombre, valor in activos_circulantes:
        print("{:<45} ${:>15,.2f}".format(nombre, valor))
        total_activo_circulante += valor

    print("-" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "Total Activo Circulante",
        total_activo_circulante
    ))


    print("\nACTIVO NO CIRCULANTE")
    print("-" * 70)

    activos_fijos = [
        ("Terrenos y edificios", datos_BG["Terrenos y edificios"]),
        ("Maquinaria y equipo", datos_BG["Maquinaria y equipo"]),
        ("(-) Dep. acumulada maquinaria", datos_BG["Depreciación acumulada (maquinaria)"]),
        ("Mobiliario y equipo oficina", datos_BG["Mobiliario y equipo de oficina"]),
        ("Equipo de transporte", datos_BG["Equipo de transporte"]),
        ("Equipo de cómputo", datos_BG["Equipo de cómputo"]),
        ("(-) Dep. acumulada activos fijos", datos_BG["Depreciación acumulada (activo fijo)"]),
        ("Inversiones permanentes", datos_BG["Inversiones permanentes"])
    ]

    total_activo_fijo = (
        datos_BG["Terrenos y edificios"] +
        datos_BG["Maquinaria y equipo"] +
        datos_BG["Mobiliario y equipo de oficina"] +
        datos_BG["Equipo de transporte"] +
        datos_BG["Equipo de cómputo"] +
        datos_BG["Inversiones permanentes"]
        -
        datos_BG["Depreciación acumulada (maquinaria)"]
        -
        datos_BG["Depreciación acumulada (activo fijo)"]
    )

    for nombre, valor in activos_fijos:
        print("{:<45} ${:>15,.2f}".format(nombre, valor))

    print("-" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "Total Activo No Circulante",
        total_activo_fijo
    ))


    print("\nOTROS ACTIVOS")
    print("-" * 70)

    print("{:<45} ${:>15,.2f}".format(
        "Gastos de instalación",
        datos_BG["Otros activos (Gastos inst.)"]
    ))


    total_activos = (
        total_activo_circulante +
        total_activo_fijo +
        datos_BG["Otros activos (Gastos inst.)"]
    )

    print("=" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "TOTAL ACTIVOS",
        total_activos
    ))
    print("=" * 70)


    print("\nPASIVO A CORTO PLAZO")
    print("-" * 70)

    pasivo_cp = [
        ("Proveedores", datos_BG["Proveedores"]),
        ("Acreedores diversos", datos_BG["Acreedores"]),
        ("Impuestos por pagar", datos_BG["Impuestos por pagar"]),
        ("Anticipo de clientes", datos_BG["Anticipo por pagar"]),
        ("Gastos por pagar", datos_BG["Gastos por pagar"]),
        ("Hipotecas CP", datos_BG["Hipotecas"]),
        ("Préstamos bancarios CP", datos_BG["Préstamos bancarios"])
    ]

    total_pasivo_cp = 0

    for nombre, valor in pasivo_cp:
        print("{:<45} ${:>15,.2f}".format(nombre, valor))
        total_pasivo_cp += valor

    print("-" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "Total Pasivo Corto Plazo",
        total_pasivo_cp
    ))


    print("\nPASIVO A LARGO PLAZO")
    print("-" * 70)

    pasivo_lp = [
        ("Hipotecas LP", datos_BG["Hipotecas lp"]),
        ("Préstamos bancarios LP", datos_BG["Préstamos bancarios lp"])
    ]

    total_pasivo_lp = 0

    for nombre, valor in pasivo_lp:
        print("{:<45} ${:>15,.2f}".format(nombre, valor))
        total_pasivo_lp += valor

    print("-" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "Total Pasivo Largo Plazo",
        total_pasivo_lp
    ))


    total_pasivos = total_pasivo_cp + total_pasivo_lp

    print("=" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "TOTAL PASIVOS",
        total_pasivos
    ))
    print("=" * 70)


    print("\nCAPITAL CONTABLE")
    print("-" * 70)

    capital = [
        ("Capital social", datos_BG["Capital social"]),
        ("Utilidades retenidas", datos_BG["Utilidades retenidas"]),
        ("Reserva legal", datos_BG["Reserva legal"]),
        ("Utilidad del ejercicio", datos_BG["Utilidad del ejercicio"])
    ]

    total_capital = 0

    for nombre, valor in capital:
        print("{:<45} ${:>15,.2f}".format(nombre, valor))
        total_capital += valor

    print("-" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "Total Capital Contable",
        total_capital
    ))

    total_pasivo_capital = total_pasivos + total_capital

    print("=" * 70)
    print("{:<45} ${:>15,.2f}".format(
        "TOTAL PASIVO + CAPITAL",
        total_pasivo_capital
    ))
    print("=" * 70)

    if total_activos == total_pasivo_capital:
        print("\nEL BALANCE CUADRA PERFECTAMENTE.")
    else:
        diferencia = abs(total_activos - total_pasivo_capital)

        print(f"\nEL BALANCE NO CUADRA.")
        print(f"Diferencia: $ {diferencia:,.2f}")

def exportar_excel_balance_general(datos_BG):
    try:
        archivo = "BalanceGeneral.xlsx"

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Balance General"

        titulo_font = Font(bold=True, size=14)
        subtitulo_font = Font(bold=True, size=12)
        bold_font = Font(bold=True)

        borde = Border(
            bottom=Side(style="thin", color="000000")
        )

        centro = Alignment(horizontal="center")
        derecha = Alignment(horizontal="right")


        ws.column_dimensions["A"].width = 5
        ws.column_dimensions["B"].width = 40
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 20


        ws.merge_cells("B2:D2")
        ws["B2"] = "Balance General"
        ws["B2"].font = subtitulo_font
        ws["B2"].alignment = centro

        fila = 4


        ws[f"B{fila}"] = "ACTIVO CIRCULANTE"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        activos_circulantes = [
            ("Bancos", datos_BG["Bancos"]),
            ("Clientes", datos_BG["Clientes"]),
            ("Inventarios", datos_BG["Inventarios"]),
            ("Papelería y útiles", datos_BG["Papelería y útiles"])
        ]

        total_activo_circulante = 0

        for nombre, valor in activos_circulantes:
            ws[f"B{fila}"] = nombre
            ws[f"D{fila}"] = valor

            total_activo_circulante += valor
            fila += 1

        ws[f"C{fila}"] = "Total Activo Circulante"
        ws[f"D{fila}"] = total_activo_circulante

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3


        ws[f"B{fila}"] = "ACTIVO NO CIRCULANTE"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        activos_no_circulantes = [
            ("Terrenos y edificios", datos_BG["Terrenos y edificios"]),
            ("Maquinaria y equipo", datos_BG["Maquinaria y equipo"]),
            ("(-) Dep. acumulada maquinaria", datos_BG["Depreciación acumulada (maquinaria)"]),
            ("Mobiliario y equipo oficina", datos_BG["Mobiliario y equipo de oficina"]),
            ("Equipo de transporte", datos_BG["Equipo de transporte"]),
            ("Equipo de cómputo", datos_BG["Equipo de cómputo"]),
            ("(-) Dep. acumulada activos fijos", datos_BG["Depreciación acumulada (activo fijo)"]),
            ("Inversiones permanentes", datos_BG["Inversiones permanentes"])
        ]

        total_activo_no_circulante = (
            datos_BG["Terrenos y edificios"] +
            datos_BG["Maquinaria y equipo"] +
            datos_BG["Mobiliario y equipo de oficina"] +
            datos_BG["Equipo de transporte"] +
            datos_BG["Equipo de cómputo"] +
            datos_BG["Inversiones permanentes"]
            -
            datos_BG["Depreciación acumulada (maquinaria)"]
            -
            datos_BG["Depreciación acumulada (activo fijo)"]
        )

        for nombre, valor in activos_no_circulantes:
            ws[f"B{fila}"] = nombre
            ws[f"D{fila}"] = valor
            fila += 1

        ws[f"C{fila}"] = "Total Activo No Circulante"
        ws[f"D{fila}"] = total_activo_no_circulante

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3


        ws[f"B{fila}"] = "OTROS ACTIVOS"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        ws[f"B{fila}"] = "Gastos de instalación"
        ws[f"D{fila}"] = datos_BG["Otros activos (Gastos inst.)"]

        fila += 2


        total_activos = (
            total_activo_circulante +
            total_activo_no_circulante +
            datos_BG["Otros activos (Gastos inst.)"]
        )

        ws[f"C{fila}"] = "TOTAL ACTIVOS"
        ws[f"D{fila}"] = total_activos

        ws[f"C{fila}"].font = Font(bold=True, size=12)
        ws[f"D{fila}"].font = Font(bold=True, size=12)

        fila += 4


        ws[f"B{fila}"] = "PASIVO A CORTO PLAZO"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        pasivo_cp = [
            ("Proveedores", datos_BG["Proveedores"]),
            ("Acreedores diversos", datos_BG["Acreedores"]),
            ("Impuestos por pagar", datos_BG["Impuestos por pagar"]),
            ("Anticipo de clientes", datos_BG["Anticipo por pagar"]),
            ("Gastos por pagar", datos_BG["Gastos por pagar"]),
            ("Hipotecas CP", datos_BG["Hipotecas"]),
            ("Préstamos bancarios CP", datos_BG["Préstamos bancarios"])
        ]

        total_pasivo_cp = 0

        for nombre, valor in pasivo_cp:
            ws[f"B{fila}"] = nombre
            ws[f"D{fila}"] = valor

            total_pasivo_cp += valor
            fila += 1

        ws[f"C{fila}"] = "Total Pasivo Corto Plazo"
        ws[f"D{fila}"] = total_pasivo_cp

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3


        ws[f"B{fila}"] = "PASIVO A LARGO PLAZO"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        pasivo_lp = [
            ("Hipotecas LP", datos_BG["Hipotecas lp"]),
            ("Préstamos bancarios LP", datos_BG["Préstamos bancarios lp"])
        ]

        total_pasivo_lp = 0

        for nombre, valor in pasivo_lp:
            ws[f"B{fila}"] = nombre
            ws[f"D{fila}"] = valor

            total_pasivo_lp += valor
            fila += 1

        ws[f"C{fila}"] = "Total Pasivo Largo Plazo"
        ws[f"D{fila}"] = total_pasivo_lp

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3


        total_pasivos = total_pasivo_cp + total_pasivo_lp

        ws[f"C{fila}"] = "TOTAL PASIVOS"
        ws[f"D{fila}"] = total_pasivos

        ws[f"C{fila}"].font = Font(bold=True, size=12)
        ws[f"D{fila}"].font = Font(bold=True, size=12)

        fila += 4


        ws[f"B{fila}"] = "CAPITAL CONTABLE"
        ws[f"B{fila}"].font = bold_font

        fila += 1

        capital = [
            ("Capital social", datos_BG["Capital social"]),
            ("Utilidades retenidas", datos_BG["Utilidades retenidas"]),
            ("Reserva legal", datos_BG["Reserva legal"]),
            ("Utilidad del ejercicio", datos_BG["Utilidad del ejercicio"])
        ]

        total_capital = 0

        for nombre, valor in capital:
            ws[f"B{fila}"] = nombre
            ws[f"D{fila}"] = valor

            total_capital += valor
            fila += 1

        ws[f"C{fila}"] = "Total Capital Contable"
        ws[f"D{fila}"] = total_capital

        ws[f"C{fila}"].font = bold_font
        ws[f"D{fila}"].font = bold_font

        fila += 3


        total_pasivo_capital = total_pasivos + total_capital

        ws[f"C{fila}"] = "TOTAL PASIVO + CAPITAL"
        ws[f"D{fila}"] = total_pasivo_capital

        ws[f"C{fila}"].font = Font(bold=True, size=12)
        ws[f"D{fila}"].font = Font(bold=True, size=12)

        for row in ws.iter_rows(min_row=1, max_row=fila, min_col=4, max_col=4):
            for cell in row:
                cell.number_format = '$ #,##0.00'
                cell.alignment = derecha

        for row in range(1, fila + 1):
            ws[f"D{row}"].border = borde

        wb.save(archivo)

        print(f"\n[SISTEMA] Balance General exportado correctamente a {archivo}")

    except Exception:
        print(f"\nError al guardar Excel: {sys.exc_info()[0:2]}\n")


def calcular_razon_liquidez(datos_BG):
    print("\n--- CÁLCULO DE RAZÓN DE LIQUIDEZ ---")
    resultados_liquidez = {}

    activo_circulante = sum([datos_BG["Bancos"], datos_BG["Clientes"], datos_BG["Inventarios"], datos_BG["Papelería y útiles"]])
    
    pasivo_circulante = sum([datos_BG["Proveedores"], datos_BG["Acreedores"], datos_BG["Impuestos por pagar"],
                              datos_BG["Anticipo por pagar"], datos_BG["Gastos por pagar"], datos_BG["Hipotecas"], datos_BG["Préstamos bancarios"]])
    
    inventarios = datos_BG["Inventarios"]
    print ("Razón Circulante")
    try:
        razon_circulante = activo_circulante / pasivo_circulante
        print(f"Resultado: {razon_circulante:.2f}")
        resultados_liquidez["Razón Circulante"] = round(razon_circulante, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultados_liquidez["Razón Circulante"] = None

    print("\nPrueba Ácida")
    try:
        prueba_acida = (
            activo_circulante - inventarios
        ) / pasivo_circulante
        resultados_liquidez["Prueba Ácida"] = round(prueba_acida, 2)

        print(f"Resultado: {prueba_acida:.2f}")
    except ZeroDivisionError:
        print("No calculable")
        resultados_liquidez["Prueba Ácida"] = None

    print("\nCapital de Trabajo Neto")
    capital_trabajo = (
        activo_circulante - pasivo_circulante
    )
    resultados_liquidez["Capital de Trabajo Neto"] = round(capital_trabajo, 2)
    print(f"Resultado: $ {capital_trabajo:,.2f}")
    resultados_liquidez["Capital de Trabajo Neto"] = round(capital_trabajo, 2)

    print("\nRazon de efectivo:")
    efectivo = datos_BG["Bancos"]
    try:
        razon_efectivo = efectivo / pasivo_circulante
        print(f"Resultado: {razon_efectivo:.2f}")
        resultados_liquidez["Razón de Efectivo"] = round(razon_efectivo, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultados_liquidez["Razón de Efectivo"] = None

    opcion = input("\n¿Desea exportar estos resultados a Excel? (s/n): ")
    if opcion.lower() == "s":
        exportar_excel_razones("Liquidez", resultados_liquidez)        


def calcular_razones_endeudamiento(datos_BG, datos_ER):
    print("\n--- RAZONES DE ENDEUDAMIENTO ---")
    resultados_endeudamiento = {}

    total_activo = (
        datos_BG["Bancos"] +
        datos_BG["Clientes"] +
        datos_BG["Inventarios"] +
        datos_BG["Papelería y útiles"] +

        datos_BG["Terrenos y edificios"] +
        datos_BG["Maquinaria y equipo"] +
        datos_BG["Mobiliario y equipo de oficina"] +
        datos_BG["Equipo de cómputo"] +
        datos_BG["Equipo de transporte"] +
        datos_BG["Inversiones permanentes"]
        -
        datos_BG["Depreciación acumulada (maquinaria)"] -
        datos_BG["Depreciación acumulada (activo fijo)"]
        +
        datos_BG["Otros activos (Gastos inst.)"]
    )

    total_pasivo_cp = (
        datos_BG["Proveedores"] +
        datos_BG["Acreedores"] +
        datos_BG["Impuestos por pagar"] +
        datos_BG["Anticipo por pagar"] +
        datos_BG["Gastos por pagar"] +
        datos_BG["Hipotecas"] +
        datos_BG["Préstamos bancarios"]
    )

    total_pasivo_lp = (
        datos_BG["Hipotecas lp"] +
        datos_BG["Préstamos bancarios lp"]
    )

    total_pasivo = (
        total_pasivo_cp +
        total_pasivo_lp
    )

    total_capital = (
        datos_BG["Capital social"] +
        datos_BG["Utilidades retenidas"] +
        datos_BG["Reserva legal"] +
        datos_BG["Utilidad del ejercicio"]
    )

    utilidad_operacion = datos_ER["Utilidad de Operación"]
    gasto_financiero = datos_ER["Gasto Financiero"]

    print("\nRazón de Endeudamiento")

    try:
        razon_endeudamiento = (
            total_pasivo / total_activo
        )
        print(f"Resultado: {razon_endeudamiento * 100:.2f}%")
        resultados_endeudamiento["Razón de Endeudamiento"] = razon_endeudamiento
    except ZeroDivisionError:
        print("No calculable")
        resultados_endeudamiento["Razón de Endeudamiento"] = None
    print("\nRazón de Capital")

    try:
        razon_capital = (
            total_capital / total_activo
        )
        print(f"Resultado: {razon_capital * 100:.2f}%")
        resultados_endeudamiento["Razón de Capital"] = razon_capital
    except ZeroDivisionError:
        print("No calculable")
        resultados_endeudamiento["Razón de Capital"] = None
    print("\nApalancamiento Financiero")

    try:
        apalancamiento = (
            total_pasivo_lp /
            datos_BG["Capital social"]
        )
        print(f"Resultado: {apalancamiento:.2f} veces")
        resultados_endeudamiento["Apalancamiento Financiero"] = round(apalancamiento, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultados_endeudamiento["Apalancamiento Financiero"] = None
    print("\nCobertura de Intereses")

    try:
        cobertura = (
            utilidad_operacion /
            gasto_financiero
        )
        print(f"Resultado: {cobertura:.2f} veces")
        resultados_endeudamiento["Cobertura de Intereses"] = round(cobertura, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultados_endeudamiento["Cobertura de Intereses"] = None
    opcion = input("¿Desea exportar estos resultados a Excel? (s/n): ")
    if opcion.lower() == "s":
        exportar_excel_razones("Endeudamiento", resultados_endeudamiento)


def calcular_razones_rentabilidad(datos_BG, datos_ER):
    print("\n--- RAZONES DE RENTABILIDAD ---")
    resultado_rentabilidad = {}

    utilidad_neta = datos_ER["Utilidad Neta"]

    ventas = datos_ER["Ventas"]

    utilidad_bruta = datos_ER["Utilidad Bruta"]

    utilidad_operacion = datos_ER["Utilidad de Operación"]

    total_activos = (
        datos_BG["Bancos"] +
        datos_BG["Clientes"] +
        datos_BG["Inventarios"] +
        datos_BG["Papelería y útiles"] +
        datos_BG["Terrenos y edificios"] +
        datos_BG["Maquinaria y equipo"] +
        datos_BG["Mobiliario y equipo de oficina"] +
        datos_BG["Equipo de cómputo"] +
        datos_BG["Equipo de transporte"] +
        datos_BG["Inversiones permanentes"]
        -
        datos_BG["Depreciación acumulada (maquinaria)"] -
        datos_BG["Depreciación acumulada (activo fijo)"]
        +
        datos_BG["Otros activos (Gastos inst.)"]
    )
    capital_contable = (
        datos_BG["Capital social"] +
        datos_BG["Utilidades retenidas"] +
        datos_BG["Reserva legal"] +
        datos_BG["Utilidad del ejercicio"]
    )


    print("\nMargen Neto")
    try:
        margen_neto = (
            utilidad_neta / ventas
        ) * 100
        print(f"Resultado: {margen_neto:.2f}%")
        resultado_rentabilidad["Margen Neto"] = round(margen_neto, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultado_rentabilidad["Margen Neto"] = None

    print("\nMargen Bruto")
    try:
        margen_bruto = (
            utilidad_bruta / ventas
        ) * 100
        print(f"Resultado: {margen_bruto:.2f}%")
        resultado_rentabilidad["Margen Bruto"] = round(margen_bruto, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultado_rentabilidad["Margen Bruto"] = None

    print("\nMargen Operativo")
    try:
        margen_operativo = (
            utilidad_operacion / ventas
        ) * 100
        print(f"Resultado: {margen_operativo:.2f}%")
        resultado_rentabilidad["Margen Operativo"] = round(margen_operativo, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultado_rentabilidad["Margen Operativo"] = None

    print("\nROA (Rendimiento sobre activos)")
    try:
        roa = (
            utilidad_neta / total_activos
        ) * 100
        print(f"Resultado: {roa:.2f}%")
        resultado_rentabilidad["ROA"] = round(roa, 2)
    except ZeroDivisionError:   
        print("No calculable")
        resultado_rentabilidad["ROA"] = None

    print("\nROE (Rendimiento sobre capital)")
    try:
        roe = (
            utilidad_neta / capital_contable
        ) * 100
        print(f"Resultado: {roe:.2f}%")
        resultado_rentabilidad["ROE"] = round(roe, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultado_rentabilidad["ROE"] = None

    print("\nRCC (Rendimiento sobre capital común)")
    try:
        rcc = (
            datos_ER["Utilidad Neta"] / datos_BG["Capital social"]
        ) * 100

        print(f"Resultado: {rcc:.2f}%")
        resultado_rentabilidad["RCC"] = round(rcc, 2)
    except ZeroDivisionError:
        print("No calculable")
        resultado_rentabilidad["RCC"] = None

    opcion = input("¿Desea exportar estos resultados a Excel? (s/n): ")
    if opcion.lower() == "s":
        exportar_excel_razones("Rentabilidad", resultado_rentabilidad)    


def calcular_razones_mercado(datos_BG, datos_ER):
    print("\n--- RAZONES DE MERCADO ---")
    resultados_mercado = {}

    capital_contable = (
        datos_BG["Capital social"] +
        datos_BG["Utilidades retenidas"] +
        datos_BG["Reserva legal"] +
        datos_BG["Utilidad del ejercicio"]
    )

    utilidad_neta = datos_ER["Utilidad Neta"]
    
    print("Ingresa los datos bursátiles/manuales.")
    numero_acciones = float(input("Número de acciones: "))
    valor_mercado = float(input("Valor de mercado por acción: "))


    print("\nValor en Libros")
    try:
        valor_libros = (capital_contable /numero_acciones)
        print(f"Resultado: $ {valor_libros:,.2f}")
        resultados_mercado["Valor en Libros"] = valor_libros
    except ZeroDivisionError:
        print("No calculable")
        resultados_mercado["Valor en Libros"] = None


    print("\nUtilidad por Acción")
    try:
        utilidad_accion = (utilidad_neta /numero_acciones)
        print(f"Resultado: $ {utilidad_accion:,.2f}")
        resultados_mercado["Utilidad por Acción"] = utilidad_accion
    except ZeroDivisionError:
        print("No calculable")
        resultados_mercado["Utilidad por Acción"] = None


    print("\nValor Mercado / Valor Libros")
    try:
        razon_vm_vl = (valor_mercado /valor_libros)
        print(f"Resultado: {razon_vm_vl:.2f}")
        resultados_mercado["Valor Mercado / Valor Libros"] = razon_vm_vl
    except ZeroDivisionError:
        print("No calculable")
        resultados_mercado["Valor Mercado / Valor Libros"] = None


    print("\nRazón Precio / Utilidad")
    try:
        razon_pu = (valor_mercado /utilidad_accion)
        print(f"Resultado: {razon_pu:.2f}")
        resultados_mercado["Razón Precio / Utilidad"] = razon_pu
    except ZeroDivisionError:
        print("No calculable")
        resultados_mercado["Razón Precio / Utilidad"] = None


    print("\nRentabilidad por Acción")
    try:
        rentabilidad_accion = (utilidad_accion / valor_libros) * 100
        print(f"Resultado: {rentabilidad_accion:.2f}%")
        resultados_mercado["Rentabilidad por Acción"] = rentabilidad_accion
    except ZeroDivisionError:
        print("No calculable")
        resultados_mercado["Rentabilidad por Acción"] = None

    opcion = input("¿Desea exportar estos resultados a Excel? (s/n): ")
    if opcion.lower() == "s":
            exportar_excel_razones("Mercado", resultados_mercado)    


def calcular_razones_actividad(datos_BG, datos_ER):
    print("\n--- RAZONES DE ACTIVIDAD ---")
    resultados_act = {}

    ventas = datos_ER["Ventas"]

    costo_ventas = datos_ER["Costo de Ventas"]

    inventarios = datos_BG["Inventarios"]

    clientes = datos_BG["Clientes"]

    proveedores = datos_BG["Proveedores"]

    total_activo_fijo = (
        (
            datos_BG["Terrenos y edificios"] +
            datos_BG["Maquinaria y equipo"] +
            datos_BG["Mobiliario y equipo de oficina"] +
            datos_BG["Equipo de cómputo"] +
            datos_BG["Equipo de transporte"] +
            datos_BG["Inversiones permanentes"]
        )
        -
        (
            datos_BG["Depreciación acumulada (maquinaria)"] +
            datos_BG["Depreciación acumulada (activo fijo)"]
        )
    )

    total_activo = (
        datos_BG["Bancos"] +
        datos_BG["Clientes"] +
        datos_BG["Inventarios"] +
        datos_BG["Papelería y útiles"] +
        total_activo_fijo +
        datos_BG["Otros activos (Gastos inst.)"]
    )

    activo_circulante = (
        datos_BG["Bancos"] +
        datos_BG["Clientes"] +
        datos_BG["Inventarios"] +
        datos_BG["Papelería y útiles"]
    )

    pasivo_corto = (
        datos_BG["Proveedores"] +
        datos_BG["Acreedores"] +
        datos_BG["Impuestos por pagar"] +
        datos_BG["Anticipo por pagar"] +
        datos_BG["Gastos por pagar"] +
        datos_BG["Hipotecas"] +
        datos_BG["Préstamos bancarios"]
    )
    capital_trabajo = (
        activo_circulante -
        pasivo_corto
    )

    
    razones = {
        "Rotación de Inventarios":
        (costo_ventas, inventarios),
        "Rotación de Cuentas por Cobrar":
        (ventas, clientes),
        "Rotación de Cuentas por Pagar":
        (costo_ventas, proveedores),
        "Rotación de Activos Fijos":
        (ventas, total_activo_fijo),
        "Rotación de Activos Totales":
        (ventas, total_activo),
        "Rotación de Capital de Trabajo":
        (ventas, capital_trabajo)
    }

    for nombre, (numerador, denominador) in razones.items():
        print(f"\n{nombre}")

        try:
            resultado = (numerador / denominador)
            print(f"Resultado: {resultado:.2f} veces")
            resultados_act[nombre] = round(resultado, 2)
        except ZeroDivisionError:
            print("No calculable")
            resultados_act[nombre] = None

    opcion = input("¿Desea exportar estos resultados a Excel? (s/n): ")
    if opcion.lower() == "s":
        exportar_excel_razones("Actividad", resultados_act)
   

def exportar_excel_razones(tipo, resultados):
    try:
        archivo = "RazonesFinancieras.xlsx"
        if os.path.exists(archivo):
            wb = openpyxl.load_workbook(archivo)
        else:
            wb = openpyxl.Workbook()
            wb.remove(wb.active) 

        if tipo in wb.sheetnames:
            ws = wb[tipo]
        else:
            ws = wb.create_sheet(title=tipo)

        ws.delete_rows(1, ws.max_row)

        encabezados = ["Razón", "Resultado"]
        for col, nombre in enumerate(encabezados, start=1):
            celda = ws.cell(row=1, column=col, value=nombre)
            celda.font = Font(bold=True)
            celda.border = Border(bottom=Side(style="thick", color="000000"))
            celda.alignment = Alignment(horizontal="center", vertical="center")

        fila = 2
        for razon, valor in resultados.items():
            ws.cell(row=fila, column=1, value=razon).alignment = Alignment(horizontal="left")
            if valor is not None:
                ws.cell(row=fila, column=2, value=valor).alignment = Alignment(horizontal="center")
            else:
                ws.cell(row=fila, column=2, value="No calculable").alignment = Alignment(horizontal="center")
            fila += 1

        
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 20

        wb.save(archivo)
        print(f"Resultados de {tipo} exportados correctamente a {archivo}")

    except Exception:
        print(f"\nError al guardar Excel: {sys.exc_info()[0:2]}\n")


def guardar(tipo, datos):
    archivo_nombre = "datos_contables.json"
    contenido = {}

    if os.path.exists(archivo_nombre):
        try:
            with open(archivo_nombre, "r") as archivo:
                contenido = json.load(archivo)
        except:
            contenido = {}

    contenido[tipo] = datos
    with open(archivo_nombre, "w") as archivo:
        json.dump(contenido, archivo, indent=4)
    print(f"\n[SISTEMA] {tipo.upper()} guardado correctamente.")


def cargar_datos():
    if os.path.exists("datos_contables.json"):
        try:
            with open("datos_contables.json", "r") as archivo:
                return json.load(archivo)
        except:
            return {}
    return {}


def main():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ingresar datos del Balance General")
        print("2. Ingresar datos del Estado de Resultados")
        print("3. Ver datos guardados ")
        print("4. Calcular Razon de Liquidez")
        print("5. Calcular Razon de Endeudamiento")
        print("6. Calcular Razon de Rentabilidad")
        print("7. Calcular Razon de Mercado")
        print("8. Calcular Razon de Actividad")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                datos = balance_general()
                guardar("balance_general", datos)
            except ValueError:
                print("\n Error: Por favor ingrese solo números.")

        elif opcion == "2":
            try:
                datos_er = estado_resultados()
                guardar("estado_resultados", datos_er)
            except ValueError:
                print("\n Error: Por favor ingrese solo números.")

        elif opcion == "3":
            datos_guardados = cargar_datos()

            print("\n--- VER DATOS GUARDADOS ---")
            print("1. Balance General")
            print("2. Estado de Resultados")
            

            subopcion = input("Selecciona una opción: ")
            if subopcion == "1":
                if "balance_general" in datos_guardados:
                    BG_tabla(datos_guardados.get("balance_general", {}))
                    opcion_exportar = input("\n¿Desea exportar el Balance General a Excel? (s/n): ")
                    if opcion_exportar.lower() == "s":
                        exportar_excel_balance_general(datos_guardados["balance_general"])
                else:
                    print("\n No se encontraron datos del Balance General o el archivo está vacío.")
            
            elif subopcion == "2":        
                if "estado_resultados" in datos_guardados:
                    ER_tabla(datos_guardados.get("estado_resultados", {}))
                    opcion_exportar = input("\n¿Desea exportar el Estado de Resultados a Excel? (s/n): ")
                    if opcion_exportar.lower() == "s":
                        exportar_excel_estado_resultados(datos_guardados["estado_resultados"])
                else:
                    print("\n No se encontraron datos del Estado de Resultados o el archivo está vacío.")

            else:
                print("Opción no válida.")
            
        elif opcion == "4":
            datos_guardados = cargar_datos()
            if "balance_general" in datos_guardados:
                calcular_razon_liquidez(datos_guardados["balance_general"])
            else:
                print("\n No se encontraron datos del Balance General para calcular la razón de liquidez.")    

        elif opcion == "5":
            datos_guardados = cargar_datos()
            if (
                "balance_general" in datos_guardados and
                "estado_resultados" in datos_guardados
            ):
                calcular_razones_endeudamiento(
                    datos_guardados["balance_general"],
                    datos_guardados["estado_resultados"]
                )
            else:
                print("Faltan datos del Balance o Estado de Resultados.")

        elif opcion == "6":
            datos_guardados = cargar_datos()
            if (
                "balance_general" in datos_guardados and
                "estado_resultados" in datos_guardados
            ):
                calcular_razones_rentabilidad(
                    datos_guardados["balance_general"],
                    datos_guardados["estado_resultados"]
                )
            else:
                print("Faltan datos para calcular.")

        elif opcion == "7":
            datos_guardados = cargar_datos()
            if (
                "balance_general" in datos_guardados and
                "estado_resultados" in datos_guardados
            ):
                calcular_razones_mercado(
                    datos_guardados["balance_general"],
                    datos_guardados["estado_resultados"]
                )
            else:
                print("Faltan datos para calcular.")        

        elif opcion == "8":
                datos_guardados = cargar_datos()

                if (
                    "balance_general" in datos_guardados and
                    "estado_resultados" in datos_guardados
                ):

                    calcular_razones_actividad(
                        datos_guardados["balance_general"],
                        datos_guardados["estado_resultados"]
                    )
                else:
                    print("Faltan datos para calcular.")

        elif opcion == "9":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
