@echo off
echo Instalando dependencias para md2word...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error al instalar las dependencias de Python.
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo Verificando instalador de Pandoc (MSI)...
if not exist "pandoc-3.8.3-windows-x86_64.msi" (
    echo Descargando Pandoc 3.8.3...
    curl -L --ssl-no-revoke -o "pandoc-3.8.3-windows-x86_64.msi" "https://github.com/jgm/pandoc/releases/download/3.8.3/pandoc-3.8.3-windows-x86_64.msi"
    if %ERRORLEVEL% NEQ 0 (
        echo Error al descargar Pandoc.
    )
)

if exist "pandoc-3.8.3-windows-x86_64.msi" (
    echo Instalando Pandoc desde MSI...
    msiexec.exe /i "pandoc-3.8.3-windows-x86_64.msi" /quiet /norestart
    if %ERRORLEVEL% NEQ 0 (
        echo Advertencia: La instalacion del MSI fallo o requiere privilegios.
    ) else (
        echo Pandoc instalado desde MSI correctamente.
    )
) else (
    echo No se pudo obtener el instalador MSI.
)

echo.
echo Verificando Pandoc via Python...
python -c "import pypandoc; pypandoc.ensure_pandoc_installed()"
if %ERRORLEVEL% NEQ 0 (
    echo Error al asegurar la instalacion de Pandoc.
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo Instalacion completada con exito.
pause
