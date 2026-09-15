# configuraciones.py
import json
import os

ARCHIVO_CONFIG = "config.json"
ARCHIVO_TMP = "config_temporal.json"
ARCHIVO_BAK = "config.bak"


def cargar_configuracion():
    config_default = {
        "nombre_usuario": "Juan Pérez",
        "idioma": "es-ES",
        "tamano_fuente": 14,
        "color_barra": "#cbd5e1",
        "color_letra": "#000000",
        "foto_perfil": ""
    }

    if os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            config_cargada = json.load(archivo)
            config_final = config_default.copy()
            config_final.update(config_cargada)
            return config_final

    return config_default


def guardar_configuracion(datos):
    if os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as original:
            contenido_original = original.read()

        with open(ARCHIVO_BAK, "w", encoding="utf-8") as respaldo:
            respaldo.write(contenido_original)

    with open(ARCHIVO_TMP, "w", encoding="utf-8") as temporal:
        json.dump(
            datos,
            temporal,
            indent=4,
            ensure_ascii=False
        )

    os.replace(ARCHIVO_TMP, ARCHIVO_CONFIG)