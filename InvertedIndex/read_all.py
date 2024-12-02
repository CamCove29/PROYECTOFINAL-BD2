
archivo_csv = r"C:\Users\Camila\Desktop\styles\styles.csv"

with open(archivo_csv, 'r') as archivo:
    encabezados = archivo.readline().strip().split(',')
    print('Encabezados del CSV:', encabezados)
    i = 0
    for linea in archivo:
        valores = linea.strip().split(',')
        print('Valores procesados:', valores)
        i+=1
        if i==4: #lineas procesadas
            break;
