import json

# Ruta del archivo JSON
DATABASE_FILE = 'instance/diccionario.json'

# Manejo del JSON

# Función para leer el archivo JSON
def cargar_datos_json():
    with open(DATABASE_FILE, 'r') as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def guardar_datos_json(data):
    try:
        with open(DATABASE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("Datos guardados correctamente en diccionario.json.")
    except Exception as e:
        print("Error al guardar los datos:", e)

# DML

def actualizar_registro(nombre_tabla, campos, campo_condicion, valor_condicion):
    data = cargar_datos_json()
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    actualizados = 0

    for registro in tabla.get('registros', []):
        if registro.get(campo_condicion) == valor_condicion:
            registro.update(campos)
            actualizados += 1

    guardar_datos_json(data)

    # Actualizar estadísticas DML
    data['estadisticas']['total_dml_operations'] += 1
    guardar_datos_json(data)

    return actualizados

def eliminar_registro(nombre_tabla, campo_condicion, valor_condicion):
    data = cargar_datos_json()
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    if is_primary_key(tabla, campo_condicion, valor_condicion):
        raise ValueError(f"No se puede eliminar un registro que es parte de una PRIMARY KEY: {campo_condicion} = {valor_condicion}.")

    registros_previos = len(tabla.get('registros', []))
    tabla['registros'] = [r for r in tabla.get('registros', []) if r.get(campo_condicion) != valor_condicion]
    registros_despues = len(tabla['registros'])

    if registros_previos == registros_despues:
        raise ValueError(f"No se encontró ningún registro con {campo_condicion} = {valor_condicion}.")

    guardar_datos_json(data)

    # Actualizar estadísticas DML
    data['estadisticas']['total_dml_operations'] += 1
    guardar_datos_json(data)

def is_primary_key(tabla, campo_condicion, valor):
    for columna in tabla.get('columnas', []):
        if campo_condicion == columna['nombre']:
            return "PRIMARY KEY" in columna['restricciones']
    return False

def insertar_registro(nombre_tabla, nuevo_registro):
    data = cargar_datos_json()
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla), None)

    if tabla is None:
        raise ValueError(f"La tabla {nombre_tabla} no existe.")

    columnas = {col['nombre'] for col in tabla['columnas']}
    for key in nuevo_registro.keys():
        if key not in columnas:
            raise ValueError(f"El campo '{key}' no es válido para la tabla '{nombre_tabla}'.")

    tabla['registros'].append(nuevo_registro)
    guardar_datos_json(data)

    # Actualizar estadísticas DML
    data['estadisticas']['total_dml_operations'] += 1
    guardar_datos_json(data)

    return {"message": "Registro insertado exitosamente."}

# DDL

def buscar_tabla(nombre_tabla):
    data = cargar_datos_json()
    for tabla in data["ejemplos_tablas"]:
        if tabla["nombre"] == nombre_tabla:
            return tabla
    return None

def eliminar_tabla(nombre_tabla):
    data = cargar_datos_json()
    
    for i, tabla in enumerate(data['ejemplos_tablas']):
        if tabla['nombre'] == nombre_tabla:
            del data['ejemplos_tablas'][i]
            guardar_datos_json(data)
            # Actualizar estadísticas DDL
            data['estadisticas']['total_ddl_commands'] += 1
            guardar_datos_json(data)
            return True    
    return False

def modificar_tabla(nombre_tabla_actual, nuevos_datos):
    data = cargar_datos_json()
    tabla = next((t for t in data["ejemplos_tablas"] if t['nombre'] == nombre_tabla_actual), None)

    if tabla is None:
        raise ValueError(f"La tabla '{nombre_tabla_actual}' no existe.")

    nuevo_nombre = nuevos_datos.get('nombre')
    if nuevo_nombre and nuevo_nombre != nombre_tabla_actual:
        if verificar_nombre_tabla_existente(nuevo_nombre):
            raise ValueError(f"Ya existe una tabla con el nombre '{nuevo_nombre}'.")
        tabla['nombre'] = nuevo_nombre

    nueva_descripcion = nuevos_datos.get('descripcion')
    if nueva_descripcion:
        tabla['descripcion'] = nueva_descripcion

    nuevas_columnas = nuevos_datos.get('columnas')
    if nuevas_columnas:
        tabla['columnas'] = nuevas_columnas

    guardar_datos_json(data)

    # Actualizar estadísticas DDL
    data['estadisticas']['total_ddl_commands'] += 1
    guardar_datos_json(data)

def verificar_nombre_tabla_existente(nombre):
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

    data.setdefault("relaciones", []).append(nueva_relacion)
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

# Función para obtener estadísticas
def obtener_estadisticas():
    data = cargar_datos_json()
    return data.get('estadisticas', {})