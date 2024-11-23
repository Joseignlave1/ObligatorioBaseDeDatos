from flask import Blueprint, jsonify, request
from backend.controllers.auth_controller import registerEndpoint, loginEndpoint
from backend.security.Security import Security

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/register", methods=['POST'])
def registerUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userRegistered = registerEndpoint(email, password)

    if userRegistered is None:
        return jsonify({'message': 'There was an error with the registration'}), 500

    jwt_token = Security.generate_jwt_token(userRegistered)
    
    return jsonify({'message': 'User registered successfully', 'token': jwt_token}), 201

@auth_bp.route("/login", methods=['POST'])
def loginUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userLogin = loginEndpoint(email, password)

    if not userLogin:
        return jsonify({'message': 'Error in the credentials'}), 401

    jwt_token = Security.generate_jwt_token(userLogin)

    return jsonify({'message': 'Login successful', 'token': jwt_token}), 200
