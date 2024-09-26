# backend/modulo_diccionario/serializers.py
def tabla_a_json(tabla):
    return {
        "id": tabla.id,
        "nombre": tabla.nombre,
        "descripcion": tabla.descripcion
    }
