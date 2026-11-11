import datetime
import time

fecha_nacimiento = input("Dime tu fecha de nacimiento  (dd/mm/aaaa): ")
fecha_procesada = datetime.datetime.strptime(fecha_nacimiento, "%d/%m/%Y").date() #Aqui expresa en que orden nos lo esta dando
#strftime es para manejar en que orden quiera.


Edad= datetime.datetime.now().year - fecha_procesada.year
print(f"Tienes {Edad} años") 