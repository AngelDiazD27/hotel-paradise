#LISTAS
"""Estas se determinan por corchetes []
-Las listas son estructuras de datos que permiten almacenar varios elementos en una sola variable, 
 son mutables osea que se pueden modificar, agregar o eliminar elementos una vez creadas
  estas pueden contener cualqueir tipo de dato y se pueden repetir los valores."""

#maneras de crear una lista:
Lista1 = []
Lista2 = list()

Lista2 = ["x", "y", "z"]
#para acceder a los datos de una lista se usa el indice, que empieza en 0
Lista3 = [0, "a", 2.5, True, False, "ola", "6.3" ]

#Maneras de mostrar una lista:
print(Lista3)
print("\n**********\n")
print(Lista3[:])
print("\n**********\n")

#Acceder a los datos de una lista
print(Lista3[0]) #Va a acceder al elemento 0 de la lista, que es 0
print("\n**********\n")

#Slices: Son partes de la lista que se pueden acceder de dato a dato

Sublista = Lista3[1:4] #Accede a del elemento 1 al 3, lo que va despues de los dos puntos no se incluye
print (Sublista) 
print("\n**********\n")

print(Lista3[0:4]) #Accede del elemento 0 al 3, el 4 no se incluye
print("\n**********\n")

print(Lista3[:4])#Accede del elemento 0 al 3, como en la linea 31
print("\n**********\n")

print(Lista3[2:])#Mostrara la posicion 2 hasta el final de la lista
print("\n**********\n")

print(Lista3[::2])#Mostrara la lista pero saltando de 2 en 2, osea la posicion 0, 2, 4, etc
print("\n**********\n")

print(Lista3[::-1])#Mostrara la lista al reves, emepezando por el final
print("\n**********\n")

print(Lista3[-1:]) #Accede al ultimo elemento de la lista, el -1 indica el ultimo elemento

#Agregar elementos a una lista
Lista3.append("New") #Se usa el .append para agregar un elemento y aparecera al final de la lista
print("\n///////\n")

#Modificar un elemento de la lista, suplanta el elemento en la posicion indicada
Lista3[0] = "Modificado"
print(Lista3)
#Aqui se suplanto el 0 con la palabra "Modificado"
print("\n**********\n")

#otra manera de modificar un elemento es con el .insert
Lista3.insert(1, "Insertado") #Esto inserta el elemento en la posicion 1, desplazando los demas elementos, el insert no suplanta solo agrega
print(Lista3)
print("\n///////\n")

#Eliminar un elemnto de la lista
#Forma 1: Usando el .remove() para eliminar un elemento en especifico
Lista3.remove("a")
print(Lista3)
print("\n**********\n")
#Forma 2 del, aqui se elimina el elemento en la posicion indicada, se va a eliminar el primer elemento de la lista
del Lista3[0]
#Se elimina el primer elemento de la lista que es "Modificado"
print(Lista3)

print("\n///////\n")
#Combinar listas, no se puede usar el .append, se usa el metodo .extend()
Lista3.extend(Lista2) #Esto agrega los elementos de la Lista2 a la Lista3
print(Lista3)
print("\n**********\n")

#Otro metodo es el operador +
Lista4 = Lista3 + Lista2 
#Crea una lista nueva con los elemento de ambas listas, al imprimirla se vera igual que con el .append

#Al momento de crear una lista, cuanto tu creas una variable que almacena una lista ya creada, eso no copia la lista.
#por decir:
origen = [1, 2, 3, 4, 5]

destino = origen
'aqui solo se esta almacenando "origen" en la variable destino, no la copia.'
origen.append(1_000)
#Si invocas "destino" se generara la lista "origen"
print(id(origen))
print(id(destino)) #Su id es la misma

#Copias de listas 
#Forma 1:
ListaOg = (1, 2, 3)

ListaCopia = ListaOg.copy()
print(id(ListaOg))
print(id(ListaCopia))#Aqui su id es distinto por lo que da a entender que ya son diferentes

#Forma 2:
ListaCopia = list(ListaOg)

#Forma 3: (Forma que le guta al prof)
ListaCopia = ListaOg[:] #Slicing


#metodo max
mis_datos = []
print(max(mis_datos, default=8)) #el default es para tener un elemento base
