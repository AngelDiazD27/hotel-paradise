import datetime
import csv
                                                                                                            
contactos = dict()
salasActivas = dict()
claveCliente = 1
claveSala = 1
reservaciones = dict()
numeroFolio = 1


while True:
    print("\n \t---Menu---\t")
    print("1. Registrar reservacion")
    print("2. Editar nombre de la reservacion")
    print("3. Consultar reservaciones") 
    print("4. Registrar contacto")
    print("5. Registrar Sala")
    print("6. Salir del menu")
    opcion = input("Elige una opcion (1-6):")     


    if opcion == "1":
        """Opcion que registra las reservaciones"""
        salir = False
        while not salir:
            if not contactos:
                print("No hay clientes registrados. Por favor, registra un cliente primero.")
                salir = True
                break
            print("\nSelecciona cliente para tu reservación:")
            print(f"{'CLAVE':<10}{'APELLIDO':<20}{'NOMBRE':<20}")
            for clave, (apellido, nombre) in sorted(contactos.items(), key=lambda x: x[1][0].lower()): 
                print(f"{clave:<10}{apellido:<20}{nombre:<20}")

            dato = input("\nIngresa la clave del cliente: ")
            if not dato.isdigit():
                print("Error: la clave debe ser un número.")
                respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                if respuesta == "s":
                    salir = True
                    break
                else:
                    continue

            claveCliente_reservacion = int(dato)
            if claveCliente_reservacion not in contactos:
                print("Cliente no encontrado.")
                respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                if respuesta == "s":
                    salir = True
                    break
                else:
                    continue
            break

        if salir:
            continue

        while True:
            fecha_str = input("Ingresa la fecha de la reservación con 2 dias de anticipacion (DD/MM/YYYY): ")
            try:
                fecha_reservacion = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
                fecha_actual = datetime.date.today()
                if (fecha_reservacion - fecha_actual).days < 2:
                    print("La fecha debe tener al menos 2 días de anticipación.")
                    respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                    if respuesta == "s":
                        salir = True
                        break
                    else:
                        continue
                break

            except ValueError:
                print("Formato de fecha incorrecto. Usa DD/MM/YYYY.")
                respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                if respuesta == "s":
                    salir = True
                    break              
        if salir:
            continue

        salas_disponibles = {}
        for codigo_sala, (nombre_sala, cupo_sala) in salasActivas.items():
                # Obtener los turnos ya ocupados para esta sala y fecha
            turnos_ocupados = [
            turno_reservado
            for _, (cliente_id, sala_id, fecha, turno_reservado, _) in reservaciones.items()
            if sala_id == codigo_sala and fecha == fecha_reservacion
                        ]
            # Si la sala tiene al menos un turno disponible, la agregamos
            if len(turnos_ocupados) < 3:  # 3 posibles turnos
                            salas_disponibles[codigo_sala] = (nombre_sala, cupo_sala)
        if not salas_disponibles:
            print("No hay salas disponibles para esa fecha.")
            salir = True
            if salir:
                continue
        
        while True:
            print("\nSalas disponibles para la fecha seleccionada:")
            print(f"{'CLAVE':<15}{'NOMBRE':<25}{'CUPO':<10}")
            for codigo, (salaNombre, cupo) in salas_disponibles.items():
                print(f"{codigo:<15}{salaNombre:<25}{cupo:<10}")

            codigoSala = input("Ingresa la clave de la sala: ")
            if codigoSala not in salas_disponibles:
                print ("Sala no encontrada o no disponible en la fecha seleccionada.")
                respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                if respuesta == "s":
                    salir = True
                    break
                else:
                    continue
            break
        if salir:
            continue
        
        turnos_disponibles = ("Matutino", "Vespertino", "Nocturno")
        turnos_ocupados = [
            turno_reservado
            for nombre_res, (cliente_id, sala_id, fecha, turno_reservado, nombre_res) in reservaciones.items()
            if sala_id == codigoSala and fecha == fecha_reservacion
        ]
        turnos_libres = [turno for turno in turnos_disponibles if turno not in turnos_ocupados]
        if not turnos_libres:
            print("No hay turnos disponibles para esa fecha")
            salir = True
            continue
        
        while True:
            turno = input(f"Elige un turno disponible {turnos_libres}: ").capitalize()
            if turno in turnos_libres:
                break
            else:
                print("Turno no válido o ya ocupado.")
                respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
                if respuesta == "s":
                    salir = True
                    break
        if salir:
            continue

        while True:
            nombre_evento = input("Nombre del evento: ").strip()
            if nombre_evento != "":
                break
            print("El nombre del evento no puede estar vacío.")
            respuesta = input("Toque la tecla [s] para cancelar operacion, sino toque cualquier tecla: ").lower()
            if respuesta == "s":
                salir = True
                break
        if salir:
            continue

        reservacion_id = len(reservaciones) + 1
        reservaciones[reservacion_id] = (claveCliente_reservacion, codigoSala, fecha_reservacion, turno, nombre_evento)
        print("\nReservación registrada exitosamente.")


    elif opcion == "2":
        """Opcion que modifica el nombre de la reservacion"""
        if not reservaciones:
            print("No hay reservaciones para modificar.")
            continue

        print("\nIngrese el rango de fechas para buscar la reservacion a modificar.")
        while True:
            fecha_inicio = input("Ingresa la fecha de inicio (DD/MM/YYYY): ")
            fecha_fin = input("Ingresa la fecha final (DD/MM/YYYY): ")
            try:
                fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
                fecha_fin = datetime.datetime.strptime(fecha_fin, "%d/%m/%Y").date()
                if fecha_inicio > fecha_fin:
                    print("La fecha de inicio no puede ser posterior a la fecha final.")
                    continue
                break
            except ValueError:
                print("Formato de fecha incorrecto. Usa DD/MM/YYYY.")
                continue

        rango_reservacion = {
            reservacion_id: (idCliente, codigoSala, fecha, turno, NombreReservacion)
            for reservacion_id, (idCliente, codigoSala, fecha, turno, NombreReservacion) in reservaciones.items()
            if fecha_inicio <= fecha <= fecha_fin
        }

        if not rango_reservacion:
            print("No hay reservaciones en el rango de fechas especificado.")
            continue

        print("\nReservaciones encontradas:")
        print(f"{'FOLIO':<15}{'CLIENTE':<30}{'SALA':<15}{'FECHA':<15}{'TURNO':<15}{'EVENTO':<30}")
        for reservacion_id, (idCliente, codigoSala, fecha, turno, NombreReservacion) in rango_reservacion.items():
            cliente = contactos.get(idCliente, ("Desconocido", ""))
            nombre_cliente = f"{cliente[0]} {cliente[1]}"
            print(f"{str(reservacion_id):<15}"
                  f"{nombre_cliente:<30}{codigoSala:<15}{fecha.strftime('%d/%m/%Y'):<15}{turno:<15}{NombreReservacion:<30}")

        FolioACambiar = input("Ingresa la clave de la reservación a cambiar: ")
        try:
            FolioACambiar = int(FolioACambiar)
        except ValueError:
            print("Clave de reservación inválida.")
            continue

        if FolioACambiar not in rango_reservacion:
            print("Reservación no encontrada en el rango de fechas.")
            continue

        idCliente, codigoSala, fecha, turno, NombreReservacion = reservaciones[FolioACambiar]
        print(f"Nombre actual del evento: {NombreReservacion}")
        nuevo_nombre = input("Ingresa el nuevo nombre del evento: ").strip()
        if nuevo_nombre:
            reservaciones[FolioACambiar] = (idCliente, codigoSala, fecha, turno, nuevo_nombre)
            print("Nombre del evento actualizado exitosamente.")
        else:
            print("El nombre no puede estar vacío.")


    elif opcion == "3":
        """Opcion que consulta las reservaciones"""
        while True:
            fecha_str = input("\nIngresa la fecha para el reporte (DD/MM/YYYY): ")
            try:
                fecha_reporte = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except ValueError:
                print("Formato de fecha incorrecto.")
                continue
            

            reservas_filtradas = [(reservacion_id, idCliente, codigoSala, fecha, hora, NombreReservacion)
                for reservacion_id, (idCliente, codigoSala, fecha, hora, NombreReservacion ) in reservaciones.items()
                    if fecha == fecha_reporte]
            
            if not reservas_filtradas:
                print("No hay reservaciones para esta fecha.")
                break
            else:
                print("*"*80)
                print(f"{'**' :<10} REPORTE DE RESERVACIONES PARA EL DÍA: {fecha_str}  {'**':>10}")
                print(f"{'SALA':<10}{'CLIENTE':<30}{'EVENTO':<25}{'TURNO':<15}")
                print("*"*80)

                for reservacion_id, idCliente, codigoSala, fecha, hora, NombreReservacion in reservas_filtradas:
                    cliente = contactos.get(idCliente, "Cliente no encontrado.")
                    sala = salasActivas.get(codigoSala, "Sala no encontrada.")
                    evento = f"{NombreReservacion}"  
                    nombre_cliente = f"{cliente[0]} {cliente[1]}"
                    print(f"{codigoSala:<10}{nombre_cliente:<30}{evento:<25}{turno:<15}")

                print(("*" * 33) + "FIN DEL REPORTE" + ("*" * 33))
                break

        exportar_csv = input("Desea guardar el reporte en un archivo CSV? Escribe 's' para guardar o cualquier otra tecla para no guardar: "
                                ).lower()
        if exportar_csv == 's':
            nombre_archivo = input("Escribe el nombre del archivo (sin extensión): ").strip()
            if nombre_archivo == "":
                nombre_archivo = "reporte_reservaciones"
            nombre_archivo += ".csv"
            try:
                with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
                    escritor = csv.writer(archivo_csv)

                    escritor.writerow(["*" * 80])
                    escritor.writerow([f"{'**' :<10} REPORTE DE RESERVACIONES PARA EL DÍA: {fecha_str}  {'**':>10}"])
                    escritor.writerow([f"{'SALA':<10}{'CLIENTE':<30}{'EVENTO':<25}{'TURNO':<15}"])
                    escritor.writerow(["*" * 80])

                    for reservacion_id, idCliente, codigoSala, fecha, hora, NombreReservacion in reservas_filtradas:
                        cliente = contactos.get(idCliente, ("Desconocido", ""))
                        nombre_cliente = f"{cliente[0]} {cliente[1]}"
                        escritor.writerow([f"{codigoSala:<10}{nombre_cliente:<30}{evento:<25}{turno:<15}"])
                        escritor.writerow(["*" * 33 + "FIN DEL REPORTE" + "*" * 33])
                print(f"Reporte guardado exitosamente como '{nombre_archivo}'.")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}") 
 

    elif opcion == "4":
        """Funcion que registra los datos del cliente"""
        while True:
            apellido = input("\nApellido(s): ")
            nombre = input("Nombre(s): ") 
            if not (apellido.replace (" ", "").isalpha() and nombre.replace(" ", "").isalpha()):
                print("Error al agregar cliente, solo se permiten letras. Introduzca nuevamente.")
                continue
            contactos[claveCliente] = (apellido, nombre)
            print("cliente registrado exitosamente.")
            print(f"Clave del cliente: {claveCliente}")
            claveCliente += 1
            break


    elif opcion == "5":
        """Opcion que registra los datos de la sala"""
        while True:
            salaNombre = input("\nEscribe el nombre de la sala: ")
            if not (salaNombre.replace (" ", "").strip()):
                print("Error al agregar sala, el nombre no puede estar vacio y el cupo debe ser numerico.")
                continue
            else:
                break
        while True:
            cupo = input("Capacidad de la sala (especificar con numeros): ")
            if not cupo.isdigit() or cupo <= "0":
                print("El cupo debe ser una cantidad numerica y mayor a 0.")
                continue
            else:
                break
        codigoSala = f"S{claveSala:02d}"
        salasActivas[codigoSala] = (salaNombre, cupo)
        print("Sala registrada exitosamente.")
        print(f"Clave de la sala: {codigoSala}")
        claveSala += 1  

    elif opcion == "6":
        print("Saliendo del menu...")
        break
    else:
        print("Opcion no valida, intenta de nuevo")