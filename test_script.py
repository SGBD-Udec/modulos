import json
import os

# Ruta al archivo JSON
JSON_FILE_PATH = 'modulo_ddl_dml/data.json'  # Asegúrate de que esta ruta sea correcta

def cargar_datos_json():
    """Carga datos desde el archivo JSON o inicializa una estructura vacía."""
    print("Cargando datos JSON...")  # Mensaje de depuración
    if not os.path.exists(JSON_FILE_PATH):
        inicializar_archivo_json()
    
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)
        print("Datos cargados:", data)  # Imprime los datos cargados
        return data

def inicializar_archivo_json():
    """Inicializa el archivo JSON con la estructura básica."""
    if not os.path.exists('modulo_ddl_dml'):
        os.makedirs('modulo_ddl_dml')  # Asegúrate de que el directorio exista
    
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

def agregar_tabla(nombre_tabla, columnas):
    """Agrega una nueva tabla en el archivo JSON."""
    data = cargar_datos_json()
    if nombre_tabla not in data['tablas']:
        data['tablas'][nombre_tabla] = {'columnas': columnas}
        guardar_datos_json(data)
        print(f"Tabla '{nombre_tabla}' agregada con columnas: {columnas}")
    else:
        print(f"La tabla '{nombre_tabla}' ya existe.")

if __name__ == "__main__":
    # Cargar datos desde el JSON
    data = cargar_datos_json()
    print("Datos iniciales:", data)
    
    # Crear una tabla de prueba
    agregar_tabla("test_table", ["col1", "col2"])
    
    # Listar tablas
    print("Tablas después de agregar:", cargar_datos_json()['tablas'])
