# instance/modulo_ddl_dml/serializers.py
from .models import Ejemplo

def ejemplo_to_dict(ejemplo):
    """Convierte un objeto Ejemplo en un diccionario."""
    return {
        'id': ejemplo.id,
        'nombre': ejemplo.nombre,
        'descripcion': ejemplo.descripcion
    }

def ejemplos_to_list(ejemplos):
    """Convierte una lista de objetos Ejemplo en una lista de diccionarios."""
    return [ejemplo_to_dict(ejemplo) for ejemplo in ejemplos]
