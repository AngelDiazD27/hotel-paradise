("-----Herencias-----")
#Mecanismo que hace que una clase herede atributos y metodos de otra clase ya existente,
#  permitiendo reutilizar el codigo y crear una jerarquia de clases organizada.
# *Las clases que heredan de otra clase se llaman subclases o clases derivadas.*
# *La clase de la que se hereda se llama superclase o clase base.*
"ejemplo de herencia"
class Persona: #Clase base o superclase
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        """Despliega un saludo presentando los datos de nombre y edad de la
        persona representada por la instancia"""
        print(f"Hola, me llamo {self.nombre} y tengo {self.edad} años de edad.")

class Estudiante(Persona): #Clase derivada o subclase
    #La clase Estudiante usa como base (superclase) a la clase Persona (lo usa como parametro)
    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self.carrera = carrera
    def estudiar(self):
        """Despliega un saludo presentando los datos de nombre y carrera que
        está estudiando la persona representada por la instancia"""
        print(f"{self.nombre} está estudiando {self.carrera}")
un_estudiante = Estudiante("Demóstenes", 25, "Licenciado en tecnologías de información")
un_estudiante.saludar() #Método de la clase base
un_estudiante.estudiar() #Método de la clase derivada