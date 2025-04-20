# SoundFresh - Reproductor de Música Desktop

SoundFresh es un proyecto de reproductor de música de escritorio desarrollado en Python utilizando la biblioteca PyQt6 para la interfaz gráfica y **SQLite** para la gestión de datos locales (usuarios y playlists).

## Tecnologías Clave

*   **Python:** Lenguaje de programación principal.
*   **PyQt6:** Biblioteca para la creación de la interfaz gráfica de usuario (GUI).
*   **SQLite:** Sistema de gestión de bases de datos relacional ligero y basado en archivos, utilizado para almacenar:
    *   Información de usuarios (credenciales cifradas con bcrypt).
    *   Playlists creadas por los usuarios.
*   **bcrypt:** Biblioteca para el hash seguro de contraseñas.
*   **PyQt6.QtMultimedia:** Módulo para la reproducción de archivos de audio.

## Funcionalidades Principales

*   **Autenticación de Usuarios:** Registro y login de usuarios con almacenamiento seguro de contraseñas.
*   **Exploración de Música Local:** Abrir carpetas locales que contengan archivos MP3.
*   **Reproducción de Música:**
    *   Controles básicos (Play/Pause, Siguiente, Anterior).
    *   Modo aleatorio (Shuffle).
    *   Modo repetición (Repeat song).
*   **Gestión de Playlists:**
    *   Guardar la lista de canciones actual como una nueva playlist asociada al usuario.
    *   Ver las playlists guardadas por el usuario.
    *   Cargar canciones de una playlist guardada en el reproductor.
    *   Eliminar playlists guardadas.
*   **Interfaz Gráfica:**
    *   Ventana principal con pestañas para Reproductor, Biblioteca (Playlists) y Ajustes (futuro).
    *   Panel lateral (dock) para mostrar la lista de canciones actual.
    *   Menú de acciones (Abrir carpeta, Guardar playlist, Cerrar sesión, Salir).

## Estructura del Proyecto

```
/
|-- data/                     # Directorio para la base de datos SQLite (creado automáticamente)
|   |-- soundfresh.db         # Archivo de la base de datos SQLite
|-- img/                      # Imágenes para la interfaz
|-- src/
|   |-- database/
|   |   |-- db_setup.py       # Script para inicializar la base de datos y tablas
|   |-- login/
|   |   |-- constants.py      # Constantes (ej. listas para ComboBox)
|   |   |-- loginSF.py        # Lógica y UI de la ventana de login
|   |   |-- registerSF.py     # Lógica y UI de la ventana de registro
|   |-- reproductor/
|   |   |-- form_playlist.py  # Lógica y UI del formulario para guardar playlists
|   |   |-- reprocSF.py       # Lógica y UI de la ventana principal del reproductor
|   |-- __init__.py           # Archivos __init__.py para reconocer los directorios como paquetes
|-- styles/
|   |-- estilosMenu.css       # Archivos CSS para estilizar la UI
|   |-- estilosRep.css
|   |-- img/                  # Imágenes usadas en los CSS
|-- main.py                   # Punto de entrada de la aplicación
|-- README.md                 # Este archivo
|-- requirements.txt          # (Recomendado) Archivo para listar dependencias
```

## Cómo Ejecutar

1.  **Clonar el repositorio:**
    ```bash
    git clone <url_del_repositorio>
    cd <nombre_del_repositorio>
    ```
2.  **Instalar dependencias:** (Asegúrate de tener Python y pip instalados)
    *   Se recomienda crear un entorno virtual:
        ```bash
        python -m venv venv
        source venv/bin/activate  # En Linux/macOS
        venv\Scripts\activate      # En Windows
        ```
    *   Instalar las bibliotecas necesarias (idealmente desde un `requirements.txt`):
        ```bash
        pip install PyQt6 bcrypt PyOpenGL # Agrega otras dependencias si son necesarias
        ```
        *Si no existe `requirements.txt`, instala manualmente: `pip install PyQt6 bcrypt`*

3.  **Inicializar la base de datos:** (Se ejecuta una vez o si se elimina el archivo `data/soundfresh.db`)
    ```bash
    python src/database/db_setup.py
    ```
4.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## Futuras Mejoras

*   Implementar la pestaña de "Ajustes".
*   Permitir modificar playlists existentes.
*   Añadir búsqueda dentro de la lista de canciones actual.
*   Mejorar la gestión de metadatos de las canciones (ID3 tags).
*   Refinar el manejo de errores y la experiencia de usuario.
*   Crear un archivo `requirements.txt`.
*   Empaquetar la aplicación para una distribución más sencilla (usando PyInstaller, cx_Freeze, etc.).
