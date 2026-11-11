import random
#modulo que nos permite generar numeros aleatorios
print(random.random())#Genera un numero aleatorio entre 0 y 1
print(random.randint(1,15))#Genera un numero aleatorio entre 1 y 15
print(random.randrange(1,15,2))#Genera un numero aleatorio entre 1 y 15 pero solo los numeros impares, 
#                               porque el 3er parametro es el paso (2 en este caso)
"-Metodo choice y shuffle-"
#choice: selecciona un elemento aleatorio de una secuencia (lista, tupla, cadena)
colores = ["rojo", "verde", "azul", "amarillo"] 
print(random.choice(colores))#Aqui se selecciona un color aleatorio de la lista anterior
#shuffle: lo que hace el shuffle es mezclar los elementos de una secuencia (lista, tupla, cadena)
random.shuffle(colores)
print(colores)#Aqui se mezclan los colores de la lista anterior