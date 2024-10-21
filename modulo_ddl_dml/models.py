# modulo_ddl_dml/models.py
import json

# Ruta del archivo JSON
DATABASE_FILE = 'instance/diccionario.json'

# Función para leer el archivo JSON
def cargar_datos_json():
    with open(DATABASE_FILE, 'r') as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def guardar_datos_json(data):
    try:
        with open(DATABASE_FILE, 'w') as f:  # Asegúrate de usar DATABASE_FILE
            json.dump(data, f, indent=4)
        print("Datos guardados correctamente en diccionario.json.")  # Mensaje de depuración
    except Exception as e:
        print("Error al guardar los datos:", e)

# Función para buscar una tabla por nombre
def buscar_tabla(nombre_tabla):
    data = cargar_datos_json()
    for tabla in data.get('ejemplos_tablas', []):
        if tabla['nombre'] == nombre_tabla:
            return tabla
    return None

# Función para eliminar una tabla por nombre
def eliminar_tabla(nombre_tabla):
    data = cargar_datos_json()
    
    for i, tabla in enumerate(data['ejemplos_tablas']):
        if tabla['nombre'] == nombre_tabla:
            del data['ejemplos_tablas'][i]
            guardar_datos_json(data)
            return True
    
    return False

# Función para actualizar un registro
def actualizar_registro(nombre_tabla, campos, campo_condicion, valor_condicion):
    data = cargar_datos_json()
    tabla = buscar_tabla(nombre_tabla)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    actualizados = 0
    for registro in tabla.get('registros', []):  # Asegúrate de que 'registros' exista
        if registro.get(campo_condicion) == valor_condicion:
            registro.update(campos)
            actualizados += 1

    guardar_datos_json(data)
    return actualizados

# Función para eliminar un registro
def eliminar_registro(nombre_tabla, campo_condicion, valor_condicion):
    data = cargar_datos_json()
    tabla = buscar_tabla(nombre_tabla)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")
    
    tabla['registros'] = [r for r in tabla.get('registros', []) if r.get(campo_condicion) != valor_condicion]
    guardar_datos_json(data)

# Función para insertar un nuevo registro en una tabla
def insertar_registro(nombre_tabla, nuevo_registro):
    data = cargar_datos_json()
    tabla = buscar_tabla(nombre_tabla)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    # Mensaje de depuración antes de la inserción
    print("Antes de insertar:", tabla['registros'])

    # Añadir el nuevo registro a la lista de registros de la tabla
    tabla['registros'].append(nuevo_registro)

    # Mensaje de depuración después de la inserción
    print("Después de insertar:", tabla['registros'])

    # Guardar los datos actualizados en el JSON
    guardar_datos_json(data)


# ---- Nuevas Funciones para Relaciones ---- #

# Función para agregar una relación
def agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion):
    data = cargar_datos_json()

    nueva_relacion = {
        "tabla_origen": tabla_origen,
        "columna_origen": columna_origen,
        "tabla_destino": tabla_destino,
        "columna_destino": columna_destino,
        "tipo_relacion": tipo_relacion
    }

    data.setdefault("relaciones", []).append(nueva_relacion)  # Asegúrate de que 'relaciones' exista
    guardar_datos_json(data)

# Función para obtener todas las relaciones
def obtener_relaciones():
    data = cargar_datos_json()
    return data.get("relaciones", [])

# Función para eliminar una relación
def eliminar_relacion(tabla_origen, tabla_destino):
    data = cargar_datos_json()
    relaciones = data.get("relaciones", [])
    
    relaciones_filtradas = [r for r in relaciones if not (r["tabla_origen"] == tabla_origen and r["tabla_destino"] == tabla_destino)]
    
    data["relaciones"] = relaciones_filtradas
    guardar_datos_json(data)
    return True
