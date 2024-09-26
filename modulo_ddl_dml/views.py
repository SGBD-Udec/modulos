# modulo_ddl_dml/views.py
from flask import Blueprint, request, jsonify
from .services import agregar_ejemplo, obtener_ejemplos, eliminar_ejemplo

blueprint = Blueprint('ddl_dml', __name__)

@blueprint.route('/ejemplos', methods=['POST'])
def crear_ejemplo():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')  # Asegúrate de que la descripción sea capturada
    agregar_ejemplo(nombre, descripcion)
    return jsonify({'mensaje': 'Ejemplo creado'}), 201

@blueprint.route('/ejemplos', methods=['GET'])
def listar_ejemplos():
    ejemplos = obtener_ejemplos()
    return jsonify([{'id': e.id, 'nombre': e.nombre, 'descripcion': e.descripcion} for e in ejemplos]), 200

@blueprint.route('/ejemplos/<int:id>', methods=['DELETE'])
def eliminar_ejemplo_route(id):
    eliminar_ejemplo(id)
    return jsonify({'mensaje': 'Ejemplo eliminado'}), 204
