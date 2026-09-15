import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                               QVBoxLayout, QPushButton, QLabel, QMessageBox, QFrame,
                               QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
                               QColorDialog, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import configuraciones


class SettingsDialog(QDialog):
    def __init__(self, config_actual, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(350, 250)

        self.config_actual = config_actual
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.in_nombre = QLineEdit(self.config_actual.get("nombre_usuario", ""))

        self.in_idioma = QComboBox()
        self.in_idioma.addItems(["es-ES","en-US"])
        self.in_idioma.setCurrentText(self.config_actual.get("idioma", "es-ES"))

        self.in_fuente = QSpinBox()
        self.in_fuente.setRange(8, 48)
        self.in_fuente.setValue(self.config_actual.get("tamano_fuente", 14))

        self.btn_color_barra = QPushButton("Elegir Color")
        self.color_barra_val = self.config_actual.get("color_barra", "#cbd5e1")
        self.btn_color_barra.clicked.connect(self.elegir_color_barra)

        self.btn_color_letra = QPushButton("Elegir Color")
        self.color_letra_val = self.config_actual.get("color_letra", "#000000")
        self.btn_color_letra.clicked.connect(self.elegir_color_letra)

        self.btn_foto = QPushButton("Seleccionar Archivo")
        self.ruta_foto = self.config_actual.get("foto_perfil", "")
        self.btn_foto.clicked.connect(self.elegir_foto)

        btn_guardar = QPushButton("Guardar Configuraciones")
        btn_guardar.clicked.connect(self.accept)

        layout.addRow("Nombre de usuario:", self.in_nombre)
        layout.addRow("Idioma:", self.in_idioma)
        layout.addRow("Tamaño de fuente:", self.in_fuente)
        layout.addRow("Color Menú:", self.btn_color_barra)
        layout.addRow("Color Letra:", self.btn_color_letra)
        layout.addRow("Foto de perfil:", self.btn_foto)
        layout.addRow("", btn_guardar)

    def elegir_color_barra(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_barra_val = color.name()

    def elegir_color_letra(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_letra_val = color.name()

    def elegir_foto(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Imágenes (*.png *.jpg *.jpeg)")
        if ruta:
            self.ruta_foto = ruta

    def obtener_datos(self):
        return {
            "nombre_usuario": self.in_nombre.text(),
            "idioma": self.in_idioma.currentText(),
            "tamano_fuente": self.in_fuente.value(),
            "color_barra": self.color_barra_val,
            "color_letra": self.color_letra_val,
            "foto_perfil": self.ruta_foto
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto 1 - Manejo de Archivos")
        self.resize(850, 500)

        # 1. Consultar al usuario
        respuesta = QMessageBox.question(
            self,
            "Carga Inicial",
            "¿Desea cargar un archivo JSON de configuración externo?\n\n(De lo contrario se usaran valores por defecto).",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        ruta_seleccionada = None

        if respuesta == QMessageBox.Yes:
            ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo de Configuración", "",
                                                  "Archivos JSON (*.json)")
            if ruta:
                ruta_seleccionada = ruta

        self.config = configuraciones.cargar_configuracion(ruta_seleccionada)

        self.setup_ui()
        self.aplicar_estilos()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_layout = QVBoxLayout(menu_frame)

        titulo_menu = QLabel("MENÚ PRINCIPAL")
        titulo_menu.setAlignment(Qt.AlignCenter)
        titulo_menu.setObjectName("botonFalso")

        btn_archivo = QPushButton("ARCHIVO")
        btn_edicion = QPushButton("EDICIÓN")
        btn_ver = QPushButton("VER")
        btn_settings = QPushButton("SETTINGS")

        btn_archivo.clicked.connect(lambda: self.accion_simulada("Archivo"))
        btn_edicion.clicked.connect(lambda: self.accion_simulada("Edición"))
        btn_ver.clicked.connect(lambda: self.accion_simulada("Ver"))
        btn_settings.clicked.connect(self.abrir_settings)

        menu_layout.addWidget(titulo_menu)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(btn_archivo)
        menu_layout.addWidget(btn_edicion)
        menu_layout.addWidget(btn_ver)
        menu_layout.addWidget(btn_settings)
        menu_layout.addStretch()

        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QHBoxLayout(content_frame)

        self.foto_frame = QFrame()
        self.foto_frame.setObjectName("fotoFrame")
        self.foto_frame.setFixedSize(220, 260)

        foto_layout = QVBoxLayout(self.foto_frame)
        foto_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_foto = QLabel()
        self.lbl_foto.setAlignment(Qt.AlignCenter)
        self.lbl_foto.setScaledContents(True)
        self.lbl_foto.setStyleSheet("border-radius: 15px;")
        foto_layout.addWidget(self.lbl_foto)

        self.actualizar_foto()

        envoltorio_foto = QVBoxLayout()
        envoltorio_foto.addStretch()
        envoltorio_foto.addWidget(self.foto_frame, 0, Qt.AlignCenter)
        envoltorio_foto.addStretch()

        info_frame = QFrame()
        info_frame.setObjectName("cardFrame")
        info_layout = QVBoxLayout(info_frame)

        lbl_frase = QLabel("Solo se que no se nada\n\"Sócrates\"")
        lbl_frase.setAlignment(Qt.AlignCenter)

        self.lbl_nombre = QLabel(f"Nombre: {self.config.get('nombre_usuario', '')}")
        self.lbl_idioma = QLabel(f"Idioma: {self.config.get('idioma', '')}")

        self.lbl_nombre.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_idioma.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_nombre.setContentsMargins(20, 0, 0, 0)
        self.lbl_idioma.setContentsMargins(20, 0, 0, 0)

        info_layout.addStretch()
        info_layout.addWidget(lbl_frase)
        info_layout.addSpacing(40)
        info_layout.addWidget(self.lbl_nombre)
        info_layout.addWidget(self.lbl_idioma)
        info_layout.addStretch()

        content_layout.addLayout(envoltorio_foto, 1)
        content_layout.addWidget(info_frame, 2)

        main_layout.addWidget(menu_frame, 1)
        main_layout.addWidget(content_frame, 3)

    def actualizar_foto(self):
        ruta_foto = self.config.get("foto_perfil", "")

        if ruta_foto and os.path.exists(ruta_foto):
            pixmap = QPixmap(ruta_foto)
            self.lbl_foto.setPixmap(pixmap)
        else:
            self.lbl_foto.clear()
            self.lbl_foto.setText("AQUÍ\n\nMUESTRA\n\nLA FOTO\n\nCARGADA")

    def aplicar_estilos(self):
        color_texto_actual = self.config.get("color_letra", "#000000")
        color_barra_actual = self.config.get("color_barra", "#cbd5e1")
        tamano_fuente = self.config.get("tamano_fuente", 14)

        estilos = f"""
        QMainWindow {{
            background-color: #ffffff;
        }}
        #menuFrame {{
            background-color: {color_barra_actual};
            border-radius: 15px;
            margin: 10px;
        }}
        #contentFrame {{
            background-color: #cbd5e1;
            border-radius: 15px;
            margin: 10px;
        }}
        #cardFrame {{
            background-color: #ffffff;
            border-radius: 15px;
            margin: 15px;
            padding: 20px;
        }}
        #fotoFrame {{
            background-color: #ffffff;
            border-radius: 15px;
            margin: 15px;
        }}
        QPushButton, #botonFalso {{
            background-color: #ffffff;
            border-radius: 20px;
            padding: 12px;
            margin: 8px 15px;
            font-weight: bold;
            color: #333333;
            border: none;
        }}
        QPushButton:hover {{
            background-color: #f1f5f9;
        }}
        QLabel {{
            font-size: {tamano_fuente}px;
            color: {color_texto_actual};
        }}
        """
        self.setStyleSheet(estilos)

    def actualizar_interfaz(self):
        self.lbl_nombre.setText(f"Nombre: {self.config.get('nombre_usuario', '')}")
        self.lbl_idioma.setText(f"Idioma: {self.config.get('idioma', '')}")
        self.actualizar_foto()
        self.aplicar_estilos()

    def accion_simulada(self, menu_nombre):
        QMessageBox.information(self, f"Menú {menu_nombre}", f"Se está realizando la acción: {menu_nombre}")

    def abrir_settings(self):
        dialogo = SettingsDialog(self.config, self)
        if dialogo.exec():
            nueva_config = dialogo.obtener_datos()
            exito, mensaje = configuraciones.guardar_configuracion(nueva_config)

            if exito:
                self.config = nueva_config
                self.actualizar_interfaz()
                QMessageBox.information(self, "Éxito", mensaje)
            else:
                QMessageBox.warning(self, "Error al guardar", mensaje)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())