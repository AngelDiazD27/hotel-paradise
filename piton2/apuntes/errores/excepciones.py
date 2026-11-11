#Todo error es una excepcion, las excepciones pueden ser anticipadas por los programadores para evitar errores.
#LBYL: Look Before You Leap             EAFP: Easier Ask Forguiness then Permision

dato_str = input("Indica tu edad actual, introduce solamente numeros: ")
if dato_str.isdigit():  #look
    'La linea de arriba el .isdigit hace que se pueda evitar que truene ya que el isdigit hace que cualquier '
    'string que entre salga como int'
    edad = int(dato_str) #leap
    print(f"El doble de tu edad es igual a {edad * 2}")

else: 
    print("Lo siento, tu respuesta no cumple con contener solamente numeros")


#Uso de try except /////
#el enfoque de try es que se separa 
#El except solo se ejecuta si hay problemas, si ademas del except yo tuviera un else
#el else se ejecuta si solo si el codigo protegido (try) se ejecuto sin errores.
#Finally: Codigo o bloque es algo que quieres que se ejecute siempre haya o no haya excepciones