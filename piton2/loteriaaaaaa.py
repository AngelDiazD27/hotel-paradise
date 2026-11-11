import random
BarajaLote = ["El Gallo", "El Diablo", "La Dama", "El Catrín", "El Paraguas", "La Sirena", "La Escalera", "La Botella", 
              "El Barril", "El Árbol", "El Melón", "El Valiente", "El Gorrito", "La Muerte", "La Pera", "La Bandera", 
              "El Bandolón", "El Violoncello", "La Garza", "El Pájaro", "La Mano", "La Bota", "La Luna", "El Cotorro", 
              "El Borracho", "El Negrito", "El Corazón", "La Sandía", "El Tambor", "El Camarón", "Las Jaras", "El Músico", 
              "La Araña", "El Soldado", "La Estrella", "El Cazo", "El Mundo", "El Apache", "El Nopal", "El Alacrán", 
              "La Rosa", "La Calavera", "La Campana", "El Cantarito", "El Venado", "El Sol", "La Corona", "La Chalupa", 
              "El Pino", "El Pescado", "La Palma", "La Maceta", "El Arpa", "La Rana" ]

print (" Corre y se va corriendo ")

random.shuffle(BarajaLote)

for carta in BarajaLote:
    print(f"\n La carta es {carta}")
    if input ("Sigo? (S/N): ") in "Ss": #tmb se puede utilizar .upper
        print("seacaba")
else:
    print("\n**** Yanohaycartas") 
           


".choice es para elejir al azar pero se puede repetir"
".el shuffle es para elejir al azar pero no se repite"
