import re
import json
from flask import request, jsonify
from flask import current_app as app

# Ruta del archivo JSON
DATABASE_FILE = 'instance/diccionario.json'

# Función para leer el archivo JSON
def load_data():
    with open(DATABASE_FILE, 'r') as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def parse_command(command):
    # Expresiones regulares para comandos
    pattern_single_update = r"UPDATE (\w+) SET (\w+) = '(\w+)' WHERE (\w+) = '(\w+)';"
    pattern_multiple_update = r"UPDATE (\w+) SET ((?:\w+ = '\w+', )*\w+ = '\w+') WHERE (\w+) = '(\w+)';"
    pattern_multiple_records_update = r"UPDATE (\w+) SET (\w+) = '(\w+)' WHERE (\w+) IN \((\w+(?:, \w+)*)\);"
    pattern_single_delete = r"DELETE FROM (\w+) WHERE (\w+) = '(\w+)';"
    pattern_multiple_records_delete = r"DELETE FROM (\w+) WHERE (\w+) IN \((\w+(?:, \w+)*)\);"

    # Actualizar un solo campo
    if re.match(pattern_single_update, command):
        match = re.match(pattern_single_update, command)
        table = match.group(1)
        field = match.group(2)
        new_value = match.group(3)
        condition_field = match.group(4)
        condition_value = match.group(5)
        return {
            'type': 'update',
            'table': table,
            'fields': {field: new_value},
            'condition_field': condition_field,
            'condition_value': condition_value,
            'multiple_fields': False,
            'multiple_records': False
        }

    # Actualizar múltiples campos
    elif re.match(pattern_multiple_update, command):
        match = re.match(pattern_multiple_update, command)
        table = match.group(1)
        fields_str = match.group(2)
        fields = dict(re.findall(r"(\w+) = '(\w+)'", fields_str))
        condition_field = match.group(3)
        condition_value = match.group(4)
        return {
            'type': 'update',
            'table': table,
            'fields': fields,
            'condition_field': condition_field,
            'condition_value': condition_value,
            'multiple_fields': True,
            'multiple_records': False
        }

    # Actualizar múltiples registros
    elif re.match(pattern_multiple_records_update, command):
        match = re.match(pattern_multiple_records_update, command)
        table = match.group(1)
        field = match.group(2)
        new_value = match.group(3)
        condition_field = match.group(4)
        condition_values = match.group(5).split(', ')
        return {
            'type': 'update',
            'table': table,
            'fields': {field: new_value},
            'condition_field': condition_field,
            'condition_value': condition_values,
            'multiple_fields': False,
            'multiple_records': True
        }

    # Eliminar un solo registro
    elif re.match(pattern_single_delete, command):
        match = re.match(pattern_single_delete, command)
        table = match.group(1)
        condition_field = match.group(2)
        condition_value = match.group(3)
        return {
            'type': 'delete',
            'table': table,
            'condition_field': condition_field,
            'condition_value': condition_value,
            'multiple_records': False
        }

    # Eliminar múltiples registros
    elif re.match(pattern_multiple_records_delete, command):
        match = re.match(pattern_multiple_records_delete, command)
        table = match.group(1)
        condition_field = match.group(2)
        condition_values = match.group(3).split(', ')
        return {
            'type': 'delete',
            'table': table,
            'condition_field': condition_field,
            'condition_value': condition_values,
            'multiple_records': True
        }

    return None

# Ruta para ejecutar comandos desde el front-end
@app.route('/execute_command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command')

    if not command:
        return jsonify({'error': 'Comando no proporcionado'}), 400

    parsed_data = parse_command(command)
    
    if not parsed_data:
        return jsonify({'error': 'Comando no válido'}), 400

    # Leer y actualizar la base de datos (diccionario.json)
    database = load_data()

    if parsed_data['type'] == 'update':
        table = parsed_data['table']
        fields = parsed_data['fields']
        condition_field = parsed_data['condition_field']
        condition_value = parsed_data['condition_value']

        # Actualizar el campo deseado en la tabla
        for record in database.get(table, []):
            if record.get(condition_field) == condition_value:
                record.update(fields)

        # Guardar los cambios en el archivo JSON
        save_data(database)

        return jsonify({'message': 'Comando ejecutado correctamente'}), 200
    
    return jsonify({'error': 'Error al procesar el comando'}), 400