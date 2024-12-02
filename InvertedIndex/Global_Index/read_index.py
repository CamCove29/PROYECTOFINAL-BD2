import json
import os
import io

# Constantes
TAMAÑO_MAXIMO_BUFFER = io.DEFAULT_BUFFER_SIZE
RUTA_INDICES = r"C:\Users\Camila\Desktop\PROYECTOFINAL-BD2\InvertedIndex\Local_Index"


# Funciones
def read_json(nombre_archivo: str) -> dict:
    """Lee un archivo JSON y devuelve su contenido como diccionario."""
    try:
        with open(os.path.join(RUTA_INDICES, nombre_archivo), 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {nombre_archivo}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON en {nombre_archivo}: {e}")
        return {}


def read_index(nro_index: int, ruta: str = "") -> dict:
    """Lee un archivo de índice dado su número y una ruta opcional."""
    nro_index_str = f"{nro_index:02}"  # Formatea con ceros iniciales si es menor a 10
    nombre_archivo = os.path.join(ruta, f"index{nro_index_str}.json")
    return read_json(nombre_archivo)


# Ejecución principal
if __name__ == "__main__":
    # Prueba de lectura de un índice específico
    print(json.dumps(read_index(2, "Initial"), indent=4))

    # Calcula el tamaño de los índices del 1 al 14 en la carpeta Merge8
    for i in range(1, 15):
        indice_data = json.dumps(read_index(i, "Merge8\\")).encode('utf-8')
        print(f"Índice {i} -> {len(indice_data)} bytes")

    # Calcula el tamaño del índice 16 sin ruta adicional
    indice_16_data = json.dumps(read_index(16)).encode('utf-8')
    print(f"Tamaño índice 16: {len(indice_16_data)} bytes")

    # Casos de prueba adicionales
    print("Índice 1:", json.dumps(read_index(1), indent=4))
    print("Índice 2:", json.dumps(read_index(2), indent=4))
