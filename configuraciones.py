import json
import os

ARCHIVO_CONFIG = "config.json"
ARCHIVO_BAK = "config.bak"


def obtener_valores_defecto():
    return {
        "nombre_usuario": "Juan Pérez",
        "idioma": "es-ES",
        "tema": "Claro",
        "tamano_fuente": 14,
        "color_barra": "#cbd5e1",
        "color_letra": "#000000",
        "foto_perfil": ""
    }


def cargar_configuracion(ruta_archivo=None):
    global ARCHIVO_CONFIG
    config_default = obtener_valores_defecto()

    if not ruta_archivo:
        return config_default, None

    ARCHIVO_CONFIG = ruta_archivo

    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            config_cargada = json.load(archivo)

            config_final = config_default.copy()
            config_final.update(config_cargada)
            return config_final, None

    except FileNotFoundError:
        mensaje = "El archivo no existe. Cargando configuración por defecto."
        return config_default, mensaje

    except json.JSONDecodeError:
        mensaje = "El archivo JSON está corrupto o es inválido. Cargando configuración por defecto."
        return config_default, mensaje

    except PermissionError:
        mensaje = "Archivo no apto por falta de permisos. Cargando configuración por defecto."
        return config_default, mensaje

    except UnicodeDecodeError:
        mensaje = "El archivo seleccionado no tiene formato de texto válido. Cargando configuración por defecto."
        return config_default, mensaje

    except Exception as e:
        mensaje = f"Error inesperado al cargar el archivo: {e}. Cargando configuración por defecto."
        return config_default, mensaje


def guardar_configuracion(datos):
    ruta_base = os.path.splitext(ARCHIVO_CONFIG)[0]
    archivo_tmp = f"{ruta_base}.tmp"

    try:
        if os.path.exists(ARCHIVO_CONFIG):
            with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as original:
                contenido_original = original.read()

            with open(ARCHIVO_BAK, "w", encoding="utf-8") as respaldo:
                respaldo.write(contenido_original)

        with open(archivo_tmp, "w", encoding="utf-8") as temporal:
            json.dump(
                datos,
                temporal,
                indent=4,
                ensure_ascii=False
            )

        os.replace(archivo_tmp, ARCHIVO_CONFIG)
        return True, "Configuración guardada exitosamente."

    except PermissionError:
        return False, "Error de permisos: No se tiene acceso de escritura para guardar el archivo."
    except Exception as e:
        return False, f"Error inesperado al guardar: {e}"