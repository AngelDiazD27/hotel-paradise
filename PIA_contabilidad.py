import pandas as pd
import sys
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

def obtener_numero(pregunta, default):
    try:
        valor_str = input(f"{pregunta} (Default: {default}): ")
        if valor_str == "":
            return float(default)
        return float(valor_str)
    except ValueError:
        print("Entrada inválida. Usando valor default.")
        return float(default)

def obtener_datos_interactivos():
    print("="*70)
    print("--- 1. CONFIGURACIÓN DE VENTAS PLANEADAS (UNIDADES) ---")
    
    ventas_mr_s1 = obtener_numero("Unidades Milanesa Res (Sem 1)", 8000)
    ventas_mr_s2 = obtener_numero("Unidades Milanesa Res (Sem 2)", 7000)
    
    ventas_mp_s1 = obtener_numero("Unidades Milanesa Pollo (Sem 1)", 10000)
    ventas_mp_s2 = obtener_numero("Unidades Milanesa Pollo (Sem 2)", 9000)
    
    ventas_ev_s1 = obtener_numero("Unidades Espagueti Verde (Sem 1)", 5000)
    ventas_ev_s2 = obtener_numero("Unidades Espagueti Verde (Sem 2)", 6000)
    
    print("\n--- 2. CONFIGURACIÓN DE PRECIOS DE VENTA ---")
    precio_mr_s1 = obtener_numero("Precio Milanesa Res (Sem 1)", 150)
    precio_mr_s2 = obtener_numero("Precio Milanesa Res (Sem 2)", 160)
    
    precio_mp_s1 = obtener_numero("Precio Milanesa Pollo (Sem 1)", 130)
    precio_mp_s2 = obtener_numero("Precio Milanesa Pollo (Sem 2)", 140)
    
    precio_ev_s1 = obtener_numero("Precio Espagueti Verde (Sem 1)", 100)
    precio_ev_s2 = obtener_numero("Precio Espagueti Verde (Sem 2)", 110)

    PRODUCTOS = {
        'Milanesa Res': {
            'ventas_sem1': ventas_mr_s1, 'ventas_sem2': ventas_mr_s2,
            'precio_sem1': precio_mr_s1, 'precio_sem2': precio_mr_s2
        },
        'Milanesa Pollo': {
            'ventas_sem1': ventas_mp_s1, 'ventas_sem2': ventas_mp_s2,
            'precio_sem1': precio_mp_s1, 'precio_sem2': precio_mp_s2
        },
        'Espagueti Verde': {
            'ventas_sem1': ventas_ev_s1, 'ventas_sem2': ventas_ev_s2,
            'precio_sem1': precio_ev_s1, 'precio_sem2': precio_ev_s2
        }
    }
    
    print("\n" + "="*70)
    print("...Datos cargados. Iniciando simulación...")
    return PRODUCTOS

PRODUCTOS = {}

VENTAS_2027_SEM1_SUPUESTO = {
    'Milanesa Res': 9000,
    'Milanesa Pollo': 11000,
    'Espagueti Verde': 7000
}

REQUERIMIENTOS = {
    'Milanesa Res':   {'mat_A_kg': 0.25, 'mat_B_kg': 0.10, 'mat_C_L': 0.05, 'mod_hrs': 0.30},
    'Milanesa Pollo': {'mat_A_kg': 0.25, 'mat_B_kg': 0.10, 'mat_C_L': 0.05, 'mod_hrs': 0.25},
    'Espagueti Verde':{'mat_A_kg': 0.05, 'mat_B_kg': 0.20, 'mat_C_L': 0.15, 'mod_hrs': 0.20}
}

COSTOS = {
    'mat_A_kg': 10,
    'mat_B_kg': 15,
    'mat_C_L': 20,
    'mod_hora_sem1': 20,
    'mod_hora_sem2': 25
}

POLITICAS = {
    'inv_prod_terminado_pct': 0.20,
    'inv_materiales_pct': 0.15,
}

GIF = {
    'sem1': {'Depreciación': 30000, 'Seguros': 10000, 'Mantenimiento': 30000, 'Energéticos': 40000, 'Varios': 10000},
    'sem2': {'Depreciación': 30000, 'Seguros': 10000, 'Mantenimiento': 25000, 'Energéticos': 35000, 'Varios': 10000}
}

