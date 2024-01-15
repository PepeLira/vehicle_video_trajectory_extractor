# Implementación de Detector y Extractor de Trayectorias

## Descripción
Este documento busca describir algunos de los elementos importantes para implementar una clase de detección compatible con el software implementado. Esta clase debe implementar métodos para detectar objetos, obtener trayectorias y calcular puntos de seguimiento.

## Componentes Clave
1. **DetectorStrategy (Clase Base)**: base que proporciona una interfaz común para diferentes estrategias de detección.
2. **Ultralytics YOLO (Modelo)**: En un principio se utiliza el modelo YOLO de Ultralytics para la detección de objetos. es posible implementar clases para nuevos modelos de detección de objetos.

## Métodos y sus Descripciones

### Constructor `__init__`
- **Entrada**:
  - `source_weights_path` (str): Ruta al archivo de pesos del modelo YOLO.
  - `detection_threshold` (float): Umbral de `confidence` para la detección de objetos.

### Método `detect`
- **Entrada**:
  - `video_path` (str): Ruta al archivo de video para el análisis.
  - `video_fps` (float): Frames por segundo del video.
- **Procesamiento**: Utiliza el modelo YOLO para detectar objetos en el video.
- **Salida**:
  - Lista de diccionarios, cada uno representando las detecciones en un frame. Cada diccionario tiene claves que son los IDs de seguimiento y valores que son otro diccionario con información de la detección.

### Método `get_trajectories`
- **Entrada**:
  - `detections`: Lista de detecciones como se retorna del método `detect`.
- **Procesamiento**: Calcula las trayectorias de cada objeto detectado en el video.
- **Salida**:
  - Un diccionario donde cada clave es un ID de seguimiento y cada valor es otro diccionario que contiene las trayectorias `x` e `y`, la clase del objeto, los frames en los que se detectó, y los tiempos correspondientes.

### Método `calculate_tracking_point`
- **Entrada**:
  - `bbox` (list): Lista que contiene las coordenadas del cuadro delimitador [x1, y1, x2, y2].
- **Procesamiento**: Calcula el punto central del cuadro delimitador.
- **Salida**:
  - Tupla `(x, y)` que representa el punto central del cuadro delimitador.

### Método `__str__`
- **Salida**: Cadena que representa el tipo de detector (`"YOLOv8 Detector"`).

## Estructuras de Datos y Ejemplos

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
