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
                Contactos, clave = agregar_contacto(Contactos, clave)

            elif opcion == "2":
                modificar_contacto(Contactos)

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

    return Contactos, clave


if __name__ == "__main__":
    Contactos = dict()
    clave = 1
    Contactos, clave = main(Contactos, clave)