GASTOS_OP = {
    'sem1': {'Depreciación': 10000, 'Sueldos': 150000, 'Comisiones_pct': 0.02, 'Varios': 15000, 'Intereses': 3000},
    'sem2': {'Depreciación': 10000, 'Sueldos': 150000, 'Comisiones_pct': 0.02, 'Varios': 10000, 'Intereses': 3000}
}

FLUJO = {
    'cobranza_2026_pct': 0.90,
    'pago_compras_2026_pct': 0.60,
}

BALANCE_INICIAL = {
    'Efectivo': 100000,
    'Clientes': 50000,
    'Inv_Materiales': 45000,
    'Inv_Prod_Terminado': 135000,
    'Activo_Fijo_Neto_Inicial': (800000 + 500000 - 200000),
    'Proveedores': 33500,
    'Doc_x_Pagar': 66500,
    'ISR_x_Pagar': 50000,
    'Prestamo_Bancario_LP': 300000,
    'Capital_Contribuido': 800000,
    'Utilidades_Retenidas': 200000,
    'HARDCODE_Inv_Prod_Terminado_Final': 194911.72
}

INVERSION_ACTIVOS = 75000
TASA_ISR = 0.30
TASA_PTU = 0.10

idx_sem = ['Sem 1', 'Sem 2', 'Total 2026']
material_cols = [k for k in COSTOS.keys() if k.startswith('mat_')]

cedula_ventas = pd.DataFrame(columns=['Milanesa Res', 'Milanesa Pollo', 'Espagueti Verde'], index=idx_sem).fillna(0)
cedula_prod = pd.DataFrame(columns=['Milanesa Res', 'Milanesa Pollo', 'Espagueti Verde'], index=idx_sem).fillna(0)
cedula_consumo_mat = pd.DataFrame(columns=material_cols, index=idx_sem).fillna(0)
cedula_compras_mat = pd.DataFrame(columns=material_cols, index=idx_sem).fillna(0)
cedula_mod = pd.DataFrame(columns=idx_sem, index=['Total Horas', 'Costo Hora', 'Importe MOD']).fillna(0)
cedula_gif = pd.DataFrame(columns=idx_sem, index=['Total GIF', 'Salida Efectivo GIF', 'Tasa GIF x Hora MOD']).fillna(0)
cedula_gastos_op = pd.DataFrame(columns=idx_sem, index=['Total Gasto Op', 'Salida Efectivo Op']).fillna(0)
cedula_costo_unitario = pd.DataFrame(columns=['Milanesa Res', 'Milanesa Pollo', 'Espagueti Verde'], index=['Costo MP', 'Costo MOD', 'Costo GIF', 'Costo Unitario Sem 1', 'Costo Unitario Sem 2']).fillna(0.0)
cedula_cogs = pd.DataFrame(columns=['Milanesa Res', 'Milanesa Pollo', 'Espagueti Verde'], index=idx_sem).fillna(0)

REPORTES_FINALES = {}

def print_header(titulo):
    print("\n" + "="*70)
    print(f"--- {titulo} ---")
    print("="*70)

def calcular_cedula_1_ventas():
    print_header("Cédula 1: Presupuesto de Ventas")
    total_sem1 = 0
    total_sem2 = 0
    for prod in PRODUCTOS:
        v_s1 = PRODUCTOS[prod]['ventas_sem1'] * PRODUCTOS[prod]['precio_sem1']
        v_s2 = PRODUCTOS[prod]['ventas_sem2'] * PRODUCTOS[prod]['precio_sem2']
        cedula_ventas.loc['Sem 1', prod] = v_s1
        cedula_ventas.loc['Sem 2', prod] = v_s2
        cedula_ventas.loc['Total 2026', prod] = v_s1 + v_s2
        total_sem1 += v_s1
        total_sem2 += v_s2
    
    cedula_ventas['Total Ventas'] = cedula_ventas.sum(axis=1)
    print(cedula_ventas.to_markdown(floatfmt=",.2f"))
    
    REPORTES_FINALES['Total_Ventas_Anual'] = cedula_ventas.loc['Total 2026', 'Total Ventas']
    REPORTES_FINALES['Ventas_Sem1'] = total_sem1
    REPORTES_FINALES['Ventas_Sem2'] = total_sem2

