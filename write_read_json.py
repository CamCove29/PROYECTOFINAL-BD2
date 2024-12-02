import json

conjunto_de_diccionarios = [
    {"nombre": "Ejemplo1", "edad": 30},
    {"nombre": "Ejemplo2", "edad": 35},
    {"nombre": "Ejemplo3", "edad": 40}
]

with open("conjunto_de_diccionarios.json", "w") as archivo:
    json.dump(conjunto_de_diccionarios, archivo)


with open("conjunto_de_diccionarios.json", "r") as archivo:
    conjunto_leido = json.load(archivo)

print(conjunto_leido)
