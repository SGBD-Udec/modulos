# modulo_ddl_dml/views.py
from flask import Blueprint, jsonify, request
from .models import (
    eliminar_tabla, 
    buscar_tabla, 
    cargar_datos_json, 
    actualizar_registro, 
    insertar_registro, 
    eliminar_registro,
    is_primary_key,
    obtener_estadisticas,
    verificar_nombre_tabla_existente
)

from .services import servicio_modificar_tabla

modulo_ddl_dml = Blueprint('modulo_ddl_dml', __name__)

# Rutas de DDL

@modulo_ddl_dml.route('/api/dml_ddl/tablas', methods=['GET'])
def listar_tablas():
    """Lista todas las tablas."""
    data = cargar_datos_json()
    return jsonify(data.get('ejemplos_tablas', [])), 200

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>', methods=['GET'])
def obtener_tabla(nombre_tabla):
    """Obtiene los detalles de una tabla por nombre."""
    tabla = buscar_tabla(nombre_tabla)
    if tabla is None:
        return jsonify({"message": "Tabla no encontrada."}), 404
    return jsonify(tabla), 200

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/modificar', methods=['PUT'])
def modificar_tabla_endpoint(nombre_tabla):
    """Modifica la tabla existente."""
    nuevos_datos = request.json

    if not nuevos_datos:
        return jsonify({"message": "Se requieren nuevos datos para modificar la tabla."}), 400

    try:
        servicio_modificar_tabla(nombre_tabla, nuevos_datos)
        return jsonify({"message": "Tabla modificada exitosamente."}), 200
    except Exception as e:
        return jsonify({"message": f"Error al modificar la tabla: {str(e)}"}), 500

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>', methods=['DELETE'])
def eliminar_tabla_endpoint(nombre_tabla):
    """Elimina una tabla por nombre."""
    if eliminar_tabla(nombre_tabla):
        return jsonify({"message": "Tabla eliminada exitosamente."}), 204
    return jsonify({"message": "Tabla no encontrada."}), 404

# Rutas de DML
@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/insertar', methods=['POST'])
def insertar_registro_view(nombre_tabla):
    data = request.get_json()  # Obtén el JSON enviado
    nuevo_registro = data.get('nuevo_registro')  # Obtén el registro del JSON

    # Validar que el nuevo registro no esté vacío
    if not nuevo_registro:
        return jsonify({"message": "El registro no puede estar vacío."}), 400

    # Llamar a la función de inserción
    try:
        insertar_registro(nombre_tabla, nuevo_registro)
        return jsonify({"message": "Registro insertado exitosamente."}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/actualizar', methods=['PUT'])
def actualizar_dato(nombre_tabla):
    """Actualiza registros en una tabla."""
    campos = request.json.get('campos')
    campo_condicion = request.json.get('campo_condicion')
    valor_condicion = request.json.get('valor_condicion')

    if not campos or not campo_condicion or valor_condicion is None:
        return jsonify({"message": "Los campos, campo de condición y valor de condición son requeridos."}), 400

    try:
        actualizados = actualizar_registro(nombre_tabla, campos, campo_condicion, valor_condicion)
        return jsonify({"message": f"{actualizados} registro(s) actualizado(s) exitosamente."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/eliminar', methods=['DELETE'])
def eliminar_dato(nombre_tabla):
    """Elimina registros en una tabla."""
    campo_condicion = request.json.get('campo_condicion')
    valor_condicion = request.json.get('valor_condicion')

    if not campo_condicion or not valor_condicion:
        return jsonify({"message": "El campo de condición y el valor de condición son requeridos."}), 400

    try:
        print(f"Intentando eliminar de la tabla '{nombre_tabla}' donde {campo_condicion} = {valor_condicion}.")
        eliminar_registro(nombre_tabla, campo_condicion, valor_condicion)
        return jsonify({"message": "Registro(s) eliminado(s) exitosamente."}), 200
    except ValueError as e:
        print(f"Error de valor: {str(e)}")  # Para depuración
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(f"Error inesperado: {str(e)}")  # Para depuración
        return jsonify({"message": str(e)}), 500

# Rutas para Relaciones

@modulo_ddl_dml.route('/api/dml_ddl/relaciones', methods=['GET'])
def obtener_relaciones_endpoint():
    """Obtiene todas las relaciones."""
    relaciones = obtener_relaciones()
    return jsonify(relaciones), 200

@modulo_ddl_dml.route('/api/dml_ddl/relaciones', methods=['POST'])
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
        agregar_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)
        return jsonify({"message": "Relación creada exitosamente."}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@modulo_ddl_dml.route('/api/dml_ddl/relaciones', methods=['DELETE'])
def eliminar_relacion_endpoint():
    """Elimina una relación entre tablas."""
    data = request.json
    tabla_origen = data.get('tabla_origen')
    tabla_destino = data.get('tabla_destino')

    if not tabla_origen or not tabla_destino:
        return jsonify({"message": "Tabla origen y destino son requeridas."}), 400

    try:
        eliminar_relacion(tabla_origen, tabla_destino)
        return jsonify({"message": "Relación eliminada exitosamente."}), 204
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@modulo_ddl_dml.route('/api/dml_ddl/estadisticas', methods=['GET'])
def obtener_estadisticas():
    data = cargar_datos_json()  # Asegúrate de que esta función carga el JSON correctamente
    return jsonify({
        "estadisticas": {
            "total_dml_operations": data.get("estadisticas", {}).get("total_dml_operations", 0),
            "total_ddl_commands": data.get("estadisticas", {}).get("total_ddl_commands", 0),
        }
    })