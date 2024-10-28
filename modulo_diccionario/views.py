# modulo_diccionario/views.py
import os
import json
from flask import Blueprint, jsonify, request
from .services import (
    servicio_agregar_tabla,
    servicio_obtener_tablas,
    servicio_eliminar_tabla,
    verificar_nombre_tabla_existente
)


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

    if verificar_nombre_tabla_existente(nombre):
        return jsonify({"error": "Ya existe una tabla con ese nombre."}), 400

    servicio_agregar_tabla(nombre, descripcion, columnas)
    actualizar_contadores_dml()
    actualizar_contadores_ddl()  # Incrementar contadores de comandos DDL
    return jsonify({"message": "Tabla agregada con éxito."}), 201

@modulo_diccionario.route('/tablas/<string:nombre>', methods=['DELETE'])
def delete_tabla(nombre):
    success = servicio_eliminar_tabla(nombre)
    if success:
        return jsonify({"message": "Tabla eliminada con éxito."}), 200
    else:
        return jsonify({"error": "Tabla no encontrada."}), 404
