from flask import Flask
from modulo_diccionario.views import modulo_diccionario
from modulo_diccionario.services import agregar_ejemplo
from modulo_ddl_dml.views import modulo_ddl_dml  # Asegúrate de que este sea el nombre correcto del Blueprint

app = Flask(__name__)

# Registra los Blueprints
app.register_blueprint(modulo_diccionario)
app.register_blueprint(modulo_ddl_dml)


agregar_ejemplo("Ejemplo 1", "Descripción del ejemplo 1")  # Este ejemplo se agregará al inicio


if __name__ == '__main__':
    app.run(debug=True)
