# Formato del Archivo CSV para Trayectorias de Vehículos

Este documento describe el formato del archivo CSV utilizado para almacenar las trayectorias de vehículos. El archivo consta de varias columnas que representan diferentes atributos de los vehículos y sus posiciones a lo largo del tiempo.

## Estructura de Columnas

El archivo CSV sigue la siguiente estructura de columnas:

- `id de vehículo`: Identificador único para cada vehículo.
- `class`: Clase del vehículo (por ejemplo, `car` para coches).
- `número de frame`: Número de frame o cuadro de la secuencia de video de donde se extrajo la información.
- `posición en i`: Posición en el eje i (usualmente correspondiente a la coordenada vertical en píxeles).
- `posición en j`: Posición en el eje j (usualmente correspondiente a la coordenada horizontal en píxeles).
- `posición en x (metros)`: Posición del vehículo en el eje x en metros, representando el desplazamiento horizontal.
- `posición en y (metros)`: Posición del vehículo en el eje y en metros, representando el desplazamiento vertical.
- `tiempo`: Tiempo en segundos en el que se registra la posición del vehículo.
- `velocidad x (metros)`: Velocidad del vehículo en el eje x en metros por segundo.
- `velocidad y (metros)`: Velocidad del vehículo en el eje y en metros por segundo.

## Ejemplo de Contenido

| id de vehículo | class | número de frame | posición en i | posición en j | posición en x (metros) | posición en y (metros) | tiempo | velocidad x (metros) | velocidad y (metros) |
| -------------- | ----- | --------------- | ------------- | ------------- | ---------------------- | ---------------------- | ------ | -------------------- | -------------------- |
| 1              | car   | 1               | 10            | 20            | 0                      | 0                      | 0.0    | 0                    | 0                    |
| 1              | car   | 2               | 11            | 21            | 0.1                    | 0.2                    | 0.1    | 1                    | 1                    |
| 2              | car   | 1               | 20            | 40            | 0                      | 0                      | 0.0    | 0                    | 0                    |
