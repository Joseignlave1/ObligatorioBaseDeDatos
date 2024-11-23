from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.controllers.student_controller import (
    getAllStudentsEndpoint,
    getStudentByCi as controller_getStudentByCi,  # Renombramos para evitar conflicto
    addStudentEndpoint,
    modifyStudent,
    deleteStudent
)

student_bp = Blueprint('student_bp', __name__)

@student_bp.route("/students/all", methods=['GET'])
@jwt_required()
def getAllStudents():
    students = getAllStudentsEndpoint()
    return jsonify(students)

@student_bp.route("/students/<int:student_ci>", methods=['GET'])
@jwt_required()
def getStudentByCi(student_ci):
    student = controller_getStudentByCi(student_ci)  # Llamamos al controlador con el nombre adecuado
    if student:
        return jsonify(student)
    else:
        return jsonify({'message': 'Student not found'}), 404

@student_bp.route("/students", methods=['POST'])
@jwt_required()
def addStudent():
    data = request.json
    student_ci = data.get('ci')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    contact_phone = data.get('contact_phone')
    email_address = data.get('email_address')
    
    if not all([student_ci, first_name, last_name, birth_date, contact_phone, email_address]):
        return jsonify({'message': 'Missing data for required fields'}), 400
    
    result = addStudentEndpoint(student_ci, first_name, last_name, birth_date, contact_phone, email_address)
    return jsonify(result), 201

@student_bp.route("/students/<int:student_ci>", methods=['PUT'])
@jwt_required()
def modifyStudentRoute(student_ci):
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    contact_phone = data.get('contact_phone')
    email_address = data.get('email_address')
    
    if not all([first_name, last_name, birth_date, contact_phone, email_address]):
        return jsonify({'message': 'Missing data for required fields'}), 400
    
    result = modifyStudent(student_ci, first_name, last_name, birth_date, contact_phone, email_address)
    return jsonify(result)

@student_bp.route("/students/<int:student_ci>", methods=['DELETE'])
@jwt_required()
def deleteStudentRoute(student_ci):
    result = deleteStudent(student_ci)
    return jsonify(result)
