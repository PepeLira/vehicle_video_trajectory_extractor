# Aplicación de Escritorio

Este documento describe aspectos importantes para ejecutar la aplicación de escritorio y continuar con su desarrollo.

## Requerimientos Previos

Antes de comenzar, asegúrate de cumplir con los siguientes requisitos:

- Python versión 3.7 o superior.
- Un modelo preentrenado de YOLOv8 disponible en el directorio raíz `pretrained_models/`.
- Pytorch 2.2.1 o una versión estable posterior, a la fecha de referencia 07/02/2024. ([Guía de instalación de pytorch](..\docs\torch_install_guide.md))

### Espacios Virtuales (Opcional)

Para una mejor gestión de dependencias, se recomienda el uso de `pyenv` o cualquier entorno virtual de su elección.

## Primeros Pasos para Lanzar la Aplicación

1. Asegúrate de estar en el directorio correcto:

    ```bash
    cd desktop_aplication/src
    ```

2. Si es la primera vez que ejecutas la aplicación, instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Para lanzar la aplicación, ejecuta:

    ```bash
    python ./main.py
    ```

## Estructura del Repositorio

La aplicación sigue un patrón de diseño MVC (Modelo-Vista-Controlador) y se organiza en las siguientes carpetas:


  ```bash
  src/
  ├── alignment/                 # Implementación de estrategias de alineación.
  ├── controllers/               # Integración de la interfaz gráfica con la lógica de procesamiento.
  ├── filters/                   # Estrategias para filtros de alineamiento y extracción.
  ├── models/                    # Modelos usados en la aplicación.
  ├── trajectory_extraction/     # Estrategias para la extracción de trayectorias.
  │   └── extensions/
  └── views/                     # Elementos de la interfaz gráfica de usuario.

  ```

  
### Archivos Clave

- `video_processor.py`: Inicia la ejecución del procesador de video.
- `video_processor_controller.py`: Conecta la interfaz gráfica con el procesador de video y los modelos.
- `input_video.py`: Interactúa con los archivos de video seleccionados.


## Implementar Modulos

- [Guía para implementar Detectores y Extractores de Trayectorias](../docs/implementar_detector.md)  
- [Guía para alineadores de video](../docs/implementar_alineadores.md)
