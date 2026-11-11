import datetime

contactos = dict()
salasActivas = dict()
claveCliente = 1
claveSala = 1
reservaciones = dict()
numeroFolio = 1

def ordenador(item):
    clave, (apellido, nombre) = item
    return (apellido, nombre)

while True:
    print("\n---Menu de opciones---")
    print("1. Registrar contacto")
    print("2. Registrar Sala")
    print("3. Registrar reservacion") 
    print("4. Modificar nombre de la reservacion")
    print("5. Consultar reservaciones")
    print("6. Salir del menu")

    opcion = input("Elige una opcion (1-6):")
    if opcion == "1":
        """Funcion que registra los datos del cliente"""
        while True:
            apellido = input("Apellido(s): ")
            nombre = input("Nombre(s): ")
            if apellido.replace (" ", "").isalpha() and nombre.replace(" ", "").isalpha():
                contactos[claveCliente] = (apellido, nombre)
                print("cliente registrado exitosamente.")
                claveCliente += 1
                continuar = input("si deseas registrar a otro cliente escribe si: ").lower()
                if continuar != "si":
                    break
            else:
                print("Error inesperado al registrar cliente.")
                break

    elif opcion == "2":
        """Opcion que registra los datos del sala"""
        while True:
            salaNombre = input("Escribe el nombre de la sala: ")
            cupo = input("Capacidad de la sala (especificar con numeros): ")
            if salaNombre.replace (" ", "") and cupo.replace(" ", "").isdigit():
                codigoSala = f"S{claveSala:02d}"#d = decimal de enteros
                salasActivas[codigoSala] = (salaNombre, cupo)
                print("Sala registrada exitosamente.")
                print(f"Clave de la sala: {codigoSala}")
                claveSala += 1
                continuar = input("Deseas registrar otra sala? (s/n)").lower()
                if continuar == "n":
                    break
            else:
                print("Error inesperado al registrar la sala.")
                break

    elif opcion == "3":
        """Opcion que registra reservacion"""
        print("Seleccion cliente para tu reservacion:")
        for clave, (apellido, nombre) in sorted(contactos.items(), key=ordenador):
            print(f"{clave}. {apellido}, {nombre}")

        try: 
            claveCliente = int(input("Ingresa la clave del cliente: "))
            if claveCliente not in contactos:
                print("Cliente no encontrado.")
                continue
            print("Selecciona la sala para tu reservacion:")
            for codigo, (salaNombre, cupo) in salasActivas.items():
                print(f"{codigo}. {salaNombre} (Cupo: {cupo})")

            
            codigoSala = input("Ingresa el codigo de la sala: ")
            if codigoSala not in salasActivas:
                print("Sala no encontrada.")
                continue
            fecha_str = input("Ingresa la fecha de la reservacion con 2 dias de anticipacion a la fecha de hoy (YYYY-MM-DD): ")
            try:
                fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
                fecha_actual = datetime.date.today()
                diferencia = (fecha - fecha_actual).days
                if diferencia < 2:
                    print("La fecha debe tener al menos 2 días de anticipación respecto a hoy.")
                    continue
            except ValueError:
                print("Formato de fecha incorrecto.")
                continue

            # Revisar si el turno ya está ocupado para la sala y fecha
            turno = input("Ingresa el turno (Matutino/Vespertino/Nocturno): ").lower()
            if turno == "matutino":
                hora = datetime.time(9, 0)
            elif turno == "vespertino":
                hora = datetime.time(15, 0)
            elif turno == "nocturno":
                hora = datetime.time(19, 0)
            else:
                print("Turno no válido.")
                continue

            ocupado = False
            for _, (c, s, f, h, _) in reservaciones.items():
                if s == codigoSala and f == fecha and h == hora:
                    ocupado = True
                    break
            if ocupado:
                print("Ese turno ya está reservado para esta sala en esa fecha.")
                continue
            NombreReservacion = input("Como se llama el Evento: ")
           
            reservacion_id = len(reservaciones) + 1
            reservaciones[reservacion_id] = (claveCliente, codigoSala, fecha, hora, NombreReservacion )
            print(f"Id de la reservacion: {reservacion_id}")
            print("Reservacion registrada exitosamente.")            
        except ValueError:
            print("Entrada invalida. Intenta de nuevo.")
            continue
    
    elif opcion == "4":
        FolioACambiar = input("Ingresa el id de la reservacion: ")
        try:
            FolioACambiar = int(FolioACambiar)
        except ValueError:
            print("Id de reservacion invalido.")
            continue
        if FolioACambiar not in reservaciones:
            print("Reservacion no encontrada")
        else:
            datos = reservaciones[reservacion_id]
            print(f"Nombre actual del evento: {NombreReservacion}")
            nuevo_nombre = input("Ingresa el nuevo nombre del evento: ")
            NombreReservacion = nuevo_nombre
            reservaciones[reservacion_id] = (claveCliente, codigoSala, fecha, hora, NombreReservacion)
            
            for reservacion_id, (claveCliente, codigoSala, fecha, hora, NombreReservacion) in reservaciones.items():
                print(f"Id: {reservacion_id}, Cliente: {claveCliente}, Sala: {codigoSala}, Fecha: {fecha}, Hora: {hora}, Evento: {NombreReservacion}")
            print("Nombre del evento actualizado exitosamente.")

    elif opcion == "5":
        fecha_str = input("Ingresa la fecha para el reporte (YYYY-MM-DD): ")
        try:
            fecha_reporte = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            print("Formato de fecha incorrecto.")
            continue

        # Filtrar reservaciones por la fecha solicitada
        reservas_filtradas = [(reservacion_id, claveCliente, codigoSala, fecha, hora, NombreReservacion)
            for reservacion_id, (claveCliente, codigoSala, fecha, hora, NombreReservacion ) in reservaciones.items()
                if fecha == fecha_reporte]

        if not reservas_filtradas:
            print("No hay reservaciones para esta fecha.")
        else:
            print("\n REPORTE DE RESERVACIONES PARA EL DÍA", fecha_str, "")
            print("**")
            print("SALA\tCLIENTE\t\tEVENTO\t\t\t\t\t\t\t\tTURNO")
            print("**")

            for reservacion_id, claveCliente, codigoSala, fecha, hora, NombreReservacion in reservas_filtradas:
                cliente = contactos.get(claveCliente, "Cliente no encontrado.")
                sala = salasActivas.get(codigoSala, "Sala no encontrada.")
                evento = f"Evento de {cliente[0]}"  # O algún evento específico si se quiere agregar
                turno = "Matutino" if hora == datetime.time(9, 0) else "Vespertino" if hora == datetime.time(15, 0) else "Nocturno"

                print(f"{codigoSala}\t{cliente[0]}, {cliente[1]}\t{evento}\t{turno}\t{NombreReservacion}")

            print("**")
            print("FIN DEL REPORTE")
            break

    elif opcion == "6":
        print("Saliendo del menu...")
        break
    else:
        print("Opcion no valida, intenta de nuevo")

