#UDF: User Defined Function
#Una función recibe datos a través de los argumentos que se le pueden definir y puede retornar un valor resultante de su proceso al código que la invoca; 
# por lo que para efectos introductorios, podemos categorizar las funciones de acuerdo a sus argumentos y valor de retorno:

#1.Funcion que no requiere argumentos y no retorna valor alguno
def pasa_cinco_renglones(): #Esta funcion solo pasa cinco renglones hacia abajo
  """Este método solamente pasa cinco renglones hacia abajo en la consola"""

  print()
  print()
  print()
  print()
  print()

print("Hola")
pasa_cinco_renglones()
print("A todos")
pasa_cinco_renglones()
print("Dije, a todos")
print("\n**********\n")
"""Esta funcion no recibe argumentos, osea no requiere de parametros externos y 
 no retorna ningun valor porque solo muestra un mensaje"""

#2.Funcion que requiere argumentos y no retorna valor alguno
def despliega_titulo(mensaje):
  """Método que enmarca un título, el cual se le proporcionará como un argumento de tipo str"""

  largo = len(mensaje)
  print("*" * (largo + 6))
  print(f"** {mensaje} **")
  print("*" * (largo + 6))

despliega_titulo("Menú principal")
print("\n**********\n")
"""Esta funcion recibe un argumento tipo str, que es el mensaje que pasa como parametro y no retorna ningun valor 
   porque solo muestra un msj"""

#3.Funcion que recibe argumentos y retorna un valor
def suma_dos_numeros(numero1, numero2):
  """Método que regresa la suma aritmética de dos números proporcionado cada uno mediante parámetros separados """

  suma = numero1 + numero2
  return suma

dato1 = int(input("Dime un número: "))
dato2 = int(input("Dime un número: "))

print(f"El resultado de sumar {dato1} y {dato2} es igual a {suma_dos_numeros(dato1, dato2)}")
print("\n**********\n")
"""Esta funcion recibe argumentos int que son los numeros a sumar y retorna el resultado de la suma."""

#4.Funcion que manejan argumentos opcionales
def nombre(primer_nombre, primer_apellido, segundo_apellido = "N/A"):
    """Método que despliega el nombre completo de la persona indicada """

    print(f"Primer Nombre: {primer_nombre}")
    print(f"Primer Apellido: {primer_apellido}")
    print(f"Segundo Apellido: {segundo_apellido}\n")

nombre("Domitila", "Ronaldo", "De la Roca") #Aqui se pasan los tres argumentos
print()
nombre("Crisóforo", "Smith")#Aqui solo se pasan los dos primeros, el tercero es opcional.
print("\n**********\n")

#5.Funcion que maneja una cantidad variable de argumentos
def suma_numeros(*numeros):
    """Suma cualquier cantidad de números que se pasen como argumentos."""
    suma = 0
    for numero in numeros:
        suma += numero
    return suma

# Llamadas con diferentes cantidades de argumentos
print(suma_numeros(3, 5))
print(suma_numeros(10, 20, 30, 40))
print(suma_numeros(1, 2, 3, 4, 5, 6, 7))
