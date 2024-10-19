# servicios.py
from .models import cargar_datos_json, guardar_datos_json, agregar_tabla, obtener_tablas, eliminar_tabla, agregar_relacion, obtener_relaciones

# Servicio para agregar una tabla con columnas
def servicio_agregar_tabla(nombre, descripcion, columnas):
    if verificar_nombre_tabla_existente(nombre):  # Asegúrate de tener esta función
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
def servicio_eliminar_tabla(tabla_id):
    return eliminar_tabla(tabla_id)

# Servicio para agregar una relación entre tablas
def servicio_agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)

# Servicio para obtener todas las relaciones
def servicio_obtener_relaciones():
    return obtener_relaciones()

