from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diccionario(db.Model):
    __tablename__ = 'diccionario'  # Asegúrate de que este nombre coincide con el que estás usando en las consultas
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # Asegúrate de que esta línea esté presente

    def __repr__(self):
        return f'<Palabra {self.nombre}>'
