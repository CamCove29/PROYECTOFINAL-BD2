import json

ruta_indices = r"C:\Users\Camila\Desktop\PROYECTOFINAL-BD2\InvertedIndex\Local_Index"

def write_json(nombre_archivo:str, index:dict)->None: #funcion para escribir un diccionario en un archivo json
    try:
        with open(ruta_indices+ "\\" + nombre_archivo,'w') as archivo:
            json.dump(index,archivo)
    except FileNotFoundError:
        return {}

def write_index(nro_index:int, index:dict, ruta:str="")->None:
    nro_index_str:str = str(nro_index) #convierte el nro de index a string

    if nro_index<10: #caso en el que se debe añadir un cero al inicio
        nro_index_str = "0"+nro_index_str
    print("nro_index:",nro_index_str)
    write_json(ruta+"index"+nro_index_str+".json", index) #escribimos el diccionario en un archivo json

write_index(20,{"hola":"mundo"}) #prueba
