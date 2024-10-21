# modulo_ddl_dml/models.py
import json

# Ruta del archivo JSON
DATABASE_FILE = 'instance/diccionario.json'

# Manejo del Json

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

# DML

# Función para actualizar un registro
def actualizar_registro(nombre_tabla, campos, campo_condicion, valor_condicion):
    # Cargar los datos desde el archivo JSON
    data = cargar_datos_json()

    # Obtener la tabla directamente de los datos
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    actualizados = 0

    # Iterar sobre los registros de la tabla y actualizar los que cumplan con la condición
    for registro in tabla.get('registros', []):
        if registro.get(campo_condicion) == valor_condicion:
            # Actualizar el registro con los nuevos campos
            registro.update(campos)
            actualizados += 1

    # Guardar los datos actualizados en el archivo JSON
    guardar_datos_json(data)

    # Devolver la cantidad de registros actualizados
    return actualizados


# Función para eliminar un registro
def eliminar_registro(nombre_tabla, campo_condicion, valor_condicion):
    # Cargar los datos desde el archivo JSON
    data = cargar_datos_json()

    # Obtener la tabla directamente desde los datos
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    registros_previos = len(tabla.get('registros', []))  # Número de registros antes de eliminar

    # Eliminar los registros que cumplan con la condición
    tabla['registros'] = [r for r in tabla.get('registros', []) if r.get(campo_condicion) != valor_condicion]

    registros_despues = len(tabla['registros'])  # Número de registros después de eliminar

    # Verificar si se eliminó al menos un registro
    if registros_previos == registros_despues:
        raise ValueError(f"No se encontró ningún registro con {campo_condicion} = {valor_condicion}.")

    # Guardar los datos actualizados en el archivo JSON
    guardar_datos_json(data)


# Función para insertar un nuevo registro en una tabla
def insertar_registro(nombre_tabla, nuevo_registro):
    data = cargar_datos_json()  # Cargar datos desde el archivo JSON
    # Obtener la tabla directamente de data
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    # Verificar que el registro tenga las columnas necesarias
    columnas = {col['nombre'] for col in tabla['columnas']}
    for key in nuevo_registro.keys():
        if key not in columnas:
            raise ValueError(f"El campo '{key}' no es válido para la tabla '{nombre_tabla}'.")

    # Añadir el nuevo registro a la lista de registros de la tabla
    tabla['registros'].append(nuevo_registro)

    # Depuración: imprime el objeto data para verificar que los registros se hayan agregado
    print("Datos antes de guardar:", data)

    # Guardar los datos actualizados en el JSON
    guardar_datos_json(data)  # Ahora, esto debería guardar los datos actualizados

    return {"message": "Registro insertado exitosamente."}


# DDL

# Función para buscar una tabla por nombre
def buscar_tabla(nombre_tabla):
    data = cargar_datos_json()
    for tabla in data["ejemplos_tablas"]:
        if tabla["nombre"] == nombre_tabla:
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
# Función para modificar una tabla
def modificar_tabla(nombre_tabla_actual, nuevos_datos):
   
    # Cargar los datos desde el archivo JSON
    data = cargar_datos_json()

    # Buscar la tabla que se quiere modificar
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla_actual), None)

    if tabla is None:
        raise ValueError(f"La tabla '{nombre_tabla_actual}' no existe.")

    # Modificar el nombre de la tabla si se proporciona un nuevo nombre
    nuevo_nombre = nuevos_datos.get('nombre')
    if nuevo_nombre and nuevo_nombre != nombre_tabla_actual:
        if verificar_nombre_tabla_existente(nuevo_nombre):
            raise ValueError(f"Ya existe una tabla con el nombre '{nuevo_nombre}'.")
        tabla['nombre'] = nuevo_nombre

    # Modificar la descripción de la tabla si se proporciona una nueva descripción
    nueva_descripcion = nuevos_datos.get('descripcion')
    if nueva_descripcion:
        tabla['descripcion'] = nueva_descripcion

    # Modificar las columnas de la tabla si se proporciona una nueva lista de columnas
    nuevas_columnas = nuevos_datos.get('columnas')
    if nuevas_columnas:
        tabla['columnas'] = nuevas_columnas

    # Guardar los cambios en el archivo JSON
    guardar_datos_json(data)


def verificar_nombre_tabla_existente(nombre):
    """Verifica si existe una tabla con el nombre dado en el archivo JSON."""
    data = cargar_datos_json()
    return any(tabla['nombre'] == nombre for tabla in data['ejemplos_tablas'])



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
