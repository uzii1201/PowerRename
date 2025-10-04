# PowerRename by @uzii

Una herramienta ligera para Windows que permite renombrar archivos y carpetas de manera masiva, inspirada en Microsoft PowerToys, desarrollada en Python con PySide6.

---

## Características

* Soporte de arrastrar y soltar archivos y carpetas
* Vista previa de los archivos antes de aplicar los cambios
* Soporte para expresiones regulares (regex) para renombrado avanzado
* Opción de ignorar la extensión de los archivos durante el renombrado
* Filtrado por extensiones de archivo
* Interfaz en modo oscuro
* Integración con el menú contextual de Windows (clic derecho)
* Empaquetado como un único ejecutable `.exe` (no requiere instalación de Python si se compila)

---

## Capturas

Incluye capturas de pantalla de la aplicación en acción dentro de la carpeta `screenshots/` del repositorio.

```markdown
![Vista principal](screenshots/main_window.png)
![Vista previa de renombrado](screenshots/preview.png)
```

---

## Instalación y Uso(Dos opciones A/B)

### A Desda codigo fuente

1. Clonar o descargar el repositorio:
git clone https://github.com/uzii1201/PowerRename.git

2. Instalar dependencias:

pip install -r requirements.txt

3. Ejecutar la aplicación:
python main.py

4. Arrastrar los archivos o carpetas que se quieran renombrar.
5. Configurar búsqueda, reemplazo, filtros y opciones de renombrado.
6. Vista previa de los cambios y, si todo está correcto, aplicar el renombrado.

### B Generar el ejecutable `.exe`

1. Ejecutar el script de construcción:
build.bat
2. El archivo ejecutable se generará en la carpeta `dist/`.
3. Ahora se puede ejecutar la app directamente desde `dist/` o usar el menú contextual de Windows (`install_context.bat`).

---

## Tecnologías usadas

* **Python 3.13**
* **PySide6** (interfaz gráfica)
* **PyInstaller** (para empaquetar como `.exe`)

---

## Autor

**@uzii**

* GitHub: [https://github.com/uzii1201](https://github.com/uzii1201)

---

## Licencia

Este proyecto es solo para fines educativos y demostrativos.
Puedes usarlo, modificarlo y compartirlo bajo los términos de la licencia **MIT**.
