# modulo_ddl_dml/views.py
from flask import Blueprint, jsonify, request
from .models import agregar_tabla, cargar_datos_json, eliminar_tabla, buscar_tabla

modulo_ddl_dml = Blueprint('modulo_ddl_dml', __name__)

@modulo_ddl_dml.route('/api/tablas', methods=['GET'])
def listar_tablas():
    """Lista todas las tablas."""
    data = cargar_datos_json()
    print(data)  # Imprime los datos cargados para depuración
    return jsonify(data['tablas'])  # Debería devolver los datos de la clave 'tablas'

@modulo_ddl_dml.route('/api/tablas/<string:nombre_tabla>', methods=['GET'])
def obtener_tabla(nombre_tabla):
    """Busca una tabla por nombre y retorna sus datos."""
    tabla = buscar_tabla(nombre_tabla)
    if tabla is not None:
        return jsonify(tabla), 200
    return jsonify({"message": "Tabla no encontrada."}), 404

@modulo_ddl_dml.route('/api/tablas', methods=['POST'])
def crear_tabla():
    """Crea una nueva tabla."""
    nombre_tabla = request.json.get('nombre')
    columnas = request.json.get('columnas')

    # Validación de entrada
    if not nombre_tabla or not columnas:
        return jsonify({"message": "Nombre de tabla y columnas son requeridos."}), 400

    try:
        agregar_tabla(nombre_tabla, columnas)  # Llama a la función
        return jsonify({"message": "Tabla creada exitosamente."}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear la tabla: " + str(e)}), 500

@modulo_ddl_dml.route('/api/tablas/<string:nombre_tabla>', methods=['DELETE'])
def eliminar_una_tabla(nombre_tabla):
    """Elimina una tabla por nombre."""
    if eliminar_tabla(nombre_tabla):
        return jsonify({"message": "Tabla eliminada exitosamente."}), 204
    return jsonify({"message": "Tabla no encontrada."}), 404
