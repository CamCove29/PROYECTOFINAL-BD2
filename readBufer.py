import csv
import itertools

lineas_por_pagina = 100

# Abre el archivo CSV en modo lectura
with open(r"C:\Users\Camila\Desktop\styles\styles.csv", 'r') as archivo_csv:
    # Lee 4096 bytes desde el archivo
    datos = archivo_csv.read(4096)
    # Imprime los datos leídos
    print(datos)