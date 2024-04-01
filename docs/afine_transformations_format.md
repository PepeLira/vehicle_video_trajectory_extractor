# Formato del Archivo CSV para Transformaciones Afines en Video

Este documento describe el formato del archivo CSV que registra las transformaciones afines aplicadas a los frames de un video. Las transformaciones afines son operaciones que incluyen rotación, escala, traslación (desplazamiento), y sus combinaciones, que se aplican sobre las imágenes para modificar su orientación o posición en un plano. Este tipo de transformación es fundamental en el procesamiento de imágenes y la visión por computadora, especialmente para la alineación y corrección de imágenes.

## Descripción de Columnas

El archivo CSV consta de las siguientes columnas:

- `número de frame`: El número de secuencia del frame dentro del video. El primer frame es considerado el frame de referencia.
- `theta`: El ángulo de rotación en radianes. Representa la rotación que se debe aplicar al frame con respecto al frame de referencia.
- `s`: Factor de escala. Indica el cambio de tamaño que se debe aplicar al frame. Un valor de 1 indica el tamaño original, mientras que valores menores o mayores ajustan el tamaño respectivamente.
- `tx`: Traslación en el eje x. Representa el desplazamiento horizontal del frame con respecto a su posición original.
- `ty`: Traslación en el eje y. Representa el desplazamiento vertical del frame con respecto a su posición original.

## Ejemplo de Archivo CSV

```csv
número de frame,theta,s,tx,ty
1,0.0,0.0,0.0,0.0 # El primer frame es el frame de referencia
2,0.2,0.3,0.4,0.5
```