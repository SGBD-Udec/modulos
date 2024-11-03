# modulo_diccionario/models.py
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

            }
        }
    
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

        # Actualizar el conteo de tablas en "estadisticas"
    data["estadisticas"]["total_tablas"] = len(data.get("ejemplos_tablas", []))
    return data

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

    # Actualizar estadísticas al agregar una nueva tabla
    data["estadisticas"]["total_tablas"] += 1

    guardar_datos_json(data)

def obtener_tablas():
    """Devuelve la lista de tablas con columnas."""
    return cargar_datos_json()["ejemplos_tablas"]

def obtener_columnas_de_tabla(nombre_tabla):
    """Devuelve las columnas de una tabla específica."""
    tablas = obtener_tablas()
    for tabla in tablas:
        if tabla['nombre'] == nombre_tabla:
            return tabla.get('columnas', [])
    return []


def agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    data = cargar_datos_json()
    nueva_relacion = {
        "tabla_origen": tabla_origen,
        "columna_origen": columna_origen,
        "tabla_destino": tabla_destino,
        "columna_destino": columna_destino,
        "tipo_relacion": tipo_relacion
    }

    # Asegúrate de que 'relaciones' esté inicializado
    if "relaciones" not in data:
        data["relaciones"] = []

    data["relaciones"].append(nueva_relacion)

    # Intenta guardar los datos, maneja la excepción
    try:
        guardar_datos_json(data)
    except Exception as e:
        print(f"Error al guardar la relación: {e}")
        raise  # Vuelve a lanzar la excepción para que sea manejada en el endpoint

# Función para obtener todas las relaciones
def obtener_relaciones():
    data = cargar_datos_json()
    return data.get("relaciones", [])

# Función para eliminar una relación
def eliminar_relacion(tabla_origen, tabla_destino):
    try:
        data = cargar_datos_json()
        relaciones = data.get("relaciones", [])
        
        # Filtrar las relaciones que no coincidan con los parámetros dados
        relaciones_filtradas = [r for r in relaciones if not (r["tabla_origen"] == tabla_origen and r["tabla_destino"] == tabla_destino)]
        
        data["relaciones"] = relaciones_filtradas  # Actualiza las relaciones en el JSON
        guardar_datos_json(data)  # Guarda los cambios
        return True
    except Exception as e:
        print(f"Error al eliminar relación: {e}")
        raise  # Vuelve a lanzar la excepción para que sea manejada en el endpoint
