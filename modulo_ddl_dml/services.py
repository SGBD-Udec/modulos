# instance/modulo_ddl_dml/services.py
from .models import Ejemplo, db

def crear_tabla():
    """Crea la tabla 'ejemplo'."""
    db.create_all()

def agregar_ejemplo(nombre, descripcion):
    """Agrega un nuevo registro a la tabla 'ejemplo'."""
    nuevo_ejemplo = Ejemplo(nombre=nombre, descripcion=descripcion)
    db.session.add(nuevo_ejemplo)
    db.session.commit()

def obtener_ejemplos():
    """Obtiene todos los registros de la tabla 'ejemplo'."""
    return Ejemplo.query.all()

def eliminar_ejemplo(ejemplo_id):
    """Elimina un registro de la tabla 'ejemplo' por ID."""
    ejemplo = Ejemplo.query.get(ejemplo_id)
    if ejemplo:
        db.session.delete(ejemplo)
        db.session.commit()
