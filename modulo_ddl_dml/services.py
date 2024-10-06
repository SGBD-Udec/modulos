from .models import cargar_datos, guardar_datos

def crear_tabla():
    """Crea la tabla 'ejemplo' en el archivo JSON si no existe."""
    data = cargar_datos_json()
    if 'ejemplo' not in data:
        data['ejemplo'] = []
        guardar_datos_json(data)

def agregar_ejemplo(nombre, descripcion):
    """Agrega un nuevo registro a la tabla 'ejemplo' en el archivo JSON."""
    data = cargar_datos_json()
    nuevo_ejemplo = {'nombre': nombre, 'descripcion': descripcion}
    data['ejemplo'].append(nuevo_ejemplo)
    guardar_datos_json(data)

def obtener_ejemplos():
    """Obtiene todos los registros de la tabla 'ejemplo' del archivo JSON."""
    return cargar_datos_json().get('ejemplo', [])

def eliminar_ejemplo(ejemplo_id):
    """Elimina un registro de la tabla 'ejemplo' por ID en el archivo JSON."""
    data = cargar_datos_json()
    ejemplos = data.get('ejemplo', [])
    if 0 <= ejemplo_id < len(ejemplos):
        ejemplos.pop(ejemplo_id)  # Usamos pop para eliminar por índice
        data['ejemplo'] = ejemplos
        guardar_datos_json(data)
