#modulo_ddl_dml/services.py
from .models import buscar_tabla, insertar_registro, actualizar_registro, eliminar_registro,modificar_tabla, verificar_nombre_tabla_existente

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


def servicio_modificar_tabla(nombre_tabla_actual, nuevos_datos):

    try:
        modificar_tabla(nombre_tabla_actual, nuevos_datos)
    except ValueError as e:
        raise ValueError(str(e))