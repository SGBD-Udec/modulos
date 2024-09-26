from flask import Blueprint, render_template
from .models import Diccionario

blueprint = Blueprint('diccionario', __name__)

@blueprint.route('/')
def mostrar_diccionario():
    palabras = Diccionario.query.all()  # Esto debería funcionar si la conexión está bien
    print(f'Palabras obtenidas: {palabras}')  # Imprime los resultados en la consola
    return render_template('diccionario.html', palabras=palabras)
