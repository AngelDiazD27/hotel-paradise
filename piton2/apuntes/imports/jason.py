#json o JavaScript Object Notation es un formato de intercambio de datos ligero y fácil de leer y escribir para los humanos y fácil de analizar y generar para las máquinas.
import json

#IMPORTANTE: Las {} indica objetos y las [] indican arrays o arreglos

lista = [[1, "a"],
         [2, "b"],
         [3, "c"]]
with open("piton2/apuntes/imports/archivo.json", "w") as archivo:
    json.dump(lista, archivo)  #convierte la lista en formato json y la guarda en el archivo