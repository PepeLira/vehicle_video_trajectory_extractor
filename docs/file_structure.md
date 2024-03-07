# Descripción de los Directorios del Proyecto

El proyecto se divide en dos directorios principales: `desktop_application` y `research`.

## desktop_application

En este directorio se encuentra la implementación del software de escritorio que integra los dos métodos investigados en el proyecto: el algoritmo de alineamiento de fotogramas y el detector de vehículos. El software es modular y fácilmente desacoplable, y cuenta con una interfaz gráfica intuitiva que permite seleccionar archivos y opciones de configuración.

Las subcarpetas dentro de `src` incluyen:

- `alignment`: Contiene los archivos de modelado de alineamiento.
- `controllers`: Contiene los controladores para el patrón MVC.
- `filters`: Contiene los archivos de modelado de filtros.
- `trajectory_extraction`: Contiene los archivos de modelado del extractor de trayectorias.
- `views`: Contiene las vistas para el patrón MVC.

## research

Este directorio se utiliza para investigar los métodos utilizados en el proyecto. Incluye dos subdirectorios:

- `video_alignment_methods`: En esta carpeta se realizan investigaciones sobre el algoritmo de alineamiento de fotogramas.
- `object_detection_methods`: Aquí se investiga el detector de vehículos y extractor de trayectorias.

Además, el proyecto incluye un directorio `datasets` para almacenar los conjuntos de datos necesarios para el modelo de detección de objetos, y un script que interpreta el conjunto de datos y lo proporciona en el formato necesario.

```
📂 vehicle_video_trajectory_extractor/
├── 📄 README.md
├── LICENSE
├── 📂 research/
│   ├── 📂 video_alignment_methods/
│   │   ├── 📄 README.md
│   │   └── [archivos de investigación y documentación]
│   │
│   └── 📂 object_detection_methods/
│       ├── 📄 README.md
│       └── [archivos de investigación y documentación]
│
├── 📂 datasets/
│   ├── 📄 README.md
│   ├── 📄 interpreter_script.py  # Script para interpretar y formatear el dataset
│   └── [carpetas y archivos del dataset]
│
├── 📂 docs/ # Documentación del software
│   ├── 📄 Estructura_de_archivos.md
│   └── [archivos de documentación]
│
└── 📂 desktop_aplication/
    ├── 📄 README.md
    └── 📂 src/  # Código fuente
        ├── 📂 alignment/
        │   └── [archivos modelado de alineamiento]
        ├── 📂 controllers/
        │   └── [controllers para patron MVC]
        │
        ├── 📂 filters/
        │   └── [archivos modelado de filtros]
        │
        ├── 📂 trajectory_extraction/
        │   └── [archivos modelado de extractor de trayectorias]
        │
        ├── 📂 views/
        │   └── [views para patron MVC]
        │
        └── [main, requirements.txt y modelo VideoProcessor.py ]