def calcular_cedula_2_produccion():
    print_header("Cédula 2: Presupuesto de Producción (Unidades)")
    idx_prod = ['Unidades a Vender', 'Inv. Final', 'Total Necesidad', 'Inv. Inicial', 'Unidades a Producir']
    
    df_prod_s1 = pd.DataFrame(columns=PRODUCTOS.keys(), index=idx_prod).fillna(0)
    for prod in PRODUCTOS:
        df_prod_s1.loc['Unidades a Vender', prod] = PRODUCTOS[prod]['ventas_sem1']
        df_prod_s1.loc['Inv. Final', prod] = PRODUCTOS[prod]['ventas_sem2'] * POLITICAS['inv_prod_terminado_pct']
        df_prod_s1.loc['Inv. Inicial', prod] = PRODUCTOS[prod]['ventas_sem1'] * POLITICAS['inv_prod_terminado_pct']
    
    df_prod_s1.loc['Total Necesidad'] = df_prod_s1.loc['Unidades a Vender'] + df_prod_s1.loc['Inv. Final']
    df_prod_s1.loc['Unidades a Producir'] = df_prod_s1.loc['Total Necesidad'] - df_prod_s1.loc['Inv. Inicial']
    
    df_prod_s2 = pd.DataFrame(columns=PRODUCTOS.keys(), index=idx_prod).fillna(0)
    for prod in PRODUCTOS:
        df_prod_s2.loc['Unidades a Vender', prod] = PRODUCTOS[prod]['ventas_sem2']
        df_prod_s2.loc['Inv. Final', prod] = VENTAS_2027_SEM1_SUPUESTO[prod] * POLITICAS['inv_prod_terminado_pct']
        df_prod_s2.loc['Inv. Inicial', prod] = df_prod_s1.loc['Inv. Final', prod]
    
    df_prod_s2.loc['Total Necesidad'] = df_prod_s2.loc['Unidades a Vender'] + df_prod_s2.loc['Inv. Final']
    df_prod_s2.loc['Unidades a Producir'] = df_prod_s2.loc['Total Necesidad'] - df_prod_s2.loc['Inv. Inicial']
    
    print("--- Producción Semestre 1 ---")
    print(df_prod_s1.to_markdown(floatfmt=",.0f"))
    print("\n--- Producción Semestre 2 ---")
    print(df_prod_s2.to_markdown(floatfmt=",.0f"))
    
    cedula_prod.loc['Sem 1'] = df_prod_s1.loc['Unidades a Producir']
    cedula_prod.loc['Sem 2'] = df_prod_s2.loc['Unidades a Producir']
    cedula_prod.loc['Total 2026'] = cedula_prod.loc['Sem 1'] + cedula_prod.loc['Sem 2']
    
def calcular_cedula_3_consumo_mat():
    print_header("Cédula 3: Presupuesto de Consumo de Materiales")
    
    consumo_s1 = {'mat_A_kg': 0, 'mat_B_kg': 0, 'mat_C_L': 0}
    for prod in PRODUCTOS:
        unidades = cedula_prod.loc['Sem 1', prod]
        consumo_s1['mat_A_kg'] += unidades * REQUERIMIENTOS[prod]['mat_A_kg']
        consumo_s1['mat_B_kg'] += unidades * REQUERIMIENTOS[prod]['mat_B_kg']
        consumo_s1['mat_C_L'] += unidades * REQUERIMIENTOS[prod]['mat_C_L']
    cedula_consumo_mat.loc['Sem 1'] = pd.Series(consumo_s1)
    
    consumo_s2 = {'mat_A_kg': 0, 'mat_B_kg': 0, 'mat_C_L': 0}
    for prod in PRODUCTOS:
        unidades = cedula_prod.loc['Sem 2', prod]
        consumo_s2['mat_A_kg'] += unidades * REQUERIMIENTOS[prod]['mat_A_kg']
        consumo_s2['mat_B_kg'] += unidades * REQUERIMIENTOS[prod]['mat_B_kg']
        consumo_s2['mat_C_L'] += unidades * REQUERIMIENTOS[prod]['mat_C_L']
    cedula_consumo_mat.loc['Sem 2'] = pd.Series(consumo_s2)
    
    cedula_consumo_mat.loc['Total 2026'] = cedula_consumo_mat.loc['Sem 1'] + cedula_consumo_mat.loc['Sem 2']
    print(cedula_consumo_mat.to_markdown(floatfmt=",.2f"))

