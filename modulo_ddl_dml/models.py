# modulo_ddl_dml/models.py
from modulo_diccionario.models import db  # Asegúrate de que estás importando la misma instancia de db

class Ejemplo(db.Model):
    __tablename__ = 'ejemplo'  # Asegúrate de que este sea el nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)  # Agrega este campo según tus necesidades

    def __repr__(self):
        return f'<Ejemplo {self.nombre}>'
