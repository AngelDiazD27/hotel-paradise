"---modulo math---"
import math
#modulo para operaciones matematicas sin la necesidad de definir funciones
"==Funciones basicas=="
num_flotante = float(input("Dime un numero flotante: "))
print(f"Su valor sin redondear es: {math.floor(num_flotante)}")#Redondea hacia abajo
print(f"Su valor redondeado hacia arriba es: {math.ceil(num_flotante)}")#Redondea hacia arriba
print(f"Su valor redondeado es: {round(num_flotante)}")#Redondea al entero mas cercano

