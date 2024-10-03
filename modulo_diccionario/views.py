from flask import Blueprint, jsonify
from .services import obtener_ejemplos, agregar_ejemplo

modulo_diccionario = Blueprint('modulo_diccionario', __name__)

@modulo_diccionario.route('/ejemplos', methods=['GET'])
def get_ejemplos():
    ejemplos = obtener_ejemplos()
    return jsonify(ejemplos)

@modulo_diccionario.route('/ejemplos/agregar', methods=['POST'])
def post_ejemplo():
    # Aquí deberías manejar la adición de un nuevo ejemplo desde el request
    agregar_ejemplo("Ejemplo desde API", "Descripción desde API")
    return jsonify({"message": "Ejemplo agregado."}), 201
