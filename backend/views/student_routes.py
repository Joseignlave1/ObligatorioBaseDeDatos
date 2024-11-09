from flask import Blueprint, jsonify, request
from backend.controllers.students_controller import registerUserEndpoint
from backend.security.Security import Security

students_bp = Blueprint('students_bp', __name__)

@students_bp.route("/register", method = ['POST'])

def registerUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userRegistered = registerUserEndpoint(email, password)

    if userRegistered is None:
        return jsonify({'message': 'there was an error with the registration'}), 500

    jwt_token = Security.generate_jwt_token(userRegistered)

    return jsonify({'message': 'user registered successfully'}, jwt_token), 201
