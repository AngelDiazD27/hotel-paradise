#DECORADORES
#En python todo es un objeto, por lo que las funciones son objetos de primera clase.
#Esta herramienta permite modificar el comportamiento de una funcion (UDF) sin modificar su codigo fuente, funcionan
# como envoltorios (wrappers).
#>Decorador: Son FUNCIONES que toman otra FUNCION como argumento y retornan una nueva función con funcionalidades adicionales
#>Sintaxis de un decorador: Se utiliza el símbolo @ seguido del nombre del decorador 
#   y se coloca encima de la definición de la función o método que se desea decorar.

def decorador(func):
    print(" [1] Entrando al decorador")

    def nueva_funcion():
        print(" [2] Antes de llamar a la función original")
        func()
        print(" [3] Después de llamar a la función original")

    print(" [4] Saliendo del decorador (la función ya fue decorada)\n")
    return nueva_funcion

@decorador 
def saludar():
    print(" [Función original] ¡Hola mundo!")

print("\n [5] Ahora vamos a llamar a la función decorada:\n")
saludar()
#Lo que pasara despues es mostrar el print 1 y 4, luego mostrara el print 5 y finalizara con el 2, Funcion og y 3

