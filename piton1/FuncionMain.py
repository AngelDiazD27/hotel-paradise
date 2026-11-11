#La funcion main es como un menu que permite al usuario elegir que funcion quiere ejecutar
#Codificamos todas las otras UDFs requeridas
def foo():#ejemplo de UDF, no hace nada solo es un ejemplo
    pass

#Codificamos la función main() 
def main():
    """Aquí iremos colocando el código principal que irá invocando
    a las otras UDFs previamente definicas"""
    ...

"""Si se está ejecutando de manera directa el programa se activará
el siguiente código que invoca a la función main()

Por el contrario, si el código se está ejecutando como consecuencia
de haberse importado entonces no se invocará a la función main()"""

if __name__ == "__main__":
    main()