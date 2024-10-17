# modulo_diccionario/views.py
import os
import json
from flask import Blueprint, jsonify, request, current_app
from .services import obtener_ejemplos_tablas, agregar_ejemplo_tabla, eliminar_ejemplo_tabla  # Asegúrate de importar las funciones adecuadas

modulo_diccionario = Blueprint('modulo_diccionario', __name__)

def obtener_datos_json():
    """Función para obtener los datos del archivo diccionario.json."""
    try:
        with open(os.path.join(current_app.instance_path, 'diccionario.json'), 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return []

@modulo_diccionario.route('/ejemplos', methods=['GET'])
def get_ejemplos():
    ejemplos_tablas = obtener_ejemplos_tablas()
    return jsonify(ejemplos_tablas)

@modulo_diccionario.route('/ejemplos/agregar', methods=['POST'])
def post_ejemplo():
    data = request.json
    agregar_ejemplo_tabla(data.get("nombre"), data.get("descripcion"))
    return jsonify({"message": "Ejemplo agregado."}), 201

@modulo_diccionario.route('/ejemplos/<int:ejemplo_id>', methods=['DELETE'])
def eliminar_ejemplo_view(ejemplo_id):
    print(f"Intentando eliminar el ejemplo con ID: {ejemplo_id}")
    if eliminar_ejemplo_tabla(ejemplo_id):  # Llama a la función de servicio
        return jsonify({"message": f"Ejemplo con ID {ejemplo_id} eliminado."}), 204
    else:
        print(f"Ejemplo no encontrado para ID: {ejemplo_id}")
        return jsonify({"message": "Ejemplo no encontrado."}), 404



