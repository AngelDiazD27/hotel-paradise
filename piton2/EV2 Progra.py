class Persona:
    "Clase que representa a una persona"

    def __init__(self, apellidos, nombres):
        self._apellidos = apellidos
        self._nombres = nombres

    @property
    def apellidos(self):
        return self._apellidos

    @apellidos.setter
    def apellidos(self, apellidos):
        if isinstance(apellidos, str) and apellidos.isalpha():
            self._apellidos = apellidos
        else:
            raise ValueError("Los apellidos deben de ser una cadena")

    @property
    def nombres(self):
        return self._nombres

    @nombres.setter
    def nombres(self, nombres):
        if isinstance(nombres, str) and nombres.isalpha():
            self._nombres = nombres
        else:
            raise ValueError("Los apellidos deben de ser una cadena")

    def describir(self):
        print(
            f"Esta es una persona que se apellida {self.apellidos} y se llama {self.nombres}"
        )


class Empleado(Persona):
    "Clase que representa a un Empleado"

    def __init__(self, apellidos, nombres, clave):
        super().__init__(apellidos, nombres)
        self._clave = clave

        @property
        def clave(self):
            return self._clave

        @clave.setter
        def clave(self, clave):
            if isinstance(clave, int) and clave > 0:
                self._clave = clave
            else:
                raise ValueError("La clave debe de ser un numero entero positivo")

    def describir(self):
        print(
            f"Este es un empleado que se apellida {self.apellidos} y se llama {self.nombres} con clave {self._clave}"
        )


class Paciente(Persona):
    "Clase que representa a un Paciente"

    def __init__(self, apellidos, nombres, clave, sexo):
        super().__init__(apellidos, nombres)
        self.clave = clave
        self.sexo = sexo

    @property
    def clave(self):
        return self._clave

    @clave.setter
    def clave(self, clave):
        if isinstance(clave, int) and clave > 0:
            self._clave = clave
        else:
            raise ValueError("La clave debe de ser un numero entero positivo")

    @property
    def sexo(self):
        return self._sexo

    @sexo.setter
    def sexo(self, sexo):
        if sexo.lower() in ["hombre", "mujer"]:
            self._sexo = sexo
        else:
            raise ValueError("Por favor, elija un sexo válido: 'Hombre' o 'Mujer'.")

def datos_persona():
    """Funcion para ingresar los datos para la clase Persona"""
    try:
        apellidos = input("Ingrese apellidos: ")
        nombres = input("Ingrese nombres: ")
        persona = Persona(apellidos, nombres)
        return persona
    except ValueError as e:
        print(f"Error: {e}")
        return None


def datos_empleado():
    """Funcion para ingresar los datos para la clase Empleados"""
    try:
        apellidos = input("Ingrese apellidos: ")
        nombres = input("Ingrese nombres: ")
        clave = int(input("Ingrese clave del empleado: "))
        empleado = Empleado(apellidos, nombres, clave)
        return empleado
    except ValueError as e:
        print(f"Error: {e}")
        return None


def datos_paciente():
    """Funcion para ingresar los datos para la clase Paciente"""
    try:
        apellidos = input("Ingrese apellidos: ")
        nombres = input("Ingrese nombres: ")
        clave = int(input("Ingrese clave del paciente: "))
        sexo = input("Ingrese sexo (Hombre/Mujer): ")
        paciente = Paciente(apellidos, nombres, clave, sexo)
        return paciente
    except ValueError as e:
        print(f"Error: {e}")
        return None

print("Datos Persona")
una_persona = datos_persona()
if una_persona:
    una_persona.describir()

print("\nDatos Empleado")
un_empleado = datos_empleado()
if un_empleado:
    un_empleado.describir()

print("\nDatos Paciente")
un_paciente = datos_paciente()
if un_paciente:
    print(f"Paciente: {un_paciente.nombres} {un_paciente.apellidos}, Clave: {un_paciente.clave}, Sexo: {un_paciente.sexo}")

