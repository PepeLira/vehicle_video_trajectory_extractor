# Implementación de Estabilizadores Video o Alineadores de Cuadros

## Descripción
Dada la naturaleza de los videos cenitales utilizados en este proyecto, es posible encontrar desplazamientos, rotaciones y escalamientos sobre la escena. Es por esto que se plantea la necesidad de implementar estrategias que permitan corregir dichas variaciones sobre la escena y así exportar datos más limpios con las trayectorias de los vehículos. 

Este documento busca describir algunos de los elementos importantes para implementar una clase de alineación compatible con el software implementado.

## Componentes Clave

1. **AlignerStrategy (Clase Base)**: base que proporciona una interfaz común para diferentes estrategias de alineación.
2. **Metodo de extracción y emparejado de caracteristicas:** Se deben estudiar metodos de extracción y emparejado de caracteristicas tales como SIFT y ORB.

## Implementación 

Para implementar un estabilizador de video o alineador de cuadros, es fundamental implementar una clase que herede de AlignerStrategy y considere los métodos descritos en el archivo `aligner_strategy.py`. Estos son `set_affine_transformations()`, `align()` y `update_affine_transformations()`:

### Método `set_affine_transformations`

- **Entrada**:
    - `input_video` (str): Ruta al archivo de video para el análisis.
- **Procesamiento**: Establece las transformaciones afines para cada cuadro del video utilizando el método de extracción y emparejamiento de características seleccionado.
- **Salida**:
    - Actualiza el atributo `self.affine_transformations` con una lista de las transformaciones afines para cada cuadro.

### Método `align`

- **Entrada**:
    - `frame` (array): Cuadro a alinear.
    - `frame_index` (int): el índice del cuadro a alinear (0 es el primer cuadro).
    - `affine_transformations` (lista): lista de transformaciones afines para cada cuadro (`[theta, s, tx, ty]`).
- **Procesamiento**: Alinea un cuadro dado las transformaciones afines para cada cuadro.
- **Salida**:
    - Cuadro alineado.

### Método `update_affine_transformations`

- **Entrada**:
    - `affine_transformations` (lista): lista de transformaciones afines para cada cuadro (`[theta, s, tx, ty]`).
- **Procesamiento**: Actualiza las transformaciones afines para cada cuadro.
- **Salida**:
    - Actualiza el atributo `self.affine_transformations` con la nueva lista de transformaciones afines.

## Estructuras de Datos 

Ejemplo de estructura de salida para `affine_transformations`
  ```python
  [
      # Transformaciones afines para el primer cuadro
      [
          "theta": 0.0, # Rotación
          "s": 1.0, # Escala
          "tx": 0.0, # Traslación en x
          "ty": 0.0  # Traslación en y
      ],
      # Transformaciones afines para el segundo cuadro
      [
          "theta": 0.01,
          "s": 0.99,
          "tx": 1.0,
          "ty": -1.0
      ],
      # ...
      # Transformaciones afines para el último cuadro
      [
          "theta": -0.01,
          "s": 1.01,
          "tx": -1.0,
          "ty": 1.0
      ]
  ]