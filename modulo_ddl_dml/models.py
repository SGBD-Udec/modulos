import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('modulo_ddl_dml', 'data.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {"tablas": {}}
    
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
def agregar_tabla(nombre_tabla, columnas):
    """Agrega una nueva tabla al archivo JSON."""
    if not nombre_tabla or not columnas:
        raise ValueError("El nombre de la tabla y las columnas no pueden estar vacíos.")
    
    data = cargar_datos_json()
    nueva_tabla = {
        "columnas": columnas
    }
    data["tablas"][nombre_tabla] = nueva_tabla
    guardar_datos_json(data)

def buscar_tabla(nombre_tabla):
    """Busca una tabla por nombre."""
    data = cargar_datos_json()
    return data.get('tablas', {}).get(nombre_tabla, None)

def eliminar_tabla(nombre_tabla):
    """Elimina una tabla por nombre."""
    data = cargar_datos_json()
    if nombre_tabla in data.get('tablas', {}):
        del data['tablas'][nombre_tabla]
        guardar_datos_json(data)
        return True
    return False
