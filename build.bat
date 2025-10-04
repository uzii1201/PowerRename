@echo off
echo Compilando PowerRename.exe...
pyinstaller --onefile --noconsole main.py --name "PowerRename"
echo ✅ Compilación completa. El ejecutable está en la carpeta /dist.
pause