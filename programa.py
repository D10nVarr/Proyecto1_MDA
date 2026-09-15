import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                               QVBoxLayout, QPushButton, QLabel, QMessageBox, QFrame)
from PySide6.QtCore import Qt
import configuraciones


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto 1 - Manejo de Archivos")
        self.resize(850, 500)

        self.config = configuraciones.cargar_configuracion()

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

        foto_frame = QFrame()
        foto_frame.setObjectName("cardFrame")
        foto_layout = QVBoxLayout(foto_frame)
        self.lbl_foto = QLabel("AQUÍ\n\nMUESTRA\n\nLA FOTO\n\nCARGADA")
        self.lbl_foto.setAlignment(Qt.AlignCenter)
        foto_layout.addWidget(self.lbl_foto)

        info_frame = QFrame()
        info_frame.setObjectName("cardFrame")
        info_layout = QVBoxLayout(info_frame)

        lbl_frase = QLabel("Solo se que no se nada\n\"Sócrates\"")
        lbl_frase.setAlignment(Qt.AlignCenter)

        nombre = self.config.get('nombre_usuario', 'Sin definir')
        idioma = self.config.get('idioma', 'Sin definir')

        self.lbl_nombre = QLabel(f"Nombre: ({nombre})")
        self.lbl_idioma = QLabel(f"Idioma: ({idioma})")

        info_layout.addWidget(lbl_frase)
        info_layout.addSpacing(40)
        info_layout.addWidget(self.lbl_nombre)
        info_layout.addWidget(self.lbl_idioma)
        info_layout.addStretch()

        content_layout.addWidget(foto_frame)
        content_layout.addWidget(info_frame)

        main_layout.addWidget(menu_frame, 1)
        main_layout.addWidget(content_frame, 3)

    def aplicar_estilos(self):#temporal pa pruebas
        color_texto_actual = self.config.get("color_letra", "#000000")

        estilos = f"""
        QMainWindow {{
            background-color: #ffffff;
        }}
        #menuFrame, #contentFrame {{
            background-color: #cbd5e1; /* Gris azulado base */
            border-radius: 15px;
            margin: 10px;
        }}
        #cardFrame {{
            background-color: #ffffff;
            border-radius: 15px;
            margin: 15px;
            padding: 20px;
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
            font-size: 14px;
            color: {color_texto_actual};
        }}
        """
        self.setStyleSheet(estilos)

    def accion_simulada(self, menu_nombre):
        QMessageBox.information(self, f"Menú {menu_nombre}", f"Se está realizando la acción: {menu_nombre}")

    def abrir_settings(self):
        QMessageBox.information(self, "Settings",
                                "Aquí se abrirá la nueva ventana de configuraciones en la siguiente fase.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())