# Implementación de Detector y Extractor de Trayectorias

## Descripción
Este documento busca describir algunos de los elementos importantes para implementar una clase de detección compatible con el software implementado. Esta clase debe implementar métodos para detectar objetos, obtener trayectorias y calcular puntos de seguimiento.

## Componentes Clave
1. **DetectorStrategy (Clase Base)**: base que proporciona una interfaz común para diferentes estrategias de detección.
2. **Modelo de detección de objetos**: En un principio se debe identificar con que modelo de detección de objetos se desea trabajar, por ejemplo YOLOv8.
3. **Modelo de Seguimiento de Múltiples Objetos (MOT):** Se debe definir que método de seguimiento se va a sumar a los resultados de la detección para identificar y seguir vehículos de las detecciones.

## Implementación 

Para implementar un extractor de trayectorias, lo más importante es que se debe implementar una clase que herede de DetectorStrategy y debe considerar los métodos descritos en el archivo `detector_strategy.py`, estos son `detect()` y `get_trajectories()`:
### Método `detect`
- **Entrada**:
  - `video_path` (str): Ruta al archivo de video para el análisis.
  - `video_fps` (float): Frames por segundo del video.
- **Procesamiento**: Utiliza el modelo seleccionado para detectar objetos en el video.
- **Salida**:
  - Lista de diccionarios, cada uno representando las detecciones en un frame. Cada diccionario tiene claves que son los IDs de seguimiento y valores que son otro diccionario con información de la detección. En este ultimo se incluyen `"bbox"`, `"class"`, `"score"`, `"frame"`, que corresponden a las etiquetas, índice de clases, confidence y el numero de frame en el que se encuentran respectivamente (Especificadas más adelante en Estructura de Datos).

### Método `get_trajectories`
- **Entrada**:
  - `detections`: Lista de detecciones como se retorna del método `detect`.
- **Procesamiento**: Calcula las trayectorias de cada objeto detectado en el video.
- **Salida**:
  - Un diccionario donde cada clave es un ID de seguimiento y cada valor es otro diccionario que contiene las trayectorias `x` e `y`, la clase del objeto, los frames en los que se detectó, y los tiempos correspondientes (Especificadas más adelante en Estructura de Datos).

## Estructuras de Datos 

### Detecciones
- **Formato**: Lista de diccionarios. Cada diccionario tiene claves que son los IDs de seguimiento, y valores que son diccionarios con las siguientes llaves: `"bbox"`, `"class"`, `"score"`, `"frame"`.
- **Ejemplo**:
  ```python
  [
      {
          1: {
              "bbox": [50, 100, 200, 400],
              "class": "auto",
              "score": 0.85,
              "frame": 1
          },
          2: {
              "bbox": [30, 90, 150, 300],
              "class": "bus",
              "score": 0.75,
              "frame": 1
          }
      },
      # ... más frames
  ]

### Trayectorias
- **Formato**: Diccionario donde cada clave es un ID de seguimiento y cada valor es otro diccionario con las llaves `"x_trajectory"`, `"y_trajectory"`, `"class"`, `"frames"`, `"time"`.
- **Ejemplo**:
  ```python
  {
    1: {
        "x_trajectory": [125, 130, 135],
        "y_trajectory": [250, 255, 260],
        "class": "auto",
        "frames": [1, 2, 3],
        "time": [0.0, 0.04, 0.08]
    },
    2: {
        "x_trajectory": [90, 95, 100],
        "y_trajectory": [195, 200, 205],
        "class": "bus",
        "frames": [1, 2, 3],
        "time": [0.0, 0.04, 0.08]
      }
      # ... más trayectorias
  }
