import sys
import os
import json
import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment





ventas = float(input("Ingrese el monto de las ventas: "))
Costo_ventas = float(input("Ingrese el costo de las ventas: "))
Utilidad_bruta = ventas - Costo_ventas
print("La utilidad bruta es: ", Utilidad_bruta)

Gasto_ventas = float(input("Ingrese el gasto de ventas: "))
Gasto_admin = float(input("Ingrese el gasto administrativo: "))
gasto_depreciacion = float(input("Ingrese el gasto de depreciación: "))
Utilidad_operacion= Utilidad_bruta - (gasto_depreciacion + Gasto_admin + Gasto_ventas)
print("La utilidad de operación es: ", Utilidad_operacion)

Gasto_financiero = float(input("Ingrese el gasto financiero: "))
productos_financieros = float(input("Ingrese los productos financieros: "))
Resultado_integral = Gasto_financiero - productos_financieros
print("El resultado integral es: ", Resultado_integral)

Otros_gastos = float(input("Ingrese otros gastos: "))
otros_productos = float(input("Ingrese otros productos: "))
Partidas_descontinuas= Otros_gastos-    otros_productos
print("Las partidas descontinuas son: ", Partidas_descontinuas)

Utilidad_antes_impuestos = Utilidad_operacion - (Resultado_integral + Partidas_descontinuas)
print("La utilidad antes de impuestos es: ", Utilidad_antes_impuestos)


ISR = float(input("Ingrese el monto del ISR: ")) / 100
PTU = float(input("Ingrese el monto de la PTU: ")) / 100

Utilidad_neta= Utilidad_antes_impuestos - (Utilidad_antes_impuestos * ISR) - (Utilidad_antes_impuestos * PTU)
print("La utilidad neta es: ", Utilidad_neta)

datos_ER= {
    "Ventas": ventas,
    "Costo de Ventas": Costo_ventas,
    "Utilidad Bruta": Utilidad_bruta,
    "Gasto de Ventas": Gasto_ventas,
    "Gasto Administrativo": Gasto_admin,
    "Gasto de Depreciación": gasto_depreciacion,
    "Utilidad de Operación": Utilidad_operacion,
    "Gasto Financiero": Gasto_financiero,
    "Productos Financieros": productos_financieros,
    "Resultado Integral": Resultado_integral,
    "Otros Gastos": Otros_gastos,
    "Otros Productos": otros_productos,
    "Partidas Descontinuas": Partidas_descontinuas,
    "Utilidad Antes de Impuestos": Utilidad_antes_impuestos,
    "ISR (%)": ISR * 100,
    "PTU (%)": PTU * 100,
    "Utilidad Neta": Utilidad_neta
}

#BALANCE GENERAL

bancos = float(input("Bancos: "))
clientes = float(input("Clientes: "))
inventarios = float(input("Inventarios: "))
papeleria = float(input("Papelería y útiles: "))
total_activo_circulante = bancos + clientes + inventarios + papeleria
print("El total del activo circulante es: ", total_activo_circulante)

Terrenos_edificios = float(input("Terrenos y edificios: "))
Maquinaria_equipo = float(input("Maquinaria y equipo: "))
Depreciacion_ac_maquinaria = float(input("Depreciación acumulada (maquinaria): "))
Mobiliario = float(input("Mobiliario y equipo de oficina: "))
equipo_transporte = float(input("Equipo de transporte: "))
equipo_computo = float(input("Equipo de cómputo: "))
depreciacion_acumulada_activo_fijo = float(input("Depreciación acumulada (activo fijo): "))
inversiones_permanente = float(input("Inversiones permanentes: "))

total_activo_fijo = (Terrenos_edificios + Maquinaria_equipo + Mobiliario + equipo_computo+ equipo_transporte+inversiones_permanente) - (Depreciacion_ac_maquinaria + depreciacion_acumulada_activo_fijo)
print("El total del activo fijo es: ", total_activo_fijo)