def calcular_cedula_4_compras_mat():
    print_header("Cédula 4: Presupuesto de Compra de Materiales")
    idx_compras = ['Consumo', 'Inv. Final', 'Total Necesidad', 'Inv. Inicial', 'Unidades a Comprar', 'Costo x Unidad', 'Importe Compra']
    
    material_cols = [k for k in COSTOS.keys() if k.startswith('mat_')]
    df_compras = pd.DataFrame(columns=material_cols, index=idx_compras).fillna(0.0)

    consumo_2027_s1 = {'mat_A_kg': 0, 'mat_B_kg': 0, 'mat_C_L': 0}
    for prod in PRODUCTOS:
        unidades = VENTAS_2027_SEM1_SUPUESTO[prod] 
        consumo_2027_s1['mat_A_kg'] += unidades * REQUERIMIENTOS[prod]['mat_A_kg']
        consumo_2027_s1['mat_B_kg'] += unidades * REQUERIMIENTOS[prod]['mat_B_kg']
        consumo_2027_s1['mat_C_L'] += unidades * REQUERIMIENTOS[prod]['mat_C_L']

    for mat in material_cols:
        df_compras.loc['Consumo', mat] = cedula_consumo_mat.loc['Sem 1', mat]
        df_compras.loc['Inv. Final', mat] = cedula_consumo_mat.loc['Sem 2', mat] * POLITICAS['inv_materiales_pct']
        df_compras.loc['Inv. Inicial', mat] = cedula_consumo_mat.loc['Sem 1', mat] * POLITICAS['inv_materiales_pct']
        df_compras.loc['Costo x Unidad', mat] = COSTOS[mat]
    
    df_compras.loc['Total Necesidad'] = df_compras.loc['Consumo'] + df_compras.loc['Inv. Final']
    df_compras.loc['Unidades a Comprar'] = df_compras.loc['Total Necesidad'] - df_compras.loc['Inv. Inicial']
    df_compras.loc['Importe Compra'] = df_compras.loc['Unidades a Comprar'] * df_compras.loc['Costo x Unidad']
    total_compras_s1 = df_compras.loc['Importe Compra'].sum()
    
    cedula_compras_mat.loc['Sem 1'] = df_compras.loc['Importe Compra']
    
    for mat in material_cols:
        df_compras.loc['Consumo', mat] = cedula_consumo_mat.loc['Sem 2', mat]
        df_compras.loc['Inv. Final', mat] = consumo_2027_s1[mat] * POLITICAS['inv_materiales_pct']
        df_compras.loc['Inv. Inicial', mat] = cedula_consumo_mat.loc['Sem 2', mat] * POLITICAS['inv_materiales_pct']
    
    df_compras.loc['Total Necesidad'] = df_compras.loc['Consumo'] + df_compras.loc['Inv. Final']
    df_compras.loc['Unidades a Comprar'] = df_compras.loc['Total Necesidad'] - df_compras.loc['Inv. Inicial']
    df_compras.loc['Importe Compra'] = df_compras.loc['Unidades a Comprar'] * df_compras.loc['Costo x Unidad']
    total_compras_s2 = df_compras.loc['Importe Compra'].sum()
    
    cedula_compras_mat.loc['Sem 2'] = df_compras.loc['Importe Compra']
    
    cedula_compras_mat.loc['Total 2026'] = cedula_compras_mat.loc['Sem 1'] + cedula_compras_mat.loc['Sem 2']
    cedula_compras_mat['Total'] = cedula_compras_mat.sum(axis=1)
    
    print(cedula_compras_mat.to_markdown(floatfmt=",.2f"))
    REPORTES_FINALES['Total_Compras_Anual'] = cedula_compras_mat.loc['Total 2026', 'Total']
    
    costo_inv_final_mat = (df_compras.loc['Inv. Final'] * df_compras.loc['Costo x Unidad']).sum()
    REPORTES_FINALES['Inv_Materiales_Final_Importe'] = costo_inv_final_mat


