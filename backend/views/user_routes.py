# app/routes.py
from flask import Blueprint, jsonify
from backend.controllers.students_controller import registerUserEndpoint

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return "<h1>Hello, World!</h1>"

