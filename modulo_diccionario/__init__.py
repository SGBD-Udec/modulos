from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

# Crear el Blueprint
modulo_diccionario = Blueprint('modulo_diccionario', __name__)

# Importar las vistas para evitar problemas de importación circular
from .views import *
