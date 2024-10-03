import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = 'instance/diccionario.json'

def cargar_datos():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {"tablas": {}, "ejemplos": []}
    
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def guardar_datos(data):
    """Guarda datos en el archivo JSON."""
    try:
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error al guardar datos: {e}")

# Funciones para manejar ejemplos
def agregar_ejemplo(nombre, descripcion):
    """Agrega un nuevo ejemplo al archivo JSON."""
    data = cargar_datos()
    nuevo_id = len(data["ejemplos"]) + 1  # Generar un nuevo ID
    nuevo_ejemplo = {
        'id': nuevo_id,
        'nombre': nombre,
        'descripcion': descripcion
    }
    data["ejemplos"].append(nuevo_ejemplo)
    guardar_datos(data)

def obtener_ejemplos():
    """Devuelve la lista de ejemplos."""
    return cargar_datos()["ejemplos"]

def eliminar_ejemplo(ejemplo_id):
    """Elimina un ejemplo por ID."""
    data = cargar_datos()
    data["ejemplos"] = [e for e in data["ejemplos"] if e['id'] != ejemplo_id]
    guardar_datos(data)
