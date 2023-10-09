# Definir una estructura para los archivos del proyecto

El repositorio del proyecto debe contar con una carpeta para continuar con la investigación de los métodos utilizados en este estudio. El primer método corresponde a un algoritmo de alineamiento de fotogramas. El segundo a un detector de vehículos y extractor de trayectorias una vez estos fueron identificados.

Para la investigación es necesario separar en una carpeta los datasets a trabajar para el modelo detector de objetos, este deberá apoyarse de un script que interprete el dataset junto a sus etiquetas y lo provea en el formato necesario. 

La raíz también debe contar con una carpeta con la implementación de un software de escritorio que integre los dos métodos estudiados, de manera modularizada y fácilmente desacoplable. Además deberá contar con una interfaz gráfica que permita interactuar con el de manera simple e intuitiva, permitiendo seleccionar archivos y opciones de configuración. Debe seguir un flujo de dos etapas:

### Etapa 1:

- Selección de Video
- Preguntar si se desea alinear (estabilizar)
    - Seleccionar método de alineamiento
- Permitir seleccionar filtros a aplicar sobre las transformaciones obtenidas
- Transparentar método a utilizar y filtros a aplicar antes de continuar
- Aplicar alineamiento y mostrar barra de progreso

### Etapa 2:

- Permitir seleccionar modelo para extraer trayectorias
- Permitir seleccionar filtros a aplicar sobre las trayectorias
- Aplicar modelo y filtros seleccionados (mostrar barra de progreso)

### Menú de opciones:

- Exportar transformaciones de alineamiento (se desbloquea después de alinear)
- Exportar las trayectorias antes de filtrar y después de filtrar (se desbloquea después de calcular trayectorias)

### Interfaz:

- Preferentemente debe mostrar una pre visualización del video
- Debe permitir cambiar entre los diferentes estados del video para comparar (idealmente si pueden estar uno al lado del otro)


```
📂 project/
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
    ├── 📂 src/  # Código fuente
    │   ├── 📄 main.py
    │   ├── 📂 alignment/
    │   │   └── [módulos y scripts de alineamiento]
    │   │
    │   └── 📂 trajectory_extraction/
    │       └── [módulos y scripts de detección y extracción de trayectorias]
    │
    ├── 📂 ui/  # Archivos de interfaz de usuario
    │   └── [archivos de diseño de interfaz, e.g., .ui, .qss]
    │
    ├── 📂 tests/  # Pruebas unitarias y de integración
    │   └── [scripts de prueba]
    │
    └── 📂 build/  # Binarios y ejecutables
        └── [archivos compilados y ejecutables]
```