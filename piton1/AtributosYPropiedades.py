("-----Atributos-----")
# Estas estan disponibles para todos los objetos existentes y se crean a partir de una clase.
#un atributo es una variable que pertenece a un objeto, y se define dentro de la clase. 
# Es lo que va despues de self en el metodo __init__.

"""Ejemplo de atributo"""
class Persona:
    """Atributo que define el nombre de la persona"""
    nombre = "Mel"
    
    """Atributo que define la edad de la persona"""
    edad = 20 
una_people = Persona() #Este es un objeto (variable) de la clase persona
print(una_people.nombre) #Acceso al atributo nombre de la clase Persona

print(una_people) #Imprime la referencia de memoria del objeto, no el nombre de la persona

otra_people = Persona()
print(otra_people.nombre) 
"""El recurso nombre, se puede a volver a usar si yo me refiero a Mel como otra persona"""   

("-----Propiedades-----")
#Es un metodo especial que se comporta como un atributo.
#Son mecanismos mas avanzados que controlan el acceso del atributo que esta en la clase, difenen metodos q se ejecutan automaticamente
# El decorador @Property en python se utiliza para definir una propiedad, cuando se tiene el valor de la propiedad, se ejecuta un metodo getter.
#Cuando se modifica el valor, se ejecuta el setter.
#   Este decorador crea un descriptor, es un objeto que se utiliza para apoderarse del acceso a un atributo. Cuando se tiene el valor
#   del atributo, en este caso, en el ejemplo de arriba, "nombre", el descriptor busca el metodo getter y este devuelve el valor del atributo nombre
#Su proposito es encapsular.

#>Metodos basicos de propiedades:
# - Getter: Permite obtener (lee) el valor de un atributo. 
# - Setter: Permite modificar (escribe) el valor de un atributo.

#Un punto clave a recordar es que en python se puede utilizar el guion bajo (_) como prefijo para un nombre de atributo para mostra que no debe ser cambiado
# directamente desde fuera de la clase, esto también se demuestra en el ejemplo siguiente.
class PersonaConPropiedad:
    def __init__(self, nombre):
        self._nombre = nombre  # Atributo privado con guion bajo, osea que no debe ser accedido directamente desde fuera de la clase
    
    @property
    def nombre(self):
        """Getter para obtener el nombre"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Setter para modificar el nombre"""
        if isinstance(nuevo_nombre, str) and nuevo_nombre: #(isinstance verifica si el nuevo_nombre es una cadena)
            self._nombre = nuevo_nombre
        else:
            raise ValueError("El nombre debe ser una cadena no vacía")

"Resumen:"
# - Atributos: Son variables que pertenecen a un objeto y se definen dentro de la clase.
# - Propiedades: Son mecanismos que controlan el acceso a los atributos, utilizando decoradores como @property para definir getters y setters.
# - Encapsulamiento: Se logra utilizando atributos privados (con guion bajo) y propiedades para controlar el acceso a esos atributos.
# - Todos los properties son atributos, pero no todos los atributos son propiedades. Porque las propiedades solo sirven para encapsular
#   y controlar el acceso a los atributos, mientras que los atributos son simplemente variables que pertenecen a un objeto.
# - Todos los properties pasan por un getter pero no siempre por un setter, ya que el setter es opcional 
#   y solo se utiliza si se desea modificar el valor del atributo.
