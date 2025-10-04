@echo off
setlocal

:: Ruta absoluta al EXE (misma carpeta que este BAT)
set EXE_PATH=%~dp0PowerRename.exe

:: Verificar si existe el EXE
if not exist "%EXE_PATH%" (
    echo No se encontró PowerRename.exe en la misma carpeta.
    pause
    exit /b
)

:: Agregar al menú contextual para archivos
reg add "HKCR\*\shell\PowerRename" /ve /d "PowerRename by @uzii" /f
reg add "HKCR\*\shell\PowerRename\command" /ve /d "\"%EXE_PATH%\" \"%%1\"" /f

:: Agregar al menú contextual para carpetas
reg add "HKCR\Directory\shell\PowerRename" /ve /d "PowerRename by @uzii" /f
reg add "HKCR\Directory\shell\PowerRename\command" /ve /d "\"%EXE_PATH%\" \"%%1\"" /f

echo.
echo PowerRename se instalo en el menu contextual de Windows.
pause
