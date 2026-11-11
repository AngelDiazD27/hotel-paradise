import math
Radio = float(input("Dame el radio del círculo: ")) 

def area_circulo(Radio): 
    Area = math.pi * (Radio ** 2)
    return Area
print(f"Area del circulo: {area_circulo(Radio):.4} cm²") 
