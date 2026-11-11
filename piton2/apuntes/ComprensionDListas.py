#La comprension de listas basicamente es un for abreviado
#Forma normie de manejo de una lista
valores =[1, 2, 3, 4]
posicion = 0

resultado = []

while posicion < len(valores):
    resultado.append(valores[posicion] * 3)
    posicioon = posicion + 1

print (resultado) #Esta version es normal si sabes programar pero no esta chida si sabes python

#Forma que ya le sabe
valores =[1, 2, 3, 4]
resultado = []

for valor in valores:
     resultado.append(valor * 3)

print(resultado)

#Forma que le gusta a SalaGod
valores = [1, 2, 3, 4]
resultado = [valor *3 for valor in valores]