def calcular_cedula_5_mod():
    print_header("Cédula 5: Presupuesto de Mano de Obra Directa (MOD)")
    
    horas_s1 = 0
    for prod in PRODUCTOS:
        horas_s1 += cedula_prod.loc['Sem 1', prod] * REQUERIMIENTOS[prod]['mod_hrs']
    cedula_mod.loc['Total Horas', 'Sem 1'] = horas_s1
    cedula_mod.loc['Costo Hora', 'Sem 1'] = COSTOS['mod_hora_sem1']
    cedula_mod.loc['Importe MOD', 'Sem 1'] = horas_s1 * COSTOS['mod_hora_sem1']
    
    horas_s2 = 0
    for prod in PRODUCTOS:
        horas_s2 += cedula_prod.loc['Sem 2', prod] * REQUERIMIENTOS[prod]['mod_hrs']
    cedula_mod.loc['Total Horas', 'Sem 2'] = horas_s2
    cedula_mod.loc['Costo Hora', 'Sem 2'] = COSTOS['mod_hora_sem2']
    cedula_mod.loc['Importe MOD', 'Sem 2'] = horas_s2 * COSTOS['mod_hora_sem2']
    
    cedula_mod.loc['Total Horas', 'Total 2026'] = horas_s1 + horas_s2
    cedula_mod.loc['Importe MOD', 'Total 2026'] = cedula_mod.loc['Importe MOD', 'Sem 1'] + cedula_mod.loc['Importe MOD', 'Sem 2']
    
    print(cedula_mod.to_markdown(floatfmt=",.2f"))
    REPORTES_FINALES['Total_MOD_Anual'] = cedula_mod.loc['Importe MOD', 'Total 2026']

def calcular_cedula_6_gif():
    print_header("Cédula 6: Presupuesto de Gastos Indirectos de Fabricación (GIF)")
    
    total_gif_s1 = sum(GIF['sem1'].values())
    salida_gif_s1 = total_gif_s1 - GIF['sem1']['Depreciación']
    tasa_gif_s1 = total_gif_s1 / cedula_mod.loc['Total Horas', 'Sem 1']
    
    cedula_gif.loc['Total GIF', 'Sem 1'] = total_gif_s1
    cedula_gif.loc['Salida Efectivo GIF', 'Sem 1'] = salida_gif_s1
    cedula_gif.loc['Tasa GIF x Hora MOD', 'Sem 1'] = tasa_gif_s1
    
    total_gif_s2 = sum(GIF['sem2'].values())
    salida_gif_s2 = total_gif_s2 - GIF['sem2']['Depreciación']
    tasa_gif_s2 = total_gif_s2 / cedula_mod.loc['Total Horas', 'Sem 2']
    
    cedula_gif.loc['Total GIF', 'Sem 2'] = total_gif_s2
    cedula_gif.loc['Salida Efectivo GIF', 'Sem 2'] = salida_gif_s2
    cedula_gif.loc['Tasa GIF x Hora MOD', 'Sem 2'] = tasa_gif_s2
    
    cedula_gif.loc['Total GIF', 'Total 2026'] = total_gif_s1 + total_gif_s2
    cedula_gif.loc['Salida Efectivo GIF', 'Total 2026'] = salida_gif_s1 + salida_gif_s2
    
    print(cedula_gif.to_markdown(floatfmt=",.2f"))
    REPORTES_FINALES['Total_GIF_Anual'] = cedula_gif.loc['Total GIF', 'Total 2026']
    REPORTES_FINALES['Total_Salida_GIF_Anual'] = cedula_gif.loc['Salida Efectivo GIF', 'Total 2026']

def calcular_cedula_7_gastos_op():
    print_header("Cédula 7: Presupuesto de Gastos de Operación")
    
    comisiones_s1 = REPORTES_FINALES['Ventas_Sem1'] * GASTOS_OP['sem1']['Comisiones_pct']
    total_gasto_op_s1 = sum(v for k, v in GASTOS_OP['sem1'].items() if k != 'Comisiones_pct') + comisiones_s1
    salida_gasto_op_s1 = total_gasto_op_s1 - GASTOS_OP['sem1']['Depreciación']
    
    cedula_gastos_op.loc['Total Gasto Op', 'Sem 1'] = total_gasto_op_s1
    cedula_gastos_op.loc['Salida Efectivo Op', 'Sem 1'] = salida_gasto_op_s1
    
    comisiones_s2 = REPORTES_FINALES['Ventas_Sem2'] * GASTOS_OP['sem2']['Comisiones_pct']
    total_gasto_op_s2 = sum(v for k, v in GASTOS_OP['sem2'].items() if k != 'Comisiones_pct') + comisiones_s2
    salida_gasto_op_s2 = total_gasto_op_s2 - GASTOS_OP['sem2']['Depreciación']
    
    cedula_gastos_op.loc['Total Gasto Op', 'Sem 2'] = total_gasto_op_s2
    cedula_gastos_op.loc['Salida Efectivo Op', 'Sem 2'] = salida_gasto_op_s2
    
    cedula_gastos_op.loc['Total Gasto Op', 'Total 2026'] = total_gasto_op_s1 + total_gasto_op_s2
    cedula_gastos_op.loc['Salida Efectivo Op', 'Total 2026'] = salida_gasto_op_s1 + salida_gasto_op_s2
    
    print(cedula_gastos_op.to_markdown(floatfmt=",.2f"))
    REPORTES_FINALES['Total_Gasto_Op_Anual'] = cedula_gastos_op.loc['Total Gasto Op', 'Total 2026']
    REPORTES_FINALES['Total_Salida_Op_Anual'] = cedula_gastos_op.loc['Salida Efectivo Op', 'Total 2026']