Otros_activos = float(input("Gastos de instalación: "))

total_activo= total_activo_circulante+ total_activo_fijo + Otros_activos

print("El total del activo es: ", total_activo)

proveedores = float(input("Proveedores: "))
acreedores = float(input("Acreedores: "))
impuestos_por_pagar = float(input("Impuestos por pagar: "))
anticipo_pagar = float(input("Anticipo por pagar: "))
gast_pagar = float(input("Gastos por pagar: "))
hipotecas = float(input("Hipotecas por pagar: "))
prestamos_bancarios = float(input("Préstamos bancarios: "))
total_pasivo_cl = proveedores + acreedores + impuestos_por_pagar + anticipo_pagar + gast_pagar + hipotecas + prestamos_bancarios
print("El total del pasivo a corto plazo es: ", total_pasivo_cl)
hipotecas_lp = float(input("Hipotecas por pagar a largo plazo: "))
prestamos_bancarios_lp = float(input("Préstamos bancarios a largo plazo: "))
total_pasivo_lp = hipotecas_lp + prestamos_bancarios_lp
total_pasivo = total_pasivo_cl + total_pasivo_lp
print("El total del pasivo es: ", total_pasivo)


capital_social = float(input("Capital social: "))
utilidades_retenidas = float(input("Utilidades retenidas: "))
reserva_legal = float(input("Reserva legal: "))
utilidad_ejercicio = float(input("Utilidad del ejercicio: "))

total_capital_contable = total_activo- total_pasivo
print("El total del capital contable es: ", total_capital_contable)
total_pasivo_capital_contable = total_pasivo + total_capital_contable
print("El total del pasivo más capital contable es: ", total_pasivo_capital_contable)



def calcular_razones_actividad(vtas, cv, inv, cxc, cxp, anc, atot, ct):

    razones = {
        "Rotación de Inventarios"        : (cv,   inv,  "CV / INV"),
        "Rotación de CxC"                : (vtas, cxc,  "VTAS / CXC"),
        "Rotación de CxP"                : (cv,   cxp,  "CV / CXP"),
        "Rotación de Activos Fijos"      : (vtas, anc,  "VTAS / ANC"),
        "Rotación de Activos Totales"    : (vtas, atot, "VTAS / Atot"),
        "Rotación de Capital de Trabajo" : (vtas, ct,   "VTAS / CT"),
    }

    print("\n   RAZONES DE ACTIVIDAD")
    
    for nombre, (numerador, denominador, formula) in razones.items():
        print(f"\n  {nombre}")
        print(f"  Fórmula  : {formula}")
        try:
            if denominador == 0:
                raise ZeroDivisionError
            resultado = numerador / denominador
            print(f"  Resultado: {resultado:.2f} veces")
        except ZeroDivisionError:
            print(f"  Resultado: No calculable (denominador = 0)")
        except Exception as e:
            print(f"  Resultado: Error inesperado → {e}")

    print("\n" + "-" * 45)



ct   = total_activo_circulante - total_pasivo_cl   

calcular_razones_actividad(
    vtas = ventas,
    cv   = Costo_ventas,
    inv  = inventarios,
    cxc  = clientes,
    cxp  = proveedores,
    anc  = total_activo_fijo,
    atot = total_activo,
    ct   = ct
)



def calcular_razones_liquidez(activo_circulante, pasivo_circulante, inventarios):
    print("\n   Razones de Liquidez")
    
    print("\n  Razón Corriente")
    print("  Fórmula  : Activo Circulante / Pasivo a Corto Plazo")
    try:
        if pasivo_circulante == 0:
            raise ZeroDivisionError
        razon_corriente = activo_circulante / pasivo_circulante
        print(f"  Resultado: {razon_corriente:.2f} veces")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    print("\n  Prueba Ácida")
    print("  Fórmula  : (Activo Circulante - Inventarios) / Pasivo a Corto Plazo")
    try:
        if pasivo_circulante == 0:
            raise ZeroDivisionError
        prueba_acida = (activo_circulante - inventarios) / pasivo_circulante
        print(f"  Resultado: {prueba_acida:.2f} veces")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    print("\n  Capital de Trabajo Neto")
    print("  Fórmula  : Activo Circulante - Pasivo a Corto Plazo")
    cap_trabajo = activo_circulante - pasivo_circulante
    print(f"  Resultado: ${cap_trabajo:,.2f}")

    print("\n" + "-" * 45)


