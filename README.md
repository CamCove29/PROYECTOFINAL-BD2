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

La implementación consiste 
Nuestra implementación consiste en:

1. Leer el archivo .csv de acuerdo a cantidad de un buffer (considerando que tenga un número exacto de filas, osea no haga la partición de las filas)
2. Preprocesar cada fila
3. Concatenar datos de cada fila (calculando la norma y el peso de cada palabra por fila)
![image](https://github.com/user-attachments/assets/7c2afa53-9bbc-44b5-8905-e9b6f67aa959)
### Elementos de la fórmula

#### ** \(\|v\|\): **
- Representa la **norma** del vector \(v\).
- Es un escalar (un único número) que mide la **magnitud** o **longitud** del vector \(v\).
- En este contexto, el vector \(v\) puede representar los **pesos de las palabras** en una fila de una matriz de términos (por ejemplo, en un índice invertido).

---

#### ** \(\sum_{i=0}^n\): **
- Es el **símbolo de suma**, que indica que se sumarán los términos desde el índice \(i = 0\) hasta \(i = n\).
- El **índice \(i\)** representa la posición de cada palabra en la fila.
- **\(n\)** es el **número total de palabras o términos en la fila** (o el tamaño del vector).

---

#### **\((v_i)^2\):**
- Es el **cuadrado del peso** del término \(i\).
- Esto se hace porque la fórmula de la **norma euclidiana** se basa en el **teorema de Pitágoras**: suma de los cuadrados de las coordenadas.

---

### Optimización de Consultas con Similitud de Coseno


### Construcción del Índice Invertido en PostgreSQL
