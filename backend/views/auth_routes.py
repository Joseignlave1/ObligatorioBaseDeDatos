from crypt import methods

from flask import Blueprint, jsonify, request
from backend.controllers.auth_controller import registerEndpoint, loginEndpoint
from backend.security.Security import Security

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/register", methods = ['POST'])

def registerUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userRegistered = registerEndpoint(email, password)

    jwt_token = Security.generate_jwt_token(userRegistered)

    if userRegistered is None:
        return jsonify({'message': 'there was an error with the registration'}), 500

    return jsonify({'message': 'user registered successfully'}, jwt_token), 201

@auth_bp.route ("/login", methods= ['POST'])

def loginUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userLogin = loginEndpoint(email, password)

    jwt_token = Security.generate_jwt_token(userLogin)

    if not userLogin:
        return jsonify({'message': 'Error in the credencials'}), 401
    else:
        return jsonify({'message ': 'Login succesfully'}, jwt_token), 201