calcular_razones_liquidez(
    activo_circulante = total_activo_circulante,
    pasivo_circulante = total_pasivo_cl,
    inventarios = inventarios
)



def calcular_razones_endeudamiento(activo_circulante, pasivo_circulante, inventarios):
    print("\n   Razones de Endeudamiento")
    
    print("\n  Razón de Endeudamiento")
    
    try:
        if pasivo_circulante == 0:
            raise ZeroDivisionError
        calcular_razones_endeudamiento = total_pasivo / total_activo
        print(f"  Resultado: {calcular_razones_endeudamiento:.2f} veces")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    try:
        if pasivo_circulante == 0:
            raise ZeroDivisionError
        
        print("\n  Razón capital")
        Razon_capital = total_capital_contable / total_activo
        print(f"  Resultado: {Razon_capital:.2f} veces")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    try:
        print("\n  Apalancamiento Financiero")
        apalancamiento_financiero= total_pasivo_lp / capital_social
        print(f"  Resultado: ${apalancamiento_financiero:,.2f}")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    try:
        print("\n  Razón de Cobertura de Intereses")
        cobertura_intereses = Utilidad_operacion / Gasto_financiero
        print(f"  Resultado: {cobertura_intereses:.2f} veces")
    except ZeroDivisionError:
        print("  Resultado: No calculable (denominador = 0)")

    print("\n" + "-" * 45)

calcular_razones_endeudamiento(
    activo_circulante = total_activo_circulante,
    pasivo_circulante = total_pasivo_cl,
    inventarios = inventarios
)


def main():
    datos = None
    while True:
        print("\n--- MENÚ ---")
        print("[1] Cargar archivo Excel")
        print("[2] Calcular razones de rentabilidad")
        print("[3] Calcular razones de liquidez")
        print("[4] Calcular razones de endeudamiento")
        print("[5] Calcular razones de mercado")
        print("[6] Calcular razones de actividad")
        print("[7] Exportar resultados a excel")
        print("[8] Mostrar datos cargados")
        print("[9] Salir")

        try:
            op = input("\nElige una opción: ").strip()
            if op == "1":
                print("Archivo cargado exitosamente.")

            elif op == "2":
                print("\n")


            elif op == "3":
                print("\n")


            elif op == "4":
                print("\n")


            elif op == "5":
                print("\n")


            elif op == "6":
                print("\n")

            elif op == "7":
                print("\n")

            elif op == "8":
                print("\n")

            elif op == "9":
                print("\n")

                try:
                    confirmacion = input("Esta seguro que desea salir? (S/N): ").strip()
                    if not confirmacion.isalpha():
                        continue
                    if not (confirmacion.upper() == "N" or  confirmacion.upper() == "S"):
                        print(f"La opcion {confirmacion} no esta dentro de las opciones validas. Intenta de nuevo.")
                        continue
                    if confirmacion.upper()== "N":
                        continue
                    else:
                        print("Saliendo del programa...")
                        break
                except Exception:
                    print(f"Ocurrió un problema: {sys.exc_info()[0:2]}")
                    continue
            else:
                print("Opción no válida.")

        except ValueError:
            print("La opcion proporcionada no es valida, intente de nuevo...")
            continue
        except Exception:
            print(f"Ocurrió un problema: {sys.exc_info()[0:2]}")
            continue


if __name__ == "__main__":
    main()