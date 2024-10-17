# servicios.py
import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('instance', 'diccionario.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {"tablas": {}, "ejemplos_tablas": []}
    
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def guardar_datos_json(data):
    """Guarda datos en el archivo JSON."""
    try:
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error al guardar datos: {e}")

# Funciones para manejar ejemplos
def agregar_ejemplo_tabla(nombre, descripcion):
    """Agrega un nuevo ejemplo al archivo JSON."""
    data = cargar_datos_json()
    nuevo_id = len(data["ejemplos_tablas"]) + 1  # Generar un nuevo ID
    nuevo_ejemplo = {
        'id': nuevo_id,
        'nombre': nombre,
        'descripcion': descripcion
    }
    data["ejemplos_tablas"].append(nuevo_ejemplo)
    guardar_datos_json(data)

def obtener_ejemplos_tablas():
    """Devuelve la lista de ejemplos."""
    return cargar_datos_json()["ejemplos_tablas"]

# services.py
def eliminar_ejemplo_tabla(ejemplo_id):
    """Elimina un ejemplo por ID."""    
    data = cargar_datos_json()
    # Imprimir ejemplos antes de la eliminación
    print("Ejemplos antes de eliminar:", data["ejemplos_tablas"])
    ejemplos_previos = len(data["ejemplos_tablas"])
    data["ejemplos_tablas"] = [e for e in data["ejemplos_tablas"] if e['id'] != ejemplo_id]
    guardar_datos_json(data)
    print("Ejemplos después de eliminar:", data["ejemplos_tablas"])  # Imprime después de eliminar
    return len(data["ejemplos_tablas"]) < ejemplos_previos  # Devuelve True si se eliminó un ejemplo

