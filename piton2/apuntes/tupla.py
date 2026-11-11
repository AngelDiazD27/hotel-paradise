#Las tuplas son como las listas con la diferencia que no puede modificarse, lo que define las tuplas son las comas ','
datos = ("a", "b", "c")
datosiguales = "a", "b", "c"
print(type(datos))
print(type(datosiguales))
#ambos son tuplas, los parentesis no importan, solo se usan cpor educacion:P

'unpacking'
#Una forma mas extensiva y normal (noob)
datos = (10, 20, 30, 40)
a = datos[0]
b = datos[1]
c = datos[2]
d = datos[3]

print(f"{a}, {b}, {c}, {d}")

#Forma god gigachad

datos = (10, 20, 30, 40)

a, b, c, d = datos
print(f"{a}, {b}, {c}, {d} ")

#forma valida del metodo unpacking
datos = (10, 20, 30, 40, 50)

a, b, *c = datos

print(f"{a}, {b}, {c}") #Aqui lo que hace el asterisco es que en la variable 'c' se almacenan en uan lista los ultimos elementos
#todo depende de donde agregas el asterisco.

datos = (10, 20, 30, 40, 50)

*a, b, c = datos

print(f"{a}, {b}, {c}") #Aqui ahora se va almacenar el 10,20,30 en a, por que al ser b y c no tener un asterisco, agarraran
# sus respectivos elementos, osease, que 40 estara en b y 50 en c.

#llamar a un elemento
datos = [1] #aparecera el 20 porque estas llamando a esa posocion.
