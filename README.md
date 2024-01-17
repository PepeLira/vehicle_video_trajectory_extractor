# RastreoAéreo: Vehicle Trajectory Extractor

**RastreoAéreo** es un proyecto colaborativo coordinado por la Facultad de Ingeniería Civil de la Universidad de los Andes - Chile, el cual tiene como objetivo desarrollar una solución integral para el análisis y seguimiento de vehículos en videos capturados desde una perspectiva aérea.

En este repositorio, encontrarás todo el **código fuente**, la **documentación** detallada y los recursos necesarios para comprender y utilizar esta solución. Además, se proporcionan **conjuntos de datos de ejemplo** y **modelos pre-entrenados** para facilitar la reproducción y extensión de los resultados obtenidos.

La solución propuesta integra métodos previamente estudiados y valida el sistema utilizando sistemas comerciales y un método empírico para la extracción de trayectorias. El repositorio incluye código para el alineamiento de los fotogramas de videos, autosegmentación de automóviles y la extracción de trayectorias utilizando el friltro de Kalman,  modelos lineales de flujo vehicular.

| Categoría                     | Funcionalidades Clave                                      | Completitud    |
|-------------------------------|------------------------------------------------------------|----------------|
| **Almacenamiento y Acceso**   | - Posibilidad de guardar videos procesados.                | ✅ |
|                               | - Disponibilidad de datasets en la nube.                   | ❌ |
| **Exportación de Datos**      | - Exportación de resultados en formato CSV.                | ✅ |
|                               | - Exportación de trayectorias y parámetros de alineación.  | ✅ |
| **Procesamiento de Video**    | - Alineación automática de videos.                         | ⭕ |
|                               | - Detección y seguimiento de vehículos.                    | ⭕ |
| **Interfaz y Usabilidad**     | - Interfaz intuitiva para cargar y procesar videos.        | ✅ |
|                               | - Manejo de errores y condiciones de borde.                | ⭕ |
| **Continuidad y Desarrollo**  | - Documentación formato de salida de datos (CSV).          | ⭕ |
|                               | - Documentación clases de extractores de trayectorias.     | ✅ |
|                               | - Documentación clases de alineadores de fotogramas.       | ⭕ |
| **Investigación y Desarrollo**| - Describir Notebooks con el funcionamiento de alineadores.| ✅ |
|                               | - Describir Notebooks con el entrenamiento de modelos.     | ✅ |
|                               | - Describir Notebooks con el seguimiento de detecciones.   | ✅ |
| **Compatibilidad y Acceso**   | - Ejecución remota de notebooks IPython en Colab.          | ✅ |
|                               | - Compatibilidad con diferentes formatos de video.         | ✅ |

![image](https://github.com/PepeLira/vehicle_video_trajectory_extractor/assets/43451889/2ffde6b4-ed44-472d-a32a-bedfad92eb20)
