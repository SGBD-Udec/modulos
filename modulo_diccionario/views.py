# modulo_diccionario/views.py
import os
import json
from flask import Blueprint, jsonify, request
from .services import servicio_agregar_tabla, servicio_obtener_tablas, servicio_eliminar_tabla, verificar_nombre_tabla_existente

modulo_diccionario = Blueprint('modulo_diccionario', __name__)

@modulo_diccionario.route('/tablas', methods=['GET'])
def get_tablas():
    tablas = servicio_obtener_tablas()
    return jsonify(tablas)

@modulo_diccionario.route('/tablas/agregar', methods=['POST'])
def post_tabla():
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    columnas = data.get("columnas", [])

    # Aquí deberías tener una función que verifica si el nombre ya existe
    if verificar_nombre_tabla_existente(nombre):  # Necesitas implementar esto
        return jsonify({"error": "Ya existe una tabla con ese nombre."}), 400

    # Si todo está bien, agrega la tabla
    servicio_agregar_tabla(nombre, descripcion, columnas)
    return jsonify({"message": "Tabla agregada con éxito."}), 201

@modulo_diccionario.route('/tablas/<int:tabla_id>', methods=['DELETE'])
def delete_tabla(tabla_id):
    if servicio_eliminar_tabla(tabla_id):
        return jsonify({"message": "Tabla eliminada con éxito."}), 204
    return jsonify({"message": "Tabla no encontrada."}), 404

