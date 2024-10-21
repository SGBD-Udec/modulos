# modulo_diccionario/views.py
import os
import json
from flask import Blueprint, jsonify, request
from .services import (
    servicio_agregar_tabla,
    servicio_obtener_tablas,
    servicio_eliminar_tabla,
    actualizar_contadores_dml,
    actualizar_contadores_ddl,
    obtener_estadisticas
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
    servicio_incrementar_ddl()  # Incrementar contadores de comandos DDL
    return jsonify({"message": "Tabla agregada con éxito."}), 201

@modulo_diccionario.route('/tablas/<string:nombre>', methods=['DELETE'])
def delete_tabla(nombre):
    success = servicio_eliminar_tabla(nombre)
    if success:
        return jsonify({"message": "Tabla eliminada con éxito."}), 200
    else:
        return jsonify({"error": "Tabla no encontrada."}), 404

<<<<<<< HEAD
@modulo_diccionario.route('/relaciones', methods=['GET'])
def get_relaciones():
    relaciones = servicio_obtener_relaciones()
    return jsonify(relaciones)

@modulo_diccionario.route('/relaciones/agregar', methods=['POST'])
def post_relacion():
    data = request.json
    servicio_agregar_relacion(
        data.get("tabla_origen"),
        data.get("columna_origen"),
        data.get("tabla_destino"),
        data.get("columna_destino"),
        data.get("tipo_relacion")
    )

    return jsonify({"message": "Relación agregada con éxito."}), 201

=======
@modulo_diccionario.route('/estadisticas', methods=['GET'])
def get_estadisticas():
    estadisticas = obtener_estadisticas()  
    return jsonify(estadisticas)
>>>>>>> Pruebaunion
