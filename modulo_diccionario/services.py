#modulo_diccionario/servicios.py
import json
from .models import cargar_datos_json, guardar_datos_json, agregar_tabla, obtener_tablas, obtener_columnas_de_tabla, agregar_relacion, obtener_relaciones, eliminar_relacion 

# Servicio para agregar una tabla con columnas
def servicio_agregar_tabla(nombre, descripcion, columnas):
    if verificar_nombre_tabla_existente(nombre):
        return False  # Nombre ya existe, no se puede agregar
    agregar_tabla(nombre, descripcion, columnas)
    return True  # Se agregó con éxito

def verificar_nombre_tabla_existente(nombre):
    tablas = obtener_tablas()  # Esta función debe devolver todas las tablas
    return any(tabla['nombre'] == nombre for tabla in tablas)  # Compara el nombre

# Servicio para obtener todas las tablas
def servicio_obtener_tablas():
    return obtener_tablas()

def servicio_obtener_columnas(nombre_tabla):
    return obtener_columnas_de_tabla(nombre_tabla)

def crear_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    """Crea una nueva relación entre tablas."""
    agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)

def listar_relaciones():
    """Obtiene todas las relaciones entre tablas."""
    return obtener_relaciones()

def borrar_relacion(tabla_origen, tabla_destino):
    """Elimina una relación entre tablas."""
    eliminar_relacion(tabla_origen, tabla_destino)




