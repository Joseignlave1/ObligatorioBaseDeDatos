# app/routes.py
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return "<h1>Hello, World!</h1>"

