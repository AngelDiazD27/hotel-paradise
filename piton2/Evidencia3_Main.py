import csv


contactos = dict()

def registrar_cliente(contactos, claveCliente):
    """Funcion que registra los datos del cliente"""
    try:
        nombre = input("Nombre(s): ")
        apellido = input("Apellido(s): ")
        if apellido and nombre:
            contactos[claveCliente] = (apellido, nombre)
            print("cliente registrado exitosamente.")
            claveCliente += 1
        else:
            print("Error de ingreso.")
    except Exception:
        print("Error inesperado al registrar cliente.")
    return contactos, claveCliente


def registrar_sala(claveSalas, SalasActivas):

    try:
        nombre = input("Nombre de la sala : ")
        cupo = input(int("cupo de la sala : " ))
        if nombre and cupo:
            SalasActivas[claveSalas] = (nombre, cupo)
            print("sala registrada exitosamente.")
            claveSalas +=1
        else:
            print("error de ingreso.")
    except Exception:
        print("error inesperado al registrar la sala")
    return nombre, cupo , claveSalas

def pedir_telefono():
    """Funcion que pide el numero de telefono"""
    while True:
        telefono = input("Telefono: ")
        if telefono == "":
            return None
        if telefono.isdigit():
            return telefono
        print("ERROR, INGRESA EL TELEFONO CORRECTAMENTE. SOLO NUMEROS.")


def agregar_contacto(Contactos, clave):
    """Funcion que agrega los datos de los contactos"""

    while True:
        apellido = pedir_apellidos()
        if apellido is None:
            print("Registro cancelado.")
            continuar = input("¿Deseas intentar agregar otra persona? (s/n): ").lower()
            if continuar != "s":
                break
            else:
                continue

        nombre = pedir_nombres()
        if nombre is None:
            print("Registro cancelado.")
            continuar = input("¿Deseas intentar agregar otra persona? (s/n): ").lower()
            if continuar != "s":
                break
            else:
                continue

        telefono = pedir_telefono()
        if telefono is None:
            print("Registro cancelado.")
            continuar = input("¿Deseas intentar agregar otra persona? (s/n): ").lower()
            if continuar != "s":
                break
            else:
                continue

        datos = (apellido, nombre, telefono)
        Contactos[clave] = datos
        print("Contacto Agregado Exitosamente")
        clave += 1

        continuar = input("¿Deseas agregar otra persona? (s/n): ").lower()
        if continuar != "s":
            break

    return Contactos, clave


def modificar_contacto(contactos):
    """Funcion que modifica un contacto por su clave"""
    print(f"{'Clave':<3} \t {'Apellido':<15} \t {'Nombre':15} \t {'Telefono'}")
    print("*" * 80)
    for clave, datos in Contactos.items():
        print(f"{clave:<3} \t {datos[0]:<15} \t {datos[1]:<15} \t {datos[2]}")

    while True:
        clave_buscar = input("Ingresa la clave del contacto a modificar: ")
        if clave_buscar == "":
            print("Cancelando proceso, regresando al menu...")
            break
        if clave_buscar.isdigit():
            clave_buscar = int(clave_buscar)
        else:
            print("ERROR, LA CLAVE DEBE DE SER SOLO NUMERO")
            continue
        if clave_buscar in Contactos:
            print(f"Contacto actual: {Contactos[clave_buscar]}")

            apellido = pedir_apellidos()
            if apellido is None:
                apellido = Contactos[clave_buscar][0]

            nombre = pedir_nombres()
            if nombre is None:
                nombre = Contactos[clave_buscar][1]

            telefono = pedir_telefono()
            if telefono is None:
                telefono = Contactos[clave_buscar][2]

            Contactos[clave_buscar] = (apellido, nombre, telefono)
            print(f"Contacto con clave {clave_buscar} modificado exitosamente.")
            break
        else:
            print("Esa clave NO EXISTE")


def eliminar_contacto(Contactos):
    """Funcion para eliminar un contacto por su clave"""
    print(f"{'Clave':<3} \t {'Apellido':<15} \t {'Nombre':15} \t {'Telefono'}")
    print("*" * 80)
    for clave, datos in Contactos.items():
        print(f"{clave:<3} \t {datos[0]:<15} \t {datos[1]:<15} \t {datos[2]}")

    while True:
        clave_buscar = input("Ingresa la clave a eliminar: ")
        if clave_buscar == "":
            print("Cancelando proceso, regresando al menu...")
            break
        if clave_buscar.isdigit():
            clave_buscar = int(clave_buscar)
        else:
            print("ERROR, LA CLAVE DEBE DE SER SOLO NUMERO")
            continue
        if clave_buscar in Contactos:
            del Contactos[clave_buscar]
            print(f"Contacto con clave {clave_buscar} eliminado exitosamente.")
            break
        else:
            print("Esa clave NO EXISTE")


def reporte_contactos(Contactos):
    """Funcion que me muestra un reporte de los contactos que existen al momento"""
    print(f"{'Clave':<3} \t {'Apellido':<15} \t {'Nombre':15} \t {'Telefono'}")
    print("*" * 80)
    for clave, datos in Contactos.items():
        print(f"{clave:<3} \t {datos[0]:<15} \t {datos[1]:<15} \t {datos[2]}")


def exportar_contactos(Contactos, clave):
    """Funcion que exporta los contactos capturados a un archivo csv"""

    with open("Contactos.csv", "w", encoding="latin1", newline="") as archivo:
        grabador = csv.writer(archivo)
        grabador.writerow(("Clave", "Apellido(s)", "Nombre(s)", "Telefono"))

        for clave, datos in Contactos.items():
            grabador.writerow((clave, datos[0], datos[1], datos[2]))
    print("¡¡¡ARCHIVO GENERADO CORRECTAMENTE!!!")


def main(Contactos, clave):
    while True:
        print("\nBIENVENIDO AL PROGRAMA.")
        print("Opciones disponibles: ")
        print("1. Agregar Contacto.")
        print("2. Modificar Contacto.")
        print("3. Eliminar Contacto.")
        print("4. Reporte Total de Contactos.")
        print("5. Exportar Contactos Actuales.")
        print("6. Salir del programa.\n")
        opcion = input("Selecciona la opcion que necesites (1-6): ")
        if opcion.isdigit():
            if opcion == "1":
                Contactos, clave = agregar_contacto(Contactos, claveCliente)

            elif opcion == "2":
                modificar_contacto(Contactos, claveSalas)

            elif opcion == "3":
                eliminar_contacto(Contactos)

            elif opcion == "4":
                reporte_contactos(Contactos)

            elif opcion == "5":
                exportar_contactos(Contactos, clave)

            elif opcion == "6":
                break
            else:
                print("ERROR, INGRESA UNA OPCION VALIDA")
        else:
            print("ERROR, INGRESA UNA OPCION VALIDA")

    return Contactos, claveSalas, claveCliente

if __name__ == "__main__":
    Contactos = dict ()
    claveSalas = 1
    claveCliente = 1
    Contactos, claveSalas, claveCliente = main(Contactos, claveSalas, claveCliente)

