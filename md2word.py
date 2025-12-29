import os
import sys
import glob
import pypandoc

# Carpeta donde está el script Python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constante con la ruta al archivo de referencia
REFERENCE_DOCX = os.path.join(SCRIPT_DIR, "reference.dotx")

def convert_md_to_docx(input_path):
    """
    Convierte un archivo .md a .dotx usando pypandoc con estilos definidos en reference.dotx.
    """
    if not input_path.lower().endswith('.md'):
        print(f"Saltando {input_path}: No es un archivo .md")
        return

    file_name = os.path.basename(input_path)
    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(os.getcwd(), base_name + '.dotx')
    
    try:
        print(f"Convirtiendo: {input_path} -> {output_path}")
        pypandoc.convert_file(
            input_path,
            'docx',
            outputfile=output_path,
            extra_args=['--reference-doc', REFERENCE_DOCX]
        )
        print(f"¡Éxito! Archivo guardado en: {output_path}")
    except Exception as e:
        print(f"Error al convertir {input_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python md2word.py <path_o_mascara>")
        print("Ejemplos:")
        print("  python md2word.py archivo.md")
        print("  python md2word.py carpeta/")
        print("  python md2word.py \"c:\\tmp\\imp*.md\"")
        sys.exit(1)

    path_arg = sys.argv[1]

    # Asegurar que pandoc esté disponible
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("Pandoc no encontrado. Intentando descargar...")
        try:
            pypandoc.download_pandoc()
            print("Pandoc descargado correctamente.")
        except Exception as e:
            print(f"Error al descargar Pandoc: {e}")
            print("Por favor, instala Pandoc manualmente: https://pandoc.org/installing.html")
            sys.exit(1)

    files_to_convert = []

    # Caso 1: Es una carpeta
    if os.path.isdir(path_arg):
        search_pattern = os.path.join(path_arg, "*.md")
        files_to_convert = glob.glob(search_pattern)
    # Caso 2: Es una máscara o archivo individual
    else:
        files_to_convert = glob.glob(path_arg)

    if not files_to_convert:
        print(f"No se encontraron archivos .md para el path: {path_arg}")
        return

    for file_path in files_to_convert:
        if os.path.isfile(file_path):
            convert_md_to_convert = os.path.abspath(file_path)
            convert_md_to_docx(convert_md_to_convert)

if __name__ == "__main__":
    main()
