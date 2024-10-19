import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('instance', 'diccionario.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {"ejemplos_tablas": [], "relaciones": []}
    
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
        'columnas': columnas
    }
    data["ejemplos_tablas"].append(nueva_tabla)
    guardar_datos_json(data)

def obtener_tablas():
    """Devuelve la lista de tablas con columnas."""
    return cargar_datos_json()["ejemplos_tablas"]

def eliminar_tabla(tabla_id):
    """Elimina una tabla por ID."""    
    data = cargar_datos_json()
    tablas_previas = len(data["ejemplos_tablas"])
    data["ejemplos_tablas"] = [t for t in data["ejemplos_tablas"] if t['id'] != tabla_id]
    guardar_datos_json(data)
    return len(data["ejemplos_tablas"]) < tablas_previas

def agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    """Agrega una relación entre tablas."""
    data = cargar_datos_json()
    nueva_relacion = {
        "tabla_origen": tabla_origen,
        "columna_origen": columna_origen,
        "tabla_destino": tabla_destino,
        "columna_destino": columna_destino,
        "tipo_relacion": tipo_relacion
    }
    data["relaciones"].append(nueva_relacion)
    guardar_datos_json(data)

def obtener_relaciones():
    """Devuelve la lista de relaciones entre tablas."""
    return cargar_datos_json()["relaciones"]

