# app/routes.py
from flask import Blueprint

# Crear un blueprint para las rutas principales
main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return "Hello, World!"
