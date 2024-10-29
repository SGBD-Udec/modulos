#modulo_diccionario/servicios.py
import json
from .models import cargar_datos_json, guardar_datos_json, agregar_tabla, obtener_tablas, eliminar_tabla

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

# Servicio para eliminar una tabla
def servicio_eliminar_tabla(nombre):
    eliminar_tabla(nombre)




