# modulo_diccionario/views.py
import os
import json
from flask import Blueprint, jsonify, request
from .services import (
    servicio_agregar_tabla,
    servicio_obtener_tablas,
    crear_relacion,
    listar_relaciones,
    borrar_relacion,
    servicio_obtener_columnas,
    verificar_nombre_tabla_existente
)
from .models import cargar_datos_json

modulo_diccionario = Blueprint('modulo_diccionario', _name_)


@modulo_diccionario.route('/tablas', methods=['GET'])
def get_tablas():
    tablas = servicio_obtener_tablas()
    return jsonify(tablas)

@modulo_diccionario.route('/tablas/<string:nombre_tabla>/columnas', methods=['GET'])
def get_columnas(nombre_tabla):
    """Obtiene las columnas de una tabla específica."""
    columnas = servicio_obtener_columnas(nombre_tabla)
    return jsonify(columnas)

@modulo_diccionario.route('/tablas/agregar', methods=['POST'])
def post_tabla():
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    columnas = data.get("columnas", [])

    if verificar_nombre_tabla_existente(nombre):
        return jsonify({"error": "Ya existe una tabla con ese nombre."}), 400

    servicio_agregar_tabla(nombre, descripcion, columnas)
    return jsonify({"message": "Tabla agregada con éxito."}), 201


@modulo_diccionario.route('/estadisticas', methods=['GET'])
def get_estadisticas():
    data = cargar_datos_json()
    # Contar las tablas en "ejemplos_tablas" y actualizar "total_tablas"
    data["estadisticas"]["total_tablas"] = len(data.get("ejemplos_tablas", []))
    return jsonify({"estadisticas": data["estadisticas"]})

@modulo_diccionario.route('/relaciones', methods=['GET'])
def obtener_relaciones_endpoint():
    """Obtiene todas las relaciones."""
    relaciones = listar_relaciones()
    return jsonify(relaciones), 200

@modulo_diccionario.route('/relaciones', methods=['POST'])
def agregar_nueva_relacion():
    """Crea una nueva relación entre tablas."""
    data = request.json
    tabla_origen = data.get('tabla_origen')
    columna_origen = data.get('columna_origen')
    tabla_destino = data.get('tabla_destino')
    columna_destino = data.get('columna_destino')
    tipo_relacion = data.get('tipo_relacion')

    # Validación básica
    if not all([tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion]):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    try:
        crear_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)
        return jsonify({"message": "Relación creada exitosamente."}), 201
    except Exception as e:
        print(f"Error al crear relación: {e}")  # Añadir un registro de error
        return jsonify({"message": "Error al crear relación."}), 500

@modulo_diccionario.route('/relaciones', methods=['DELETE'])
def eliminar_relacion():
    data = request.get_json()

    # Asegúrate de que estás recibiendo los datos correctos
    tabla_origen = data.get('tabla_origen')
    tabla_destino = data.get('tabla_destino')

    if not tabla_origen or not tabla_destino:
        return jsonify({"message": "Datos inválidos"}), 400

    try:
        # Llama a la función para eliminar la relación
        borrar_relacion(tabla_origen, tabla_destino)  # Asegúrate de que esta función esté definida y funcione correctamente
        return '', 204  # Devuelve un estado 204 si se elimina correctamente
    except Exception as e:
        print(f"Error al eliminar relación: {e}")  # Registra el error en la consola
        return jsonify({"message": "Error al eliminar relación."}), 500