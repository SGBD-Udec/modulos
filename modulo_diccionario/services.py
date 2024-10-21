#modulo_diccionario/servicios.py
import json
from .models import cargar_datos_json, guardar_datos_json, agregar_tabla, obtener_tablas, eliminar_tabla

# Servicio para agregar una tabla con columnas
def servicio_agregar_tabla(nombre, descripcion, columnas):
    if verificar_nombre_tabla_existente(nombre):
        return False  # Nombre ya existe, no se puede agregar
    agregar_tabla(nombre, descripcion, columnas)
    actualizar_contadores_ddl()  # Actualiza el contador de comandos DDL
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
    actualizar_contadores_dml()  # Actualiza el contador de operaciones DML

# Obtener estadísticas
def obtener_estadisticas():
    try:
        with open('instance/diccionario.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "El archivo JSON no se encontró."}

<<<<<<< HEAD
# Servicio para obtener todas las relaciones
def servicio_obtener_relaciones():
    return obtener_relaciones()

=======
    tables_count = len(data.get('ejemplos_tablas', []))  # Número de tablas
    columns_count = sum(len(table['columnas']) for table in data.get('ejemplos_tablas', []))  # Total de columnas

    # Contadores DML y DDL
    total_dml_operations = data.get('estadisticas', {}).get('totalDmlOperations', 0)
    total_ddl_commands = data.get('estadisticas', {}).get('totalDdlCommands', 0)

    return {
        "tablesCount": tables_count,
        "columnsCount": columns_count,
        "totalDmlOperations": total_dml_operations,
        "totalDdlCommands": total_ddl_commands,
    }
# Funciones para actualizar contadores
def actualizar_contadores_dml():
    try:
        with open('instance/diccionario.json', 'r') as f:
            data = json.load(f)

        data.setdefault('estadisticas', {})  # Asegúrate de que 'estadisticas' exista
        data['estadisticas']['totalDmlOperations'] = data['estadisticas'].get('totalDmlOperations', 0) + 1

        with open('instance/diccionario.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al actualizar contadores DML: {e}")

def actualizar_contadores_ddl():
    try:
        with open('instance/diccionario.json', 'r') as f:
            data = json.load(f)

        data.setdefault('estadisticas', {})  # Asegúrate de que 'estadisticas' exista
        data['estadisticas']['totalDdlCommands'] = data['estadisticas'].get('totalDdlCommands', 0) + 1

        with open('instance/diccionario.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al actualizar contadores DDL: {e}")
>>>>>>> Pruebaunion
