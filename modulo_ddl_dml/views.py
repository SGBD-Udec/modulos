from flask import Blueprint, jsonify, request
from .models import agregar_tabla, buscar_tabla, eliminar_tabla, cargar_datos_json

modulo_ddl_dml = Blueprint('modulo_ddl_dml', __name__)

@modulo_ddl_dml.route('/tablas', methods=['GET'])
def listar_tablas():
    """Lista todas las tablas."""
    data = cargar_datos_json()
    return jsonify(data['tablas'])

@modulo_ddl_dml.route('/tablas', methods=['POST'])
def crear_tabla():
    """Crea una nueva tabla."""
    nombre_tabla = request.json.get('nombre')
    columnas = request.json.get('columnas')
    agregar_tabla(nombre_tabla, columnas)
    return jsonify({"message": "Tabla creada exitosamente."}), 201

@modulo_ddl_dml.route('/tablas/<string:nombre_tabla>', methods=['DELETE'])
def eliminar_una_tabla(nombre_tabla):
    """Elimina una tabla por nombre."""
    if eliminar_tabla(nombre_tabla):
        return jsonify({"message": "Tabla eliminada exitosamente."}), 204
    return jsonify({"message": "Tabla no encontrada."}), 404
