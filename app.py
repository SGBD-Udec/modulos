from flask import Flask
from config import Config
from modulo_diccionario.models import db  # Asegúrate de que esta es la única importación de db
from modulo_diccionario.views import blueprint as diccionario_blueprint
from modulo_ddl_dml.views import blueprint as dml_blueprint  # Asegúrate de tener esto

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)  # Aquí inicializas db

    app.register_blueprint(diccionario_blueprint)
    app.register_blueprint(dml_blueprint)

    with app.app_context():
        db.create_all()  # Crea las tablas aquí

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
from flask import Flask
from config import Config
from modulo_diccionario.models import db  # Asegúrate de que esta es la única importación de db
from modulo_diccionario.views import blueprint as diccionario_blueprint
from modulo_ddl_dml.views import blueprint as dml_blueprint  # Asegúrate de tener esto

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)  # Aquí inicializas db

    app.register_blueprint(diccionario_blueprint)
    app.register_blueprint(dml_blueprint)

    with app.app_context():
        db.create_all()  # Crea las tablas aquí

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
