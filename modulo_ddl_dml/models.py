import json
import os

# Ruta del archivo JSON
JSON_FILE_PATH = os.path.join('modulo_ddl_dml', 'data.json')

def cargar_datos_json():
    """Carga datos desde el archivo JSON o inicializa una estructura vacía."""
    print("Cargando datos JSON...")  # Mensaje de depuración
    if not os.path.exists(JSON_FILE_PATH):
        inicializar_archivo_json()
    
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)
        print(data)  # Imprime los datos cargados para depuración
        return data

def inicializar_archivo_json():
    """Inicializa el archivo JSON con la estructura básica."""
    if not os.path.exists('modulo_ddl_dml'):
        os.makedirs('modulo_ddl_dml')  # Asegúrate de que el directorio exista
        print("Directorio 'modulo_ddl_dml' creado.")
    
    data_inicial = {"tablas": {}}
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data_inicial, file, indent=4)
    print(f"Archivo {JSON_FILE_PATH} creado y inicializado.")  # Mensaje de confirmación

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
    
    # Verificar si la tabla ya existe
    if nombre_tabla in data["tablas"]:
        raise ValueError("La tabla ya existe.")
    
    nueva_tabla = {
        "columnas": columnas
    }
    data["tablas"][nombre_tabla] = nueva_tabla
    guardar_datos_json(data)

def buscar_tabla(nombre_tabla):
    """Busca una tabla por nombre y retorna sus datos, o None si no existe."""
    data = cargar_datos_json()
    return data.get('tablas', {}).get(nombre_tabla, None)

def eliminar_tabla(nombre_tabla):
    """Elimina una tabla por nombre. Retorna True si se eliminó, o False si no existe."""
    data = cargar_datos_json()  # Cargar datos de tu fuente de datos (JSON, base de datos, etc.)
    if nombre_tabla in data.get('tablas', {}):
        del data['tablas'][nombre_tabla]  # Eliminar la tabla
        guardar_datos_json(data)  # Guarda los cambios en tu fuente de datos
        return True
    return False