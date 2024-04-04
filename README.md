# RastreoAéreo: Vehicle Trajectory Extractor

**RastreoAéreo** es un proyecto colaborativo coordinado por la Facultad de Ingeniería Civil de la Universidad de los Andes - Chile, el cual tiene como objetivo desarrollar una solución integral para el análisis y seguimiento de vehículos en videos capturados desde una perspectiva aérea.

En este repositorio, encontrarás todo el **código fuente**, la **documentación** detallada y los recursos necesarios para comprender y utilizar esta solución. Además, se proporcionan **conjuntos de datos de ejemplo** y **modelos pre-entrenados** para facilitar la reproducción y extensión de los resultados obtenidos.

La solución propuesta integra métodos previamente estudiados y valida el sistema utilizando sistemas comerciales y un método empírico para la extracción de trayectorias. El repositorio incluye código para el alineamiento de los fotogramas de videos, autosegmentación de automóviles y la extracción de trayectorias utilizando el friltro de Kalman,  modelos lineales de flujo vehicular.


Este repositorio está mayormente dividido en dos directorios para cumplir con dos propósitos: 
- `research/` para continuar con la investigación de modelos de detección y seguimiento de vehículos, además de sistemas de alineamiento y estabilización de video.
- `desktop_aplication/` enfocada al desarrollo de una aplicación de escritorio que implementa e integra las soluciones estudiadas previamente.

Adicionalmente, contamos con el directorio `pretrained_models/` para almacenar los modelos necesarios para los dos casos. 

## Guía de inicio rapido - Aplicación de Escritorio

Para comenzar a trabajar con la aplicación de escritorio [se deben seguir los siguientes pasos disponibles en la documentación.](./desktop_aplication/README.md)

## Investigación y Desarrollo

La aplicación cuenta con modelos pre-entrenados disponibles en el directorio [`/pretrained_models/`](pretrained_models/), estos fueron entrenados con una combinación de nuestro dataset original de videos aéreos de tráfico ininterrumpido en perspectiva cenital, en conjunto a una selección de imágenes etiquetadas provenientes del dataset [DOTAv2](https://captain-whu.github.io/DOTA/index.html). [Es posible descargar el dataset implementado  desde el siguiente link en este enlace.](https://drive.google.com/file/d/1jzNW6sFu_DrKQISmGjWIdWuqBrhkxfTR/view?usp=sharing)

A modo de ejemplo en el directorio `research/object_detection_method/`, es posible encontrar documentos Jupyter Notebook describiendo el proceso de entrenamiento y evaluación del modelo YOLOv8.

## Formato Trayectorias y Transformaciones en CSV

Luego de procesar un video, es posible exportar los resultados al [alinear un video](./docs/afine_transformations_format.md) y [extraer trayectorias](./docs/trajectories_format.md) en un archivo de texto `.csv` siguiendo los siguientes formatos:

- [Transformaciones](./docs/afine_transformations_format.md)
- [Trayectorias](./docs/trajectories_format.md)

# Caracteristicas de la Aplicación

| Categoría                     | Funcionalidades Clave                                      |
|-------------------------------|------------------------------------------------------------|
| **Almacenamiento y Acceso**   | - Posibilidad de guardar videos procesados.                | 
|                               | - Disponibilidad de datasets en la nube.                   |
| **Exportación de Datos**      | - Exportación de resultados en formato CSV.                |
|                               | - Exportación de trayectorias y parámetros de alineación.  |
| **Procesamiento de Video**    | - Alineación automática de videos.                         |
|                               | - Detección y seguimiento de vehículos.                    |
| **Interfaz y Usabilidad**     | - Interfaz intuitiva para cargar y procesar videos.        |
|                               | - Manejo de errores y condiciones de borde.                |
| **Continuidad y Desarrollo**  | - Documentación formato de salida de datos (CSV).          |
|                               | - Documentación clases de extractores de trayectorias.     |
|                               | - Documentación clases de alineadores de fotogramas.       |
| **Investigación y Desarrollo**| - Describir Notebooks con el funcionamiento de alineadores.|
|                               | - Describir Notebooks con el entrenamiento de modelos.     |
|                               | - Describir Notebooks con el seguimiento de detecciones.   |
| **Compatibilidad y Acceso**   | - Compatibilidad con diferentes formatos de video.         |
|                               |                                                            |

![image](https://github.com/PepeLira/vehicle_video_trajectory_extractor/assets/43451889/2ffde6b4-ed44-472d-a32a-bedfad92eb20)