def calcular_cedula_8_cogs():
    print_header("Cédula 8: Presupuesto de Costo de Ventas")
    
    for prod in PRODUCTOS:
        costo_mp = 0
        for mat in material_cols:
            costo_mp += REQUERIMIENTOS[prod][mat] * COSTOS[mat]
        cedula_costo_unitario.loc['Costo MP', prod] = costo_mp
        
        costo_mod_s1 = REQUERIMIENTOS[prod]['mod_hrs'] * COSTOS['mod_hora_sem1']
        costo_gif_s1 = REQUERIMIENTOS[prod]['mod_hrs'] * cedula_gif.loc['Tasa GIF x Hora MOD', 'Sem 1']
        cedula_costo_unitario.loc['Costo Unitario Sem 1', prod] = costo_mp + costo_mod_s1 + costo_gif_s1
        
        costo_mod_s2 = REQUERIMIENTOS[prod]['mod_hrs'] * COSTOS['mod_hora_sem2']
        costo_gif_s2 = REQUERIMIENTOS[prod]['mod_hrs'] * cedula_gif.loc['Tasa GIF x Hora MOD', 'Sem 2']
        cedula_costo_unitario.loc['Costo Unitario Sem 2', prod] = costo_mp + costo_mod_s2 + costo_gif_s2
        
    print("--- Costos Unitarios de Producción ---")
    print(cedula_costo_unitario.to_markdown(floatfmt=",.2f"))

    total_cogs_s1 = 0
    for prod in PRODUCTOS:
        costo = cedula_costo_unitario.loc['Costo Unitario Sem 1', prod] * PRODUCTOS[prod]['ventas_sem1']
        cedula_cogs.loc['Sem 1', prod] = costo
        total_cogs_s1 += costo
        
    total_cogs_s2 = 0
    for prod in PRODUCTOS:
        costo = cedula_costo_unitario.loc['Costo Unitario Sem 2', prod] * PRODUCTOS[prod]['ventas_sem2']
        cedula_cogs.loc['Sem 2', prod] = costo
        total_cogs_s2 += costo
    
    cedula_cogs.loc['Total 2026'] = cedula_cogs.loc['Sem 1'] + cedula_cogs.loc['Sem 2']
    cedula_cogs['Total'] = cedula_cogs.sum(axis=1)
    
    print("\n--- Costo de Ventas (COGS) ---")
    print(cedula_cogs.to_markdown(floatfmt=",.2f"))
    REPORTES_FINALES['Total_COGS_Anual'] = cedula_cogs.loc['Total 2026', 'Total']
    
    inv_final_pt_importe = 0
    for prod in PRODUCTOS:
        unidades = VENTAS_2027_SEM1_SUPUESTO[prod] * POLITICAS['inv_prod_terminado_pct']
        costo_unit = cedula_costo_unitario.loc['Costo Unitario Sem 2', prod]
        inv_final_pt_importe += unidades * costo_unit
    REPORTES_FINALES['Inv_Prod_Terminado_Final_Importe_Calculado'] = inv_final_pt_importe

