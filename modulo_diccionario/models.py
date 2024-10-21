import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('instance', 'diccionario.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {
            "ejemplos_tablas": [],
            "relaciones": [],
            "estadisticas": {
                "total_tablas": 0,
                "total_dml_operations": 0,
                "total_ddl_commands": 0
            }
        }
    
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def guardar_datos_json(data):
    """Guarda datos en el archivo JSON."""
    try:
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error al guardar datos: {e}")

# Funciones para manejar tablas
def agregar_tabla(nombre, descripcion, columnas):
    """Agrega una nueva tabla con sus columnas al archivo JSON."""
    data = cargar_datos_json()
    nuevo_id = len(data["ejemplos_tablas"]) + 1  # Generar un nuevo ID
    nueva_tabla = {
        'id': nuevo_id,
        'nombre': nombre,
        'descripcion': descripcion,
        'columnas': columnas,
        'registros': []  # Inicializar la clave 'registros' como una lista vacía
    }
    data["ejemplos_tablas"].append(nueva_tabla)
    guardar_datos_json(data)

    # Actualizar estadísticas
    data['estadisticas']['total_tablas'] += 1
    guardar_datos_json(data)

def obtener_tablas():
    """Devuelve la lista de tablas con columnas."""
    return cargar_datos_json()["ejemplos_tablas"]

def eliminar_tabla(nombre):
    """Elimina una tabla del archivo JSON."""
    data = cargar_datos_json()
    tablas = data["ejemplos_tablas"]
    
    # Filtrar la tabla que se desea eliminar
    nuevas_tablas = [tabla for tabla in tablas if tabla["nombre"] != nombre]
    
    if len(tablas) == len(nuevas_tablas):
        return False  # No se encontró la tabla para eliminar

    data["ejemplos_tablas"] = nuevas_tablas
    data['estadisticas']['total_tablas'] -= 1
    guardar_datos_json(data)
    return True

def incrementar_dml_operations():
    """Incrementa el contador de operaciones DML."""
    data = cargar_datos_json()
    data['estadisticas']['total_dml_operations'] += 1
    guardar_datos_json(data)

def incrementar_ddl_commands():
    """Incrementa el contador de comandos DDL."""
    data = cargar_datos_json()
    data['estadisticas']['total_ddl_commands'] += 1
    guardar_datos_json(data)

def obtener_estadisticas():
    """Devuelve las estadísticas actuales."""
    data = cargar_datos_json()
    return data['estadisticas']
