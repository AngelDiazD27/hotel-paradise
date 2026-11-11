import pandas as pd
#crear una serie de pandas
serie = pd.Series([10,20,30,40])
print(serie)

#si quiero tener datos  iguales
igual = pd.Series(1, range(4))
print(igual) #aqui se imprimira el "1" cuatro veces

#crear una serie con indices personalizados
#primera forma es con listas. Cada lista sera una columna
una_serie = pd.Series(["ola", "ke", "ase", "?"] , ["a","b","c","d"])
print(una_serie)#Aqui abcd son los indices de la serie
#segunda forma es con diccionarios
otra_serie = pd.Series({1:"uno", 2:"dos", 3:"tres"})
print(otra_serie) #Aqui 1,2,3 son los indices de la serie

#tupla a series
tupla = (10, 15, 20, 25)

tupla_df = pd.Series(tupla)
print(tupla_df) #aqui la tupla ya se convierte en una serie

#en caso de querer agregarle un indice a la serie
tupla = pd.Series(tupla)
indice = 'a', 'b', 'c', 'd'
tupla.index = indice
print(tupla) #aqui la tupla tiene indices a,b,c,d

'----Dataframes----'
#un dataframe de pansas es una coleccion de diversas series
diccionario_datos = {"Peso":[87, 80, 80 , 50, 100],
                     "Estatura":[171, 140, 170, 163, 180]}
#Las llaves del diccionario seran los nombres que llevaran las columnas, como un encabezado

datos_df = pd.DataFrame(diccionario_datos)
print(datos_df)
#sin embargo 