import time

tamaño_maximo_buffer = 4096
cont = 0

ruta_archivo = r"C:\Users\Camila\Desktop\styles\styles.csv"

with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    while True:
        buffer = []
        tamaño_buffer = 0

        for linea in archivo:
            tamaño_linea = len(linea.encode("utf-8"))
            if tamaño_buffer + tamaño_linea <= tamaño_maximo_buffer:
                buffer.append(linea.strip())
                tamaño_buffer += tamaño_linea
            else:
                break

        print("Nuevo buffer:\n\n", "\n".join(buffer))
        print("Tamaño buffer: ", tamaño_buffer)


        time.sleep(3)
        cont += 1
        if not buffer:
            break
    print("Listo")
    print(cont)
