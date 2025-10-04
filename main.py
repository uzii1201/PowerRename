import sys, os, re, webbrowser
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog,
    QCheckBox, QMessageBox, QLabel, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class FileTable(QTableWidget):
    """Tabla con soporte de arrastrar y soltar archivos."""
    def __init__(self, parent=None):
        super().__init__(0, 2, parent)
        self.setHorizontalHeaderLabels(["Original", "Nuevo"])
        self.setAcceptDrops(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.parent().add_files(paths)
            event.acceptProposedAction()

class PowerRenameClone(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerRename by @uzii")
        self.resize(900, 600)

        layout = QVBoxLayout()

        # Inputs de búsqueda/reemplazo
        input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar...")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Reemplazar por...")
        self.regex_checkbox = QCheckBox("Usar Regex")
        self.ignore_ext_checkbox = QCheckBox("Ignorar extensión")
        input_layout.addWidget(QLabel("Buscar:"))
        input_layout.addWidget(self.search_input)
        input_layout.addWidget(QLabel("Reemplazar:"))
        input_layout.addWidget(self.replace_input)
        input_layout.addWidget(self.regex_checkbox)
        input_layout.addWidget(self.ignore_ext_checkbox)

        layout.addLayout(input_layout)

        # Filtro por extensión
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Ejemplo: .jpg,.png,.txt (vacío = todos)")
        filter_layout.addWidget(QLabel("Filtrar extensiones:"))
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        # Tabla de vista previa
        self.table = FileTable(self)
        layout.addWidget(self.table)

        # Botones principales
        btn_layout = QHBoxLayout()
        btn_load = QPushButton("Cargar archivos")
        btn_preview = QPushButton("Vista previa")
        btn_rename = QPushButton("Renombrar")

        btn_load.clicked.connect(self.load_files)
        btn_preview.clicked.connect(self.preview)
        btn_rename.clicked.connect(self.rename_files)

        btn_layout.addWidget(btn_load)
        btn_layout.addWidget(btn_preview)
        btn_layout.addWidget(btn_rename)
        layout.addLayout(btn_layout)

        # Botón a GitHub
        github_btn = QPushButton("GitHub: @uzii1201")
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/uzii1201"))
        layout.addWidget(github_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.files = []

    def add_files(self, paths):
        """Agrega archivos a la lista con filtro de extensiones."""
        filter_exts = [ext.strip().lower() for ext in self.filter_input.text().split(",") if ext.strip()]
        for f in paths:
            if os.path.isfile(f):
                ext = os.path.splitext(f)[1].lower()
                if not filter_exts or ext in filter_exts:
                    self.files.append(f)

        self.refresh_table()

    def load_files(self):
        """Diálogo para seleccionar archivos."""
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos")
        if files:
            self.add_files(files)

    def refresh_table(self):
        """Refresca la tabla con los archivos actuales."""
        self.table.setRowCount(len(self.files))
        for i, f in enumerate(self.files):
            self.table.setItem(i, 0, QTableWidgetItem(os.path.basename(f)))
            self.table.setItem(i, 1, QTableWidgetItem(""))

    def preview(self):
        """Genera vista previa con resaltado."""
        if not self.files:
            QMessageBox.warning(self, "Advertencia", "No hay archivos cargados.")
            return

        pattern = self.search_input.text()
        replace = self.replace_input.text()
        use_regex = self.regex_checkbox.isChecked()
        ignore_ext = self.ignore_ext_checkbox.isChecked()

        for i, f in enumerate(self.files):
            name = os.path.basename(f)
            base, ext = os.path.splitext(name)

            target = base if ignore_ext else name
            new_target = target

            if use_regex:
                try:
                    new_target = re.sub(pattern, replace, target)
                except re.error:
                    new_target = "[Regex inválida]"
            else:
                new_target = target.replace(pattern, replace)

            new_name = new_target + (ext if ignore_ext else "")
            item = QTableWidgetItem(new_name)

            # Resaltar si hay cambio
            if new_name != name:
                item.setForeground(QColor("green"))
                self.table.item(i, 0).setForeground(QColor("red"))

            self.table.setItem(i, 1, item)

    def rename_files(self):
        """Aplica el renombrado."""
        if not self.files:
            QMessageBox.warning(self, "Advertencia", "No hay archivos para renombrar.")
            return

        cambios = []
        for i, f in enumerate(self.files):
            new_name = self.table.item(i, 1).text()
            if new_name and new_name != os.path.basename(f):
                new_path = os.path.join(os.path.dirname(f), new_name)
                cambios.append((f, new_path))

        if not cambios:
            QMessageBox.information(self, "Info", "No hay cambios para aplicar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar", f"¿Aplicar cambios a {len(cambios)} archivos?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.No:
            return

        for viejo, nuevo in cambios:
            try:
                os.rename(viejo, nuevo)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo renombrar:\n{viejo}\n{e}")

        QMessageBox.information(self, "Éxito", "Renombrado completo.")
        self.files = []
        self.table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 🎨 Forzar modo oscuro
    dark_stylesheet = """
        QWidget { background-color: #121212; color: #ffffff; }
        QLineEdit, QTableWidget, QTableWidgetItem {
            background-color: #1e1e1e; color: #ffffff; border: 1px solid #333333;
        }
        QPushButton {
            background-color: #2d2d2d; color: #ffffff; border: 1px solid #444444;
            padding: 6px; border-radius: 4px;
        }
        QPushButton:hover { background-color: #3c3c3c; }
        QHeaderView::section {
            background-color: #2d2d2d; color: #ffffff; padding: 4px;
        }
        QCheckBox { color: #ffffff; }
        QLabel { color: #bbbbbb; }
    """
    app.setStyleSheet(dark_stylesheet)

    win = PowerRenameClone()
    win.show()
    sys.exit(app.exec())
