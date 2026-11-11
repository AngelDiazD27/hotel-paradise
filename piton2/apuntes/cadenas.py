"---Cadenas---"
#Las cadenas son secuencias de variables inmutables, osea que son inmodificables. Cuando realizamos una operacion de
# concatencacion o de repeticion de dos valores, se esta creando un nuevo valor. Ejemplo:
cadena1 = "oda"
cadena2 = "adios"
#Para mostrar como son diferentes los valores, se muestra el id de cada variable
print(id(cadena1))
print(id(cadena2))
cadena3 = cadena1 + cadena2 #Concatencacion, aqui el id se mostrara diferente a los dos anteriores porque es un nuevo valor
print(id(cadena3))

"---cadenas f---"
#Las cadenas f son cadenas que permiten insertar variables dentro de la cadena, para ello se utiliza la letra f antes