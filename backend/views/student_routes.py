from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from security.Security import Security
from controllers.student_controller import (
    registerUserEndpoint,
    getAllStudentsEndpoint,
    getStudentById,
    addStudentEndpoint,
    modifyStudent,
    deleteStudent
)

student_bp = Blueprint('student_bp', __name__)

@students_bp.route("/register", method = ['POST'])
@jwt_required()
def registerUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    userRegistered = registerUserEndpoint(email, password)

    if userRegistered is None:
        return jsonify({'message': 'there was an error with the registration'}), 500

    jwt_token = Security.generate_jwt_token(userRegistered)

    return jsonify({'message': 'user registered successfully'}, jwt_token), 201

@student_bp.route("/students/all", methods=['GET'])
@jwt_required()
def getAllStudents():
    students = getAllStudentsEndpoint()
    return jsonify(students)

@student_bp.route("/students/<int:student_id>", methods=['GET'])
@jwt_required()
def getStudentByIdRoute(student_id):
    student = getStudentById(student_id)
    if student:
        return jsonify(student)
    else:
        return jsonify({'message': 'Student not found'}), 404

@student_bp.route("/students", methods=['POST'])
@jwt_required()
def addStudent():
    data = request.json
    student_id = data.get('id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    contact_phone = data.get('contact_phone')
    email_address = data.get('email_address')
    result = addStudentEndpoint(student_id, first_name, last_name, birth_date, contact_phone, email_address)
    return jsonify(result), 201

@student_bp.route("/students/<int:student_id>", methods=['PUT'])
@jwt_required()
def modifyStudentRoute(student_id):
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    contact_phone = data.get('contact_phone')
    email_address = data.get('email_address')
    result = modifyStudent(student_id, first_name, last_name, birth_date, contact_phone, email_address)
    return jsonify(result)

@student_bp.route("/students/<int:student_id>", methods=['DELETE'])
@jwt_required()
def deleteStudentRoute(student_id):
    result = deleteStudent(student_id)
    return jsonify(result)

