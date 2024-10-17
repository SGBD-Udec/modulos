import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('instance', 'diccionario.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o retorna estructuras vacías."""
    if not os.path.exists(JSON_FILE_PATH):
        return {"tablas": {}, "ejemplos": []}
    
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
def agregar_ejemplo(nombre, descripcion):
    """Agrega un nuevo ejemplo al archivo JSON."""
    data = cargar_datos_json()
    nuevo_id = len(data["ejemplos"]) + 1  # Generar un nuevo ID
    nuevo_ejemplo = {
        'id': nuevo_id,
        'nombre': nombre,
        'descripcion': descripcion
    }
    data["ejemplos"].append(nuevo_ejemplo)
    guardar_datos_json(data)

def obtener_ejemplos():
    """Devuelve la lista de ejemplos."""
    return cargar_datos_json()["ejemplos"]

# models.py
def eliminar_ejemplo(ejemplo_id):
    """Elimina un ejemplo por ID desde el modelo."""    
    data = cargar_datos_json()
    # Puedes también imprimir aquí si lo deseas
    data["ejemplos"] = [e for e in data["ejemplos"] if e['id'] != ejemplo_id]
    guardar_datos_json(data)
    # Devuelve True si se eliminó un ejemplo
    return len(data["ejemplos"]) < len(data["ejemplos"])  # Aquí puedes verificar el cambio
