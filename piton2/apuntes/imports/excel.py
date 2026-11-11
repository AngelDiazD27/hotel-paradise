#openpyxl es una libreria la cual se trabaja para manipular archivos de excel
import openpyxl #importamos la libreria openpyxl

libro = openpyxl.load_workbook("ejemplo.xlsx") #cargamos el archivo de excel
hoja = libro.active #seleccionamos la hoja activa del archivo
hoja.title = "Mi hoja de excel" #cambiamos el titulo de la hoja activa

#para crear una nueva hoja se usa el metodo create_sheet
nueva_hoja = libro.create_sheet("Nueva Hoja") 

#para escribir datos en una celda se usa la siguiente sintaxis
hoja["A1"] = "Hola Mundo" #la frase se escribira en la celda A1
#el .value tambien se puede usar para escribir datos en una celda
hoja["B1"].value = 12345 #el numero se escribira en la celda B1
