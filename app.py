from flask import Flask
from flask_cors import CORS  # Importa CORS
from modulo_diccionario.views import modulo_diccionario
from modulo_ddl_dml.views import modulo_ddl_dml

app = Flask(__name__)

# Configura CORS
CORS(app)  # Permite solicitudes desde cualquier origen

# Registra los Blueprints
app.register_blueprint(modulo_diccionario)
app.register_blueprint(modulo_ddl_dml)

if __name__ == '__main__':
    app.run(debug=True)
