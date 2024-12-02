import json
import time
import os  # Para verificar la existencia del archivo

# Ruta al archivo CSV
archivo_csv = r"C:\Users\Camila\Desktop\styles\styles.csv"

# Nombre del archivo JSON con las posiciones en bytes
archivo_json = "normas.json"

# Verifica si el archivo JSON existe y contiene contenido válido
if not os.path.exists(archivo_json) or os.stat(archivo_json).st_size == 0:
    print(f"El archivo {archivo_json} no existe o está vacío. Creándolo...")
    # Contenido predeterminado para el archivo JSON
    contenido_predeterminado = [0, 98, 191, 284]  # Ejemplo: posiciones en bytes
    with open(archivo_json, "w") as archivo:
        json.dump(contenido_predeterminado, archivo)
    print(f"Archivo {archivo_json} creado con contenido: {contenido_predeterminado}")
else:
    # Si existe, verifica si el contenido es válido
    try:
        with open(archivo_json, "r") as archivo:
            json.load(archivo)  # Intenta cargar el JSON
    except json.JSONDecodeError:
        print(f"El archivo {archivo_json} contiene datos inválidos. Restableciéndolo...")
        contenido_predeterminado = [0, 98, 191, 284]
        with open(archivo_json, "w") as archivo:
            json.dump(contenido_predeterminado, archivo)
        print(f"Archivo {archivo_json} restablecido con contenido: {contenido_predeterminado}")


# Definición de la función `get_row`
def get_row(posicion_bytes):
    """
    Esta función lee una línea del archivo CSV a partir de una posición específica en bytes.
    """
    # Abre el archivo en modo binario (lectura)
    with open(archivo_csv, 'rb') as archivo:
        print(f"Abrimos el archivo {archivo_csv}")

        # Posiciona el puntero en el byte especificado
        archivo.seek(int(posicion_bytes))
        print(f"Nos movemos al byte {posicion_bytes}")

        # Lee la línea completa desde esa posición
        linea_especifica = archivo.readline()
        print(f"Leemos la línea (binario): {linea_especifica}")

        # Convierte los bytes a texto usando la codificación UTF-8
        linea_especifica = linea_especifica.decode('utf-8')
        print(f"Decodificamos a texto: {linea_especifica.strip()}")

        # Devuelve la línea decodificada
        return linea_especifica


# Abre el archivo JSON que contiene las posiciones en bytes
with open(archivo_json, "r") as archivo:
    print("Abriendo el archivo normas.json...")
    # Carga el archivo JSON en un diccionario de Python
    diccionario_normas = json.load(archivo)
    print(f"Contenido del archivo JSON: {diccionario_normas}")

# Abre el archivo CSV en modo binario para leer líneas basadas en las posiciones del JSON
with open(archivo_csv, 'rb') as archivo_csv:
    print(f"Abriendo el archivo CSV {archivo_csv.name} para leer posiciones...")
    i = 0  # Contador para las filas procesadas
    for pos_fila in diccionario_normas:  # Itera sobre las posiciones especificadas en el JSON
        # Mueve el puntero a la posición especificada en el archivo
        archivo_csv.seek(int(pos_fila))
        print(f"Posición actual del puntero: {archivo_csv.tell()}")

        # Lee y decodifica la línea en esa posición
        linea = archivo_csv.readline().decode('utf-8').strip()
        print(f"Línea leída desde posición {pos_fila}: {linea}")

        i += 1  # Incrementa el contador
        if i == 20:  # Pausa cada 20 líneas procesadas
            print("Pausa después de 20 líneas...")
            time.sleep(3)  # Espera 3 segundos
            i = 0  # Reinicia el contador
