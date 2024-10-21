import json
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ruta del archivo JSON que simula el diccionario de datos
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'instance/diccionario.json')

# Cargar la base de datos simulada desde el archivo JSON
def load_database():
    with open(DATABASE_FILE, 'r') as f:
        return json.load(f)

# Guardar los cambios en la base de datos simulada
def save_database(database):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4)

# Ruta para procesar comandos CREATE TABLE y CREATE INDEX
@app.route('/create', methods=['POST'])
def create_command():
    sql_command = request.json.get('sql_command').strip()

    # Verificar si el comando es CREATE TABLE
    if sql_command.upper().startswith('CREATE TABLE'):
        return create_table(sql_command)

    # Verificar si el comando es CREATE INDEX
    elif sql_command.upper().startswith('CREATE INDEX'):
        return create_index(sql_command)

    else:
        return jsonify({"error": "El comando debe ser CREATE TABLE o CREATE INDEX"}), 400

# Función para procesar el comando CREATE TABLE
def create_table(sql_command):
    try:
        # Parsear el comando CREATE TABLE
        command_parts = sql_command.split('(')
        table_definition = command_parts[0].replace('CREATE TABLE', '').strip()
        table_name = table_definition.split()[0]

        columns_definition = command_parts[1].strip(')').split(',')
        columns = {}
        for column_def in columns_definition:
            col_parts = column_def.strip().split()
            column_name = col_parts[0]
            column_type = ' '.join(col_parts[1:])
            columns[column_name] = column_type

        # Cargar la base de datos actual (archivo JSON)
        db = load_database()

        # Agregar la nueva tabla con descripción y número de columnas
        db['tablas'][table_name] = {
            "descripcion": f"Tabla creada por el usuario con {len(columns)} columnas.",
            "numero_columnas": len(columns),
            "columns": columns,
            "indexes": {}  # Inicializamos la sección de índices
        }

        # Guardar los cambios en el archivo JSON
        save_database(db)

        return jsonify({"message": f"Tabla '{table_name}' creada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error procesando el comando CREATE TABLE: {str(e)}"}), 400

# Función para procesar el comando CREATE INDEX
def create_index(sql_command):
    try:
        # Parsear el comando CREATE INDEX
        command_parts = sql_command.split(' ON ')
        index_definition = command_parts[0].replace('CREATE INDEX', '').strip()
        index_name = index_definition.split()[0]

        table_and_columns = command_parts[1].split('(')
        table_name = table_and_columns[0].strip()
        columns = table_and_columns[1].strip(')').split(',')

        # Limpiar los nombres de columnas
        columns = [col.strip() for col in columns]

        # Cargar la base de datos actual (archivo JSON)
        db = load_database()

        # Verificar si la tabla existe
        if table_name not in db['tablas']:
            return jsonify({"error": f"La tabla '{table_name}' no existe"}), 400

        # Agregar el índice a la tabla
        db['tablas'][table_name]['indexes'][index_name] = columns

        # Guardar los cambios en el archivo JSON
        save_database(db)

        return jsonify({"message": f"Índice '{index_name}' creado en la tabla '{table_name}'"}), 200
    except Exception as e:
        return jsonify({"error": f"Error procesando el comando CREATE INDEX: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
