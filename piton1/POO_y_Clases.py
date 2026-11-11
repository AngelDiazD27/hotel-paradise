#POO (Programacion orientada a objetos)
#Su proposito es una modulizacion clara del software y es una manera de almacenar datos y operaciones
#  que se pueden realizar con ellos juntos, en una entidad llamada objeto. Cada objeto es una instancia de una clase.
#  CADA INSTANCIA ES UN OBJETO DE UNA CLASE. Esta se ve como un protototipo que define las propiedades (atributos) y comportamientos (metodos)

# >Principios fundamentales:
# 1- Encapsulamiento: Oculta detalles del objeto y solo muestra las opciones seguras al mundo exterior.
# 2- Abstraccion: Permite concentrarse en lo que hace el objeto sin tener que lidiar con el como se hace, hay interfaces
#    simples para interactuar con el objeto, haciendo mas simple al sistema.
# 3- Herencia: Puede crear nuevas clases basadas en clase que ya existan, reutiliza el codigo y crea una jerarquia de clases organizada
# 4- Polimorfismo: Hace que un objeto de diferentes clase trabaje como instancia de una clase comun, atraves de la herencia.

("-----Clases-----")
#Las clases son como un plano para crear un objeto. Define un conjunto de atributos (variables) y metodos (funciones)
#  que caracterizan a cualquier objeto del tipo de esa clase.
"""Ejemplo de creacion de clase:"""
class Libro: 
    """pos un libro equisde"""
    def __init__ (self, titulo, autor, isbn, fecha_publi):  #self es una instancia de la clase Libro,
        # self es una referencia al objeto actual, permite acceder a los atributos y metodos de la clase
        """El metodo init sirve para ejecutar un nuevo objeto de la clase Libro. Recibe como argumentos los valores
        de los atributos del objeto y recibe como titulo de metodo constructor de la clase"""
        self.titulo = titulo #Esto es un atributo de la clase
        self.autor = autor
        self.isbn = isbn
        self.fecha_publi= fecha_publi
    def __str__(self):
        """El metodo str devuelve una representacion en cadna del objeto"""
        return f"Libro: {self.titulo}, Autor: {self.autor}"     
    
("-----Instancia-----")    
# En esta parte solo implica crear un objeto unico a partir de una clase. Al crear la instancia se encapsula los atributos (variables)
#  y metodos (funciones) que ya estaban en la clase
"""Ejem de instancia"""
ejemplar = Libro("El Principito", "Antoine de Sanit-Exupery", "378-84-206-5672-2", "1943")
#En la linea de arriba, la variable ejemplar es una instancia osea un objeto de la clase libro
print(ejemplar)
#Se va imprimir la cadena que se creo en la linea 29
