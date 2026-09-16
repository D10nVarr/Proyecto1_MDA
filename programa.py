import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                               QVBoxLayout, QPushButton, QLabel, QMessageBox, QFrame,
                               QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
                               QColorDialog, QFileDialog)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import configuraciones


class SettingsDialog(QDialog):
    def __init__(self, config_actual, idioma_actual, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(350, 300)

        self.config_actual = config_actual
        self.idioma_actual = idioma_actual

        self.t = {
            "es-ES": {
                "user": "Nombre de usuario:", "lang": "Idioma:", "theme": "Tema:",
                "font": "Tamaño de fuente:", "c_menu": "Color Menú:", "c_font": "Color Letra:",
                "photo": "Foto de perfil:", "btn_color": "Elegir Color",
                "btn_file": "Seleccionar Archivo", "btn_save": "Guardar Configuraciones",
                "temas": ["Claro", "Oscuro"]
            },
            "en-US": {
                "user": "Username:", "lang": "Language:", "theme": "Theme:",
                "font": "Font size:", "c_menu": "Menu Color:", "c_font": "Font Color:",
                "photo": "Profile picture:", "btn_color": "Choose Color",
                "btn_file": "Select File", "btn_save": "Save Settings",
                "temas": ["Light", "Dark"]
            }
        }

        self.setup_ui()

    def setup_ui(self):
        textos = self.t.get(self.idioma_actual, self.t["es-ES"])
        layout = QFormLayout(self)

        self.in_nombre = QLineEdit(self.config_actual.get("nombre_usuario", ""))

        self.in_idioma = QComboBox()
        self.in_idioma.addItems(["es-ES", "en-US"])
        self.in_idioma.setCurrentText(self.config_actual.get("idioma", "es-ES"))

        self.in_tema = QComboBox()
        self.in_tema.addItems(textos["temas"])

        tema_guardado = self.config_actual.get("tema", "Claro")
        if self.idioma_actual == "en-US":
            tema_visual = "Dark" if tema_guardado == "Oscuro" else "Light"
        else:
            tema_visual = tema_guardado
        self.in_tema.setCurrentText(tema_visual)

        self.in_fuente = QSpinBox()
        self.in_fuente.setRange(8, 48)
        self.in_fuente.setValue(self.config_actual.get("tamano_fuente", 14))

        self.btn_color_barra = QPushButton(textos["btn_color"])
        self.color_barra_val = self.config_actual.get("color_barra", "#cbd5e1")
        self.btn_color_barra.clicked.connect(self.elegir_color_barra)

        self.btn_color_letra = QPushButton(textos["btn_color"])
        self.color_letra_val = self.config_actual.get("color_letra", "#000000")
        self.btn_color_letra.clicked.connect(self.elegir_color_letra)

        self.btn_foto = QPushButton(textos["btn_file"])
        self.ruta_foto = self.config_actual.get("foto_perfil", "")
        self.btn_foto.clicked.connect(self.elegir_foto)

        btn_guardar = QPushButton(textos["btn_save"])
        btn_guardar.clicked.connect(self.accept)

        layout.addRow(textos["user"], self.in_nombre)
        layout.addRow(textos["lang"], self.in_idioma)
        layout.addRow(textos["theme"], self.in_tema)
        layout.addRow(textos["font"], self.in_fuente)
        layout.addRow(textos["c_menu"], self.btn_color_barra)
        layout.addRow(textos["c_font"], self.btn_color_letra)
        layout.addRow(textos["photo"], self.btn_foto)
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
        tema_seleccionado = self.in_tema.currentText()
        if tema_seleccionado == "Light": tema_seleccionado = "Claro"
        if tema_seleccionado == "Dark": tema_seleccionado = "Oscuro"

        return {
            "nombre_usuario": self.in_nombre.text(),
            "idioma": self.in_idioma.currentText(),
            "tema": tema_seleccionado,
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

        self.textos = {
            "es-ES": {
                "titulo": "MENÚ PRINCIPAL",
                "archivo": "ARCHIVO",
                "edicion": "EDICIÓN",
                "ver": "VER",
                "settings": "SETTINGS",
                "foto_vacia": "AQUÍ\n\nMUESTRA\n\nLA FOTO\n\nCARGADA",
                "frase": "Solo sé que no sé nada\n\"Sócrates\"",
                "lbl_nombre": "Nombre:",
                "lbl_idioma": "Idioma:"
            },
            "en-US": {
                "titulo": "MAIN MENU",
                "archivo": "FILE",
                "edicion": "EDIT",
                "ver": "VIEW",
                "settings": "SETTINGS",
                "foto_vacia": "HERE\n\nSHOWS\n\nLOADED\n\nPHOTO",
                "frase": "I know that I know nothing\n\"Socrates\"",
                "lbl_nombre": "Name:",
                "lbl_idioma": "Language:"
            }
        }

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

        self.config, mensaje_alerta = configuraciones.cargar_configuracion(ruta_seleccionada)

        # Validación si el usuario eligió No cargar o cerró la ventana de archivos
        if respuesta == QMessageBox.No:
            mensaje_alerta = "Se usarán las configuraciones por defecto del sistema."
        elif respuesta == QMessageBox.Yes and not ruta_seleccionada:
            mensaje_alerta = "Canceló la selección. Se usarán las configuraciones por defecto del sistema."

        self.setup_ui()
        self.actualizar_interfaz()

        if mensaje_alerta:
            QTimer.singleShot(100, lambda: QMessageBox.information(self, "Aviso de Carga", mensaje_alerta))

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_layout = QVBoxLayout(menu_frame)

        self.titulo_menu = QLabel()
        self.titulo_menu.setAlignment(Qt.AlignCenter)
        self.titulo_menu.setObjectName("botonFalso")

        self.btn_archivo = QPushButton()
        self.btn_edicion = QPushButton()
        self.btn_ver = QPushButton()
        self.btn_settings = QPushButton()

        self.btn_archivo.clicked.connect(lambda: self.accion_simulada(self.btn_archivo.text()))
        self.btn_edicion.clicked.connect(lambda: self.accion_simulada(self.btn_edicion.text()))
        self.btn_ver.clicked.connect(lambda: self.accion_simulada(self.btn_ver.text()))
        self.btn_settings.clicked.connect(self.abrir_settings)

        menu_layout.addWidget(self.titulo_menu)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(self.btn_archivo)
        menu_layout.addWidget(self.btn_edicion)
        menu_layout.addWidget(self.btn_ver)
        menu_layout.addWidget(self.btn_settings)
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

        envoltorio_foto = QVBoxLayout()
        envoltorio_foto.addStretch()
        envoltorio_foto.addWidget(self.foto_frame, 0, Qt.AlignCenter)
        envoltorio_foto.addStretch()

        info_frame = QFrame()
        info_frame.setObjectName("cardFrame")
        info_layout = QVBoxLayout(info_frame)

        self.lbl_frase = QLabel()
        self.lbl_frase.setAlignment(Qt.AlignCenter)

        self.lbl_nombre = QLabel()
        self.lbl_idioma = QLabel()

        self.lbl_nombre.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_idioma.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_nombre.setContentsMargins(20, 0, 0, 0)
        self.lbl_idioma.setContentsMargins(20, 0, 0, 0)

        info_layout.addStretch()
        info_layout.addWidget(self.lbl_frase)
        info_layout.addSpacing(40)
        info_layout.addWidget(self.lbl_nombre)
        info_layout.addWidget(self.lbl_idioma)
        info_layout.addStretch()

        content_layout.addLayout(envoltorio_foto, 1)
        content_layout.addWidget(info_frame, 2)

        main_layout.addWidget(menu_frame, 1)
        main_layout.addWidget(content_frame, 3)

    def actualizar_foto(self, texto_vacio):
        ruta_foto = self.config.get("foto_perfil", "")
        if ruta_foto and os.path.exists(ruta_foto):
            pixmap = QPixmap(ruta_foto)
            self.lbl_foto.setPixmap(pixmap)
        else:
            self.lbl_foto.clear()
            self.lbl_foto.setText(texto_vacio)

    def aplicar_estilos(self):
        tamano_fuente = self.config.get("tamano_fuente", 14)
        tema = self.config.get("tema", "Claro")

        color_barra_actual = self.config.get("color_barra", "#cbd5e1")
        color_texto_actual = self.config.get("color_letra", "#000000")

        if tema == "Oscuro":
            bg_main = "#000000"
            bg_menu = color_barra_actual
            bg_content = "#45474b"
            bg_card = "#000000"
            bg_btn = "#000000"
            btn_hover = "#1a1a1a"
        else:
            bg_main = "#ffffff"
            bg_menu = color_barra_actual
            bg_content = "#cbd5e1"
            bg_card = "#ffffff"
            bg_btn = "#ffffff"
            btn_hover = "#f1f5f9"

        estilos = f"""
        QMainWindow {{
            background-color: {bg_main};
        }}
        #menuFrame {{
            background-color: {bg_menu};
            border-radius: 15px;
            margin: 10px;
        }}
        #contentFrame {{
            background-color: {bg_content};
            border-radius: 15px;
            margin: 10px;
        }}
        #cardFrame, #fotoFrame {{
            background-color: {bg_card};
            border-radius: 15px;
            margin: 15px;
        }}
        #cardFrame {{ padding: 20px; }}

        QPushButton, #botonFalso {{
            background-color: {bg_btn};
            border-radius: 20px;
            padding: 12px;
            margin: 8px 15px;
            font-weight: bold;
            color: {color_texto_actual}; 
            border: none;
        }}
        QPushButton:hover {{
            background-color: {btn_hover};
        }}
        QLabel {{
            font-size: {tamano_fuente}px;
            color: {color_texto_actual}; 
        }}
        """
        self.setStyleSheet(estilos)

    def actualizar_interfaz(self):
        idioma_actual = self.config.get("idioma", "es-ES")
        t = self.textos.get(idioma_actual, self.textos["es-ES"])

        self.titulo_menu.setText(t["titulo"])
        self.btn_archivo.setText(t["archivo"])
        self.btn_edicion.setText(t["edicion"])
        self.btn_ver.setText(t["ver"])
        self.btn_settings.setText(t["settings"])
        self.lbl_frase.setText(t["frase"])

        self.lbl_nombre.setText(f"{t['lbl_nombre']} {self.config.get('nombre_usuario', '')}")
        self.lbl_idioma.setText(f"{t['lbl_idioma']} {idioma_actual}")

        self.actualizar_foto(t["foto_vacia"])
        self.aplicar_estilos()

    def accion_simulada(self, menu_nombre):
        QMessageBox.information(self, f"Aviso de Menú", f"Se está realizando la acción: {menu_nombre}")

    def abrir_settings(self):
        idioma_actual = self.config.get("idioma", "es-ES")
        dialogo = SettingsDialog(self.config, idioma_actual, self)

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