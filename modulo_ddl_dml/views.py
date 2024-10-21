# modulo_ddl_dml/views.py
from flask import Blueprint, jsonify, request
from .models import eliminar_tabla, buscar_tabla, cargar_datos_json, actualizar_registro, insertar_registro, agregar_relacion, obtener_relaciones
from .services import (
    agregar_registro,
    modificar_registro,
    borrar_registro,
    crear_relacion,
    listar_relaciones,
    borrar_relacion
)

modulo_ddl_dml = Blueprint('modulo_ddl_dml', __name__)

# Rutas de DDL

@modulo_ddl_dml.route('/api/dml_ddl/tablas', methods=['GET'])
def listar_tablas():
    """Lista todas las tablas."""
    data = cargar_datos_json()
    return jsonify(data.get('ejemplos_tablas', {}))

@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>', methods=['GET'])
def obtener_tabla(nombre_tabla):
    """Obtiene los detalles de una tabla por nombre."""
    tabla = buscar_tabla(nombre_tabla)
    if tabla is None:
        return jsonify({"message": "Tabla no encontrada."}), 404
    return jsonify(tabla), 200


@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>', methods=['DELETE'])
def eliminar_tabla_endpoint(nombre_tabla):
    """Elimina una tabla por nombre."""
    if eliminar_tabla(nombre_tabla):
        return jsonify({"message": "Tabla eliminada exitosamente."}), 204
    return jsonify({"message": "Tabla no encontrada."}), 404

# Rutas de DML
@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/insertar', methods=['POST'])
def insertar_registro_view(nombre_tabla):  # Asegúrate de que el argumento esté aquí
    nuevo_registro = request.get_json()  # Aquí obtienes el nuevo registro del cuerpo de la solicitud
    if insertar_registro(nombre_tabla, nuevo_registro):  # Llama a la función de inserción correctamente
        return jsonify({"message": "Registro insertado exitosamente."}), 201
    return jsonify({"message": "Error al insertar el registro."}), 400
        
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
        return jsonify({"message": str(e)}), 500  # Regresar el mensaje de error



@modulo_ddl_dml.route('/api/dml_ddl/tablas/<string:nombre_tabla>/eliminar', methods=['DELETE'])
def eliminar_dato(nombre_tabla):
    """Elimina registros en una tabla."""
    campo_condicion = request.json.get('campo_condicion')
    valor_condicion = request.json.get('valor_condicion')

    if not campo_condicion or not valor_condicion:
        return jsonify({"message": "El campo de condición y el valor de condición son requeridos."}), 400

    try:
        borrar_registro(nombre_tabla, campo_condicion, valor_condicion)
        return jsonify({"message": "Registro(s) eliminado(s) exitosamente."}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

# Rutas para Relaciones

@modulo_ddl_dml.route('/api/dml_ddl/relaciones', methods=['GET'])
def obtener_relaciones():
    """Obtiene todas las relaciones."""
    relaciones = listar_relaciones()
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

    crear_relacion(tabla_origen, columna_origen, tabla_destino, columna_destino, tipo_relacion)
    return jsonify({"message": "Relación creada exitosamente."}), 201

@modulo_ddl_dml.route('/api/dml_ddl/relaciones', methods=['DELETE'])
def eliminar_relacion_endpoint():
    """Elimina una relación entre tablas."""
    data = request.json
    tabla_origen = data.get('tabla_origen')
    tabla_destino = data.get('tabla_destino')

    if not tabla_origen or not tabla_destino:
        return jsonify({"message": "Tabla origen y destino son requeridas."}), 400

    borrar_relacion(tabla_origen, tabla_destino)
    return jsonify({"message": "Relación eliminada exitosamente."}), 204
