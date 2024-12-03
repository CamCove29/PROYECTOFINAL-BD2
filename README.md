# PROYECTO 2&3 BD2
## Introducción
### Objetivo del Proyecto
Este proyecto está enfocado en desarrollar un proyecto integral de base de datos que soporte tanto el modelo relacional basado en tablas como técnicas avanzadas de recuperación de información basadas en el contenido de documentos textuales y objetos multimedia. 

![image](https://github.com/user-attachments/assets/625d13fe-e682-4fef-b103-3b6f605f8ca6)
### Descripción del Dataset 
Fashion Products Dataset (https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset/data), es una recopilación estructurada de información sobre productos de moda. Esta información se separa en dos archivos principales .csv:      
styles.csv: Este archivo contiene las columnas id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName. La información de cada producto es representada en una fila:

![image](https://github.com/user-attachments/assets/4d750c32-5c14-4f8e-a1bc-a189f289d081)
images.csv: Este archivo contiene las columnas filename,link, donde filename representa el id de cada imagen y link representa la ubicación de cada imagen.

![image](https://github.com/user-attachments/assets/666c724e-957a-47f4-9892-8f75fbb9df04)
### Importancia de Aplicar Indexación
La indexación es una técnica esencial en sistemas de gestión de datos que permite realizar búsquedas rápidas y eficientes, mejorando la experiencia del usuario y optimizando el uso de recursos en grandes volúmenes de datos.
1. **Índices Invertidos**  
   Los índices invertidos son ideales para buscar términos específicos en grandes colecciones de texto. Este método asocia cada término con una lista de documentos donde aparece, permitiendo una búsqueda rápida sin escanear toda la base de datos. Es fundamental en motores de búsqueda y sistemas de recuperación de texto.
2. **Índices Multidimensionales**  
   Utilizados para datos con múltiples atributos, como coordenadas geográficas o características musicales. Los índices multidimensionales permiten consultas complejas en bases de datos con información de alta dimensionalidad. Estructuras como R-trees y KD-trees son comunes en aplicaciones de geolocalización y análisis de datos espaciales.
## Backend: Índice Invertido - Índice multimedia
Se cargo los vectores y caracteristicas usando registros de longitud fija y variable para no cargar todo el dataset en memoria principal así como los ids de las imagenes se cargaron en memoria secundaria y se encuentran con una busqueda binaria. 
### Construcción del Índice Invertido
El dataset que hemos usado en este proyecto no puede manejarse en memoria RAM, por hemos encontrado como solución escalable que tome en cuenta las consideraciones de hardware: memoria, disco, velocidad. Por temas de facilidad (considerando la longitud variable) manejaremos los diccionarios de la data archivos .json. Nuestra implementación se basa en el algoritmo SPIMI (Single Pass In-Memory Indexing), el cual es utilizado para la construcción eficiente de índices invertidos.

![image](https://github.com/user-attachments/assets/6621c10e-573c-4340-8159-0f8c44ba4fae)
   Nuestra implementación consiste en:

1. Leer el archivo .csv de acuerdo a cantidad de un buffer (considerando que tenga un número exacto de filas, osea no haga la partición de las filas
2. Preprocesar cada fila
3. Concatenar datos de cada fila (calculando la norma y el peso de cada palabra por fila)
![image](https://github.com/user-attachments/assets/7c2afa53-9bbc-44b5-8905-e9b6f67aa959)

   ### Elementos de la fórmula
    - Norma del vector:   ![image](https://github.com/user-attachments/assets/c45e0d10-7bf0-45f6-9d6c-0765d1fdc94d)
    - Suma de 0 al nro de palabras por fila:   ![image](https://github.com/user-attachments/assets/759ba200-7ea8-4826-992d-724c9b39b53b)
    - Cuadrado del peso:   ![image](https://github.com/user-attachments/assets/bbdab00c-d5af-4d0a-917e-918824f1373e)

    Para calcular el valor-peso de una palabra en una fila, consideramos su frecuencia en cada campo y multiplicamos (frecuencia de palabra en el campo * peso del campo).
    
    Basamos nuestro calculo en esta primera fórmula vista en clase:
    
     ![image](https://github.com/user-attachments/assets/893d4d7b-fc84-4f8b-a634-eb05772e55ec)

    Mediante distintos cálculos e interpretaciones llegaremos a esta última fórmula:
    
     ![image](https://github.com/user-attachments/assets/1999ab6f-f764-4ba0-8102-3400e286fc06)

4. Empezar un hash (diccionario) para cada bloque.
    - Este diccionario contendrá `palabra: {pos_fila, peso de palabra para esa fila}`.
    
    ```txt
    {
        "palabra1": {"fila1": peso1, "fila2": peso2, ...},
        "palabra2": {"fila3": peso3, "fila4": peso4, ...},
        ...
    }
    ```

    - **Importante**: Solo se almacenarán las posiciones de las filas en las que la palabra tenga un peso mayor a 0. Si una palabra tiene un peso de 0 en una fila, esa información no se almacenará en el diccionario.

5. Completar el diccionario con todas las palabras preprocesadas del bloque

   - En este paso, se debe agregar cada palabra preprocesada del bloque al diccionario. Para cada palabra, se registran las filas en las que aparece junto con su peso. Este diccionario se va actualizando conforme se procesan más palabras en el bloque.

```txt
  {
  "w1": {"1": 1, "2": 2, "3": 1},
  "w10": {"3": 1, "4": 2},
  "w11": {"3": 1, "5": 2},
  "w12": {"2": 1},
  "w2": {"2": 1, "3": 3, "5": 1},
  ...
   }
 ```

6. Enviar el diccionario local (del buffer) a disco

   - Una vez que se ha procesado un bloque y el diccionario está completo, es necesario guardar el diccionario en disco. Esto asegura que no se pierdan los datos y permite que se libere espacio en la memoria para procesar el siguiente bloque.


 7. Repetir los pasos del 1 al 6 por cada buffer

      - Se repiten los pasos anteriores para cada bloque de datos (o buffer). Esto implica leer el siguiente bloque, procesarlo, agregar las palabras preprocesadas al diccionario, y luego guardarlo en disco.

 8. Cuando se termine de procesar todos los bloques del CSV, hacer un Merge entre los índices locales (mezcla en un índice global)

      - Una vez que se hayan procesado todos los bloques del CSV, se debe realizar un **merge** o mezcla de los índices locales generados para cada bloque. Esto significa combinar todos los diccionarios locales en un solo índice global que contendrá toda la información procesada.
      - Este paso es crucial para consolidar toda la información de manera eficiente y permitir que se puedan realizar búsquedas sobre el índice global.

![image](https://github.com/user-attachments/assets/b04ef552-180a-4891-b045-89223d6246d1)

 9. Luego del octavo paso, se tiene un solo índice global distribuido entre todos los archivos de índice (.json)

### Manejo de memoria secuandaria

### Ejecución óptima de consultas
# Ejecución óptima de consultas

Cuando recibimos una consulta (query), el proceso es el siguiente:
   - Obtener el índice invertido de la consulta: buscamos en el índice invertido para encontrar la información relacionada con los términos de la consulta.

   - Aplicar similitud coseno: usamos la **similitud coseno** para comparar los términos de la consulta con los documentos, sin necesidad de crear vectores complejos. Esto se hace de manera eficiente usando diccionarios, lo que ahorra tiempo y espacio.

   - Uso del índice invertido global: ya tenemos un índice invertido global guardado en disco para todo el dataset. Esto significa que no necesitamos recalcularlo cada vez, lo que acelera la búsqueda.

   - Búsqueda binaria: para encontrar rápidamente un término y sus ocurrencias, utilizamos **búsqueda binaria**. Esto mejora la velocidad de las consultas porque nos permite buscar en el índice de manera eficiente.

### Realización del KNN Search y el Range Search
El Knn Search consiste en en los K vecinos más cercanos de un punto usando la distancia euclidiana (suma de minkowski para k = 2), mientras que el range search consiste en buscar los hasta una determinada distancia
## Frontend

### Diseño del Índice con PostgreSQL
   - Para cargar nuestro dataset en postgress hicimos uso de las librerías psycopg2 y csv.
```sql
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()
 ```
   - Lo primero que hicimos fue definir la función init para crear la tabla styles y poblarla con los datos de nuestra dataset.
```sql
def init():
    with open('C:/Users/ASUS/Downloads/prueba/styles.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        cTableCommand = "CREATE TABLE IF NOT EXISTS styles (id INT, gender VARCHAR(10), masterCategory VARCHAR(25), subCategory VARCHAR(25), articleType VARCHAR(25), baseColour VARCHAR(25), season VARCHAR(10), year INT NULL, usage VARCHAR(25), productDisplayName VARCHAR(255))"
        cursor.execute(cTableCommand)
 ```
   - Dentro de la misma función, añadimos la creación de dos columnas del tipo weighted_tsv. Una de estas la indexaremos y es la que usaremos en la búsqueda.
```sql
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv tsvector")
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv2 tsvector")
    cursor.execute("UPDATE styles SET weighted_tsv = x.weighted_tsv, weighted_tsv2 = x.weighted_tsv FROM (SELECT id, setweight(to_tsvector('english', COALESCE(masterCategory,'')), 'A') || setweight(to_tsvector('english', COALESCE(articleType,'')), 'A') || setweight(to_tsvector('english', COALESCE(baseColour,'')), 'A') || setweight(to_tsvector('english', COALESCE(season,'')), 'A') || setweight(to_tsvector('english', COALESCE(usage,'')), 'A') || setweight(to_tsvector('english', COALESCE(productdisplayname,'')), 'B') AS weighted_tsv FROM styles) AS x WHERE x.id = styles.id;")
    cursor.execute("CREATE INDEX weighted_tsv_idx ON styles USING GIN (weighted_tsv2)")
    connection.commit()
    curso.close()
 ```
   - Definimos la función para que nos retorne las k filas más similares a la query 
```sql
consulta = f"""SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname
FROM(
  SELECT
  id,
  gender,
  mastercategory,
  subcategory,
  articletype,
  basecolour,
  season,
  year,
  usage,
  productdisplayname,
  ts_rank_cd(weighted_tsv2, to_tsquery('english', '(terms)')) AS similarity
  FROM styles
  WHERE to_tsquery('english', '{terms}') @@ weighted_tsv2
  ORDER BY similarity DESC LIMIT (k}
) AS R"""
cursor.execute(consulta)
rows = cursor.fetchall()
 ```
### Screeenshots de la GUI
Pantalla Principal y Única:
![frontend01](https://github.com/user-attachments/assets/3de8aeb9-9788-4c0a-837b-f49509f105ed)
### Resultados de la query
- Aplicamos la query textual *"red shoes"*
  - Resultados con índice invertido
     ![frontend02](https://github.com/user-attachments/assets/f52dbf6c-863e-4079-affc-0ecd7de15c45)

  - Resultados con postgresSQL
    ![frontend03](https://github.com/user-attachments/assets/15a29865-46a1-4b2e-a3e2-3fe88588b2ba)

## Análisis y Discución
- Al comparar nuestras consultas textuales con los resultados generados en PostgreSQL, encontramos que nuestra implementación ofrece una mayor eficiencia al devolver resultados relevantes.
- PostgreSQL realiza búsquedas más precisas cuando utiliza el operador AND ("&") para unir cada palabra de la consulta. Sin embargo, al emplear el operador OR ("|"), no considera la frecuencia de los términos en los resultados, lo que da lugar a respuestas menos relevantes. Esto se evidenció al ejecutar una consulta que contenía un término común (como "casual"), donde las palabras frecuentes no fueron adecuadamente diferenciadas de las menos comunes.



