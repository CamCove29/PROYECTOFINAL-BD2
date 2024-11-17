# PROYECTO 2&3 BD2
## Integrantes:
- Camila Milagros Coveñas Rojas
## Introducción
### Objetivo del Proyecto
Este proyecto está enfocado en desarrollar un proyecto integral de base de datos que soporte tanto el modelo relacional basado en tablas como técnicas avanzadas de recuperación de información basadas en el contenido de documentos textuales y objetos multimedia. 
![Clothing department store interior](https://github.com/user-attachments/assets/b4d4cfcf-30b0-4b5b-b798-491ff841eb04)
### Descripción del Dataset 
Fashion Products Dataset (https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset/data), es una recopilación estructurada de información sobre productos de moda. Esta información se separa en dos archivos principales .csv:      
styles.csv: Este archivo contiene las columnas id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName. La información de cada producto es representada en una fila:
![image](https://github.com/user-attachments/assets/6aa9b584-f942-4f2f-9ae7-9945d587cbe2)
images.csv: Este archivo contiene las columnas filename,link, donde filename representa el id de cada imagen y link representa la ubicación de cada imagen.
![image](https://github.com/user-attachments/assets/fb17bbe8-d994-4573-8ebc-aa7ef44bf06b)
### Importancia de Aplicar Indexación
La indexación es una técnica esencial en sistemas de gestión de datos que permite realizar búsquedas rápidas y eficientes, mejorando la experiencia del usuario y optimizando el uso de recursos en grandes volúmenes de datos.
1. **Índices Invertidos**  
   Los índices invertidos son ideales para buscar términos específicos en grandes colecciones de texto. Este método asocia cada término con una lista de documentos donde aparece, permitiendo una búsqueda rápida sin escanear toda la base de datos. Es fundamental en motores de búsqueda y sistemas de recuperación de texto.
2. **Índices Multidimensionales**  
   Utilizados para datos con múltiples atributos, como coordenadas geográficas o características musicales. Los índices multidimensionales permiten consultas complejas en bases de datos con información de alta dimensionalidad. Estructuras como R-trees y KD-trees son comunes en aplicaciones de geolocalización y análisis de datos espaciales.
