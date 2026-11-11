print("----- Diccionarios -----")
#Estructura de datos que almacena pares clave:valor, se puede acceder a los valores mediante las claves y se definen con llaves {}
#La clave debe ser unica (no se repite) y puede ser cualquier tipo de dato inmutable (numeros, cadenas y tuplas)
#Los valores pueden ser de cualquier tipo de dato, incluso otros diccionarios. Su ventaja es la velocidad de busqueda


#Crear un diccionario
diccionario_vacio1 = {}
diccionario_vacio2 = dict()
"""Si en nuestro diccionario hay varios elementos, lo separamos por comas ejemplo:    """
diccionario1 = {
    'nombre': 'Mel',
    'edad': 70,
    'sexo': 'ya',
}
print(diccionario1)
print ("\n**********\n")

#Agregar elementos al diccionario
"""Se especifica el nombre del diccionario entre corchetes (va el nombre de la llave) 
   el valor de la llave del nuevo elemento y se le realiza la asignación de valor correspondiente"""
print("Agregar un nuevo elemento al diccionario:")
diccionario1['altura'] = 1.80
print(diccionario1) 
print ("\n**********\n")


#IMPORTANTE: En un diccionario, sus elementos no se acceden posicionalmente a comparacion de una tupla.
#Acceder a los valores de un diccionario
"""Considere los siguientes puntos para acceder a los elementos de un diccionario:
-Un diccionario no puede ser accesado posicionalmente.
-El acceso a los elementos se realiza mediante la identificación de la clave cuyo valor se desea recuperar."""
print(diccionario1['nombre'])
"""Si la clave no exite se generara un keyError, para evitarlo se puede usar el metodo get()"""
print(diccionario1.get('equisde')) #Ejemplo si no existe, retornara None
#ejemplo de un keyError
# print(diccionario1['apellido']), esto generara error porque no existe la clave 'apellido'.
print ("\n**********\n")

#Alternativas para acceder al contenido de un diccionario:
#1.Acceder a las llaves del diccionario
"""Aqui se mostrara las claves del diccionario (nombre, edad, sexo, altura)"""
print("Llaves del diccionario:" )
print(diccionario1.keys())
print ("\n**********\n")

#2.Acceder a los valores del diccionario
print("Valores del diccionario:" )
"""Aqui se mostrara los valores del diccionario (Mel, 70, ya y 1.80)"""
print(diccionario1.values())
print ("\n**********\n")

#3.Acceder a los items del diccionario
print("Items del diccionario:" )
"""Aqui se mostrara los pares clave:valor del diccionario, osea muestra todo el contenido del diccionario,
   se retorna en una lista o tupla dependiendo el caso"""
print(diccionario1.items())
print ("\n**********\n")

#RECORDATORIO:
# -A parte de las listas y diccionarios, estan las tuplas.
#  Son similares a las listas pero son inmutables, no se pueden modificar y se definen con parentesis ()

print("----- Conjuntos o Sets-----")

#Estrutura de datos que almacena un conjunto de elementos no repetidos dentro de llaves {}, estas son como los diccionarios
#   pero no tienen clave:valor, solo almacenan valores.
conjunto1 = {1, 2, 3, 4}
conjunto2 = {4, 5, 6, 7}
print("Conjunto 1: " + str(conjunto1))
print("Conjunto 2: " + str(conjunto2))
print ("\n**********\n")

"""Los conjuntos son estructuras muy útiles mediante las cuales podemos aplicar las operaciones 
    clásicas de lógica de conjuntos, tales como:        """

"""-Union: Combina dos conjuntos, eliminando los elementos repetidos. """
print(conjunto1.union(conjunto2)) #manera 1
print(conjunto1 | conjunto2) #manera 2, con el operador pipe
print ("\n**********\n")

"""-Interseccion: Retorna los elementos que se encuentran en ambos conjuntos. """
print(conjunto1.intersection(conjunto2)) #manera 1
print(conjunto1 & conjunto2) #manera 2, con el operador ampersand
print ("\n**********\n")

"""-Diferencia: Retorna los elementos que se encuentran en el primer conjunto pero no en el segundo."""
print(conjunto1.difference(conjunto2)) #manera 1
print(conjunto1 - conjunto2) #manera 2, con el operador menos
print ("\n**********\n")

"""-Diferencia simetrica: Retorna los elementos que se encuentran en uno de los conjuntos pero no en ambos """
print(conjunto1.symmetric_difference(conjunto2)) #manera 1
print(conjunto1 ^ conjunto2) #manera 2, con el operador circumflejo
print ("\n**********\n")

"""-Determinar si un conjunto es un subconjunto de otro: """
print(conjunto1.issubset(conjunto2)) #manera 1, retorna True si conjunto1 es un subconjunto de conjunto2
print(conjunto1 <= conjunto2) #manera 2, con el operador menor o igual que 
