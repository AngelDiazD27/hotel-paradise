("-----Polimorfismo-----")
# - El polimorfismo basicamente llama al metodo de la clase que se esta utilizando en ese momento 
#   y adapta el tipo de objeto.
# Se puede usar el mismo nombre de metodo en diferentes clases, y cada clase puede tener su propia implementacion de ese metodo.
# Esto permite que diferentes objetos respondan de manera diferente al mismo mensaje o llamada de metodo.

"Ejemplo de polimorfismo"
class Persona: #Clase base, superclase
    """Representa a una persona genérica."""

    def __init__(self, nombre, edad):
        """Inicializa una nueva persona."""

        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        """Saluda a la persona por su nombre."""

        print(f"Hola, me llamo {self.nombre}")

class Estudiante(Persona): #Clase derivada, subclase
    """Representa a un estudiante."""

    def __init__(self, nombre, edad, carrera):
        """Inicializa un nuevo estudiante."""

        super().__init__(nombre, edad)
        self.carrera = carrera

    def saludar(self):
        """Saluda al estudiante por su nombre y carrera."""

        print(f"Hola, me llamo {self.nombre} y estudio {self.carrera}")

una_persona = Persona("Diógenes", 22)
un_estudiante = Estudiante("Pericles", 20, "Contador Público")

una_persona.saludar()
un_estudiante.saludar()
#El polimorfismo ocurre cuando se llama al metodo saludar() de cada objeto,
# y cada uno responde de manera diferente, dependiendo de su clase.

#TIPOS DE ERRORES:
# - Si la clase en cuestión no contara con una clase base se producirá una excepción del tipo TypeError.
# - Si la clase base no tiene definido el método solicitado entonces se producirá una excepción del tipo AttributeError.