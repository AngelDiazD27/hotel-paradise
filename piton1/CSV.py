("-----CSV-----")
# Una csv o Comma-Separated Values (Valores Separados por Comas) es un formato de archivo que se utiliza para
# almacenar datos tabulares, como hojas de calculo o bases de datos, en un formato de texto plano.
"Pasos para crear archivos CSV en Python:"
#Paso 1: Realizar los import correspondientes
import csv
#Paso 2: Crear una lista de diccionarios con los datos que se quieren guardar
datos_a_grabar = dict()

mi_auto1 = ("BMW",2005)
mi_auto2 = ("Toyota", 2015)

"""Se crea un diccionario donde la clave es un numero y el valor es una tupla con los datos del auto."""
datos_a_grabar[10] = mi_auto1
datos_a_grabar[20] = mi_auto2

print(datos_a_grabar)

#Paso 3: Abrir el archivo CSV en modo escritura
archivo = open("autos.csv","w", encoding='latin1', newline="") #Se usa el encoding 'latin1' para evitar problemas con caracteres especiales
#el newline="" es para evitar que se agregue una linea en blanco al final del archivo
# La w indica que va a abrir el archivo en modo de escritura, el autos.csv es el nombre del archivo que se va a crear.
#Otra manera de abrir el archivo es usando with, que cierra el archivo automaticamente al finalizar el bloque:
with open("autos.csv", "w", encoding='latin1', newline="") as archivo:

#Paso 4: Establecer una salida de escritura
    grabador = csv.writer(archivo) #Se crea un objeto grabador que se encargara de escribir en el archivo CSV

#Paso 5: Grabar el encabezado (OPCIONAL)
grabador.writerow(("Clave", "marca", "año"))

#Paso 6: Iterar sobre los elementos de los datos a grabar.
for clave, datos in datos_a_grabar.items():
  grabador.writerow((clave, datos[0], datos[1]))


#RESUMEN:
# - Se importa el modulo csv.
# - Se crea un diccionario con los datos a grabar. 
# - Se abre el archivo CSV en modo escritura.
# - Se crea un objeto grabador que se encargara de escribir en el archivo CSV.
# - Se graba el encabezado (opcional).
# - Se itera sobre los elementos del diccionario y se graban en el archivo CSV.
# - Se cierra el archivo automaticamente al finalizar el bloque with.
# - El archivo CSV se crea en el mismo directorio donde se ejecuta el script.
# - Se puede abrir el archivo CSV con cualquier editor de texto o hoja de calculo.
