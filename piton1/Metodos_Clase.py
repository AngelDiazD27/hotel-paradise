#Los metodos de clase son acciones que un objeto puede realizar. Se definen dentro de la clase pero se pueden invocar fuera de esta.
# Como las funciones que defines dentro de una clase, pero con la diferencia que van a un objeto en especifico
"""Ejemplo de metodos de clase."""
class Persona: 
    def __init__(self, nombre, edad): #__init__ se utiliza para inicializar objetos cuando se crea una nueva instancia de una clase.
        self.nombre = nombre
        self.edad = edad
        """"""
    def saludar(self):
        print(f"Hola, me llamo {self.nombre} y tengo {self.edad} años de edad.")

    def cumplir_años(self):
        self.edad += 1

persona = Persona("Euduviges", 25)

persona.saludar()         
#Aqui los metodos de la clase persona son def saludar y cumplir_años, que son acciones que el objeto persona puede realizar.
#Aqui para que ambas def sean consideradas metodos de clase, se deben definir dentro de la clase Persona. Y realizar acciones 
# que el objeto persona puede realizar y usan self para saber qué objeto los está ejecutando

