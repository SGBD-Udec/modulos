#modulo_ddl_dml/services.py
from .models import buscar_tabla, insertar_registro, actualizar_registro, eliminar_registro, agregar_relacion, obtener_relaciones, eliminar_relacion

# Función para insertar un nuevo registro en una tabla
def agregar_registro(nombre_tabla, registro):
    tabla = buscar_tabla(nombre_tabla)
    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")
    
    insertar_registro(nombre_tabla, registro)

# Función para actualizar registros en una tabla
def modificar_registro(nombre_tabla, campos, campo_condicion, valor_condicion):
    registros_actualizados = actualizar_registro(nombre_tabla, campos, campo_condicion, valor_condicion)
    if registros_actualizados == 0:
        raise ValueError("No se encontraron registros que coincidan con la condición.")

# Función para eliminar registros en una tabla
def borrar_registro(nombre_tabla, campo_condicion, valor_condicion):
    eliminar_registro(nombre_tabla, campo_condicion, valor_condicion)

# ---- Nuevas Funciones para Relaciones ---- #

def crear_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    """Crea una nueva relación entre tablas."""
    agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)

def listar_relaciones():
    """Obtiene todas las relaciones entre tablas."""
    return obtener_relaciones()

def borrar_relacion(tabla_origen, tabla_destino):
    """Elimina una relación entre tablas."""
    eliminar_relacion(tabla_origen, tabla_destino)