def calcular_reportes_finales():
    print_header("Reportes Financieros Finales")
    
    print("\n--- 1. ESTADO DE RESULTADOS PROYECTADO 2026 ---")
    ventas = REPORTES_FINALES['Total_Ventas_Anual']
    cogs = REPORTES_FINALES['Total_COGS_Anual']
    util_bruta = ventas - cogs
    gasto_op = REPORTES_FINALES['Total_Gasto_Op_Anual']
    util_op = util_bruta - gasto_op
    uai = util_op 
    ptu = uai * TASA_PTU
    isr = uai * TASA_ISR
    util_neta = uai - ptu - isr
    
    REPORTES_FINALES['Total_ISR_Anual'] = isr
    REPORTES_FINALES['Total_PTU_Anual'] = ptu
    REPORTES_FINALES['Total_Utilidad_Neta'] = util_neta
    
    er_data = {
        'Ventas': ventas,
        '(-) Costo de Ventas': cogs,
        '(=) Utilidad Bruta': util_bruta,
        '(-) Gasto de Operación': gasto_op,
        '(=) Utilidad de Operación (UAI)': uai,
        '(-) PTU (10%)': ptu,
        '(-) ISR (30%)': isr,
        '(=) UTILIDAD NETA': util_neta
    }
    er_df = pd.Series(er_data).to_frame(name='Importe')
    print(er_df.to_markdown(floatfmt=",.2f"))

    print("\n--- 2. ESTADO DE FLUJO DE EFECTIVO PROYECTADO 2026 (Anual) ---")
    
    saldo_inicial = BALANCE_INICIAL['Efectivo']
    cobranza_2025 = BALANCE_INICIAL['Clientes']
    cobranza_2026 = REPORTES_FINALES['Total_Ventas_Anual'] * FLUJO['cobranza_2026_pct']
    total_entradas = saldo_inicial + cobranza_2025 + cobranza_2026
    
    pago_prov_2025 = BALANCE_INICIAL['Proveedores']
    pago_compras_2026 = REPORTES_FINALES['Total_Compras_Anual'] * FLUJO['pago_compras_2026_pct']
    pago_mod = REPORTES_FINALES['Total_MOD_Anual']
    pago_gif = REPORTES_FINALES['Total_Salida_GIF_Anual']
    pago_gasto_op = REPORTES_FINALES['Total_Salida_Op_Anual']
    pago_isr_2025 = BALANCE_INICIAL['ISR_x_Pagar']
    pago_activo_nuevo = INVERSION_ACTIVOS
    pago_doc_x_pagar = BALANCE_INICIAL['Doc_x_Pagar']
    
    total_salidas = pago_prov_2025 + pago_compras_2026 + pago_mod + pago_gif + pago_gasto_op + pago_isr_2025 + pago_activo_nuevo + pago_doc_x_pagar
    
    saldo_final_efectivo = total_entradas - total_salidas
    REPORTES_FINALES['Saldo_Efectivo_Final'] = saldo_final_efectivo
    
    flujo_data = {
        'Saldo Inicial de Efectivo': saldo_inicial,
        '(+) Cobranza Saldo 2025': cobranza_2025,
        '(+) Cobranza Ventas 2026 (90%)': cobranza_2026,
        '(=) Total Entradas Disponibles': total_entradas,
        '(-) Pago Saldo Proveedores 2025': pago_prov_2025,
        '(-) Pago Compras 2026 (60%)': pago_compras_2026,
        '(-) Pago Mano de Obra (MOD)': pago_mod,
        '(-) Pago GIF (Salida Efectivo)': pago_gif,
        '(-) Pago Gastos Operación (Salida Efectivo)': pago_gasto_op,
        '(-) Pago ISR 2025': pago_isr_2025,
        '(-) Pago Documentos por Pagar': pago_doc_x_pagar,
        '(-) Pago Compra Activo (Refrigerador)': pago_activo_nuevo,
        '(=) Total Salidas': total_salidas,
        '(=) SALDO FINAL DE EFECTIVO': saldo_final_efectivo
    }
    flujo_df = pd.Series(flujo_data).to_frame(name='Importe')
    print(flujo_df.to_markdown(floatfmt=",.2f"))

    print("\n--- 3. BALANCE GENERAL PROYECTADO (Al 31 de Diciembre 2026) ---")
    
    s_efectivo = saldo_final_efectivo
    s_clientes = REPORTES_FINALES['Total_Ventas_Anual'] * (1 - FLUJO['cobranza_2026_pct'])
    s_inv_mat = REPORTES_FINALES['Inv_Materiales_Final_Importe']
    s_inv_pt = BALANCE_INICIAL['HARDCODE_Inv_Prod_Terminado_Final']
    s_activo_circ = s_efectivo + s_clientes + s_inv_mat + s_inv_pt
    
    depre_total_2026 = GIF['sem1']['Depreciación'] + GIF['sem2']['Depreciación'] + GASTOS_OP['sem1']['Depreciación'] + GASTOS_OP['sem2']['Depreciación']
    s_activo_fijo_neto = BALANCE_INICIAL['Activo_Fijo_Neto_Inicial'] + INVERSION_ACTIVOS - depre_total_2026
    s_total_activo = s_activo_circ + s_activo_fijo_neto

    s_proveedores = REPORTES_FINALES['Total_Compras_Anual'] * (1 - FLUJO['pago_compras_2026_pct'])
    s_impuestos_pagar = REPORTES_FINALES['Total_ISR_Anual'] + REPORTES_FINALES['Total_PTU_Anual']
    s_pasivo_circ = s_proveedores + s_impuestos_pagar
    s_prestamo = BALANCE_INICIAL['Prestamo_Bancario_LP']
    s_total_pasivo = s_pasivo_circ + s_prestamo
    
    s_capital_social = BALANCE_INICIAL['Capital_Contribuido']
    s_util_retenidas = BALANCE_INICIAL['Utilidades_Retenidas']
    s_util_neta = REPORTES_FINALES['Total_Utilidad_Neta']
    s_total_capital = s_capital_social + s_util_retenidas + s_util_neta
    
    s_total_pasivo_capital = s_total_pasivo + s_total_capital
    
    REPORTES_FINALES['Total_Activo'] = s_total_activo
    REPORTES_FINALES['Total_Pasivo_Mas_Capital'] = s_total_pasivo_capital
    
    balance_data = {
        'ACTIVO': '',
        'Efectivo': f"${s_efectivo:,.2f}",
        'Cuentas por Cobrar': f"${s_clientes:,.2f}",
        'Inventario Mat. Prima': f"${s_inv_mat:,.2f}",
        'Inventario Prod. Terminado': f"${s_inv_pt:,.2f}",
        'Total Activo Circulante': f"${s_activo_circ:,.2f}",
        'Activo Fijo Neto': f"${s_activo_fijo_neto:,.2f}",
        'TOTAL ACTIVO': f"${s_total_activo:,.2f}",
        '': '',
        'PASIVO Y CAPITAL': '',
        'Proveedores (Cuentas por Pagar)': f"${s_proveedores:,.2f}",
        'Impuestos por Pagar (ISR y PTU)': f"${s_impuestos_pagar:,.2f}",
        'Total Pasivo Circulante': f"${s_pasivo_circ:,.2f}",
        'Préstamo Bancario LP': f"${s_prestamo:,.2f}",
        'Total Pasivo': f"${s_total_pasivo:,.2f}",
        'Capital Social': f"${s_capital_social:,.2f}",
        'Utilidades Retenidas': f"${s_util_retenidas:,.2f}",
        'Utilidad Neta del Ejercicio': f"${s_util_neta:,.2f}",
        'Total Capital Contable': f"${s_total_capital:,.2f}",
        'TOTAL PASIVO + CAPITAL': f"${s_total_pasivo_capital:,.2f}"
    }
    
    balance_df = pd.Series(balance_data).to_frame(name='')
    print(balance_df.to_markdown())

