import linecache

numero_de_linea = 10  # línea que se quiere leer

archivo_csv = r"C:\Users\Camila\Desktop\styles\styles.csv"

linea_especifica = linecache.getline(archivo_csv, numero_de_linea)

print(f'Línea {numero_de_linea}: {linea_especifica}')
