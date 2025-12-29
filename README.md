# md2word

Script sencillo en Python para convertir archivos Markdown (`.md`) a documentos de Word (`.dotx`) manteniendo estilos personalizados mediante una plantilla de referencia.

## Requisitos

- **Python 3.x**
- **Pandoc**: El script intentará descargarlo automáticamente si no lo encuentra.
- **Librerías**:
  ```cmd
  pip install pypandoc
  ```

## Instalación

1. Clona o descarga este repositorio.
2. Asegúrate de tener el archivo `reference.dotx` en la misma carpeta que `md2word.py`. Este archivo define los estilos (fuentes, márgenes, encabezados) del documento resultante.

## Uso

Ejecuta el script desde la terminal pasando la ruta del archivo, carpeta o una máscara de búsqueda.

### Ejemplos

- **Convertir un solo archivo:**
  ```cmd
  python md2word.py documento.md
  ```

- **Convertir todos los archivos de una carpeta:**
  ```cmd
  python md2word.py ruta/a/mi_carpeta/
  ```

- **Convertir usando una máscara (comodines):**
  ```cmd
  python md2word.py "informes/*.md"
  ```

> [!IMPORTANT]
> En Windows, usa comillas dobles cuando utilices asteriscos (`*`) en la ruta.

## Notas
- Los archivos `.dotx` generados se guardarán en el directorio actual de trabajo con el mismo nombre que el archivo original.
- Si necesitas cambiar el formato visual, edita el archivo `reference.dotx`.

## Colaboración
- Asistido por Google Antigravity