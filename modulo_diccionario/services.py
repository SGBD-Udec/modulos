# backend/modulo_diccionario/services.py
from .models import Tabla

def obtener_tabla_por_id(tabla_id):
    return Tabla.query.filter_by(id=tabla_id).first()