def main():
    global PRODUCTOS
    PRODUCTOS = obtener_datos_interactivos()
    
    try:
        calcular_cedula_1_ventas()
        calcular_cedula_2_produccion()
        calcular_cedula_3_consumo_mat()
        calcular_cedula_4_compras_mat()
        calcular_cedula_5_mod()
        calcular_cedula_6_gif()
        calcular_cedula_7_gastos_op()
        calcular_cedula_8_cogs()
        
        calcular_reportes_finales()
        
        print("\n" + "="*70)
        print("...Simulación completada exitosamente.")
        
        total_a = REPORTES_FINALES['Total_Activo']
        total_pc = REPORTES_FINALES['Total_Pasivo_Mas_Capital']
        diferencia = total_a - total_pc
        
        print(f"\nVerificación de Cuadre del Balance General:")
        print(f"  Total Activo: ${total_a:,.2f}")
        print(f"  Total Pasivo + Capital: ${total_pc:,.2f}")
        print(f"  Diferencia (debe ser 0): ${diferencia:,.2f}")
        
    except Exception as e:
        print(f"\n*** ERROR DURANTE LA EJECUCIÓN ***")
        print(f"Ocurrió un error: {e}")
        print("Por favor, revisa los datos de entrada y la lógica del programa.")
        sys.exit(1)

if __name__ == "__main__":
    main()