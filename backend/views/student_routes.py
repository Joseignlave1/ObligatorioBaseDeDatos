from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.controllers.student_controller import (
    getAllStudentsEndpoint,
    getStudentByCi as controller_getStudentByCi,  # Renombramos para evitar conflicto
    addStudentEndpoint,
    modifyStudent,
    deleteStudent,
    addStudentToClass,
    deleteStudentFromClassEndpoint
)
from backend.controllers.class_controller import (
    getClassByIdEndpoint
)
from backend.models.student_class import (
    getClassesWithStudent
)
from backend.controllers.shift_controller import (
    getShiftByIdEndpoint
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


@student_bp.route("/students/class/AddStudent", methods=['POST'])
@jwt_required()
def addStudentToClass():
    data = request.json
    
    if not ('id_clase' in data and 'ci_alumno' in data):
        return jsonify({'message': 'Missing data for required fields'}), 400

    id_clase = data.get('id_clase')
    ci_alumno = data.get('ci_alumno')
    id_equipamiento = data.get('id_equipamiento', None)


    student = getStudentByCi(ci_alumno)
    class_data = getClassByIdEndpoint(id_clase)

    if student is None:
        return jsonify({"message": "Student not found"}), 404
    if class_data is None:
        return jsonify({"message": "Class not found"}), 404
    
    student_Classes = getClassesWithStudent(ci_alumno)

    for oneClass in student_Classes:
        if (class_data['id_turno'] == oneClass['id_turno']):
            return jsonify({"message": "Student already has a class in this shift"}), 409
    
    result = addStudentToClass(id_clase, ci_alumno, id_equipamiento)
    return jsonify(result)
    
@student_bp.route("/students/class/deleteStudent", methods=['DELETE'])
@jwt_required()
def deleteStudentFromClass():
    data = request.json
    
    if not ('id_clase' in data and 'ci_alumno' in data):
        return jsonify({'message': 'Missing data for required fields'}), 400

    id_clase = data.get('id_clase')
    ci_alumno = data.get('ci_alumno')
    
    class_data = getClassByIdEndpoint(id_clase)
    if class_data is None:
        return jsonify({"message": "Class not found"}), 404

    id_shift_exist_class = class_data.get("id_turno")
    shift_data = getShiftByIdEndpoint(id_shift_exist_class)
    if shift_data is None:
        return jsonify({"message": "Shift not found"}), 404

    hora_inicio = datetime.strptime(shift_data.get('hora_inicio'), '%H:%M:%S').time()
    hora_fin = datetime.strptime(shift_data.get('hora_fin'), '%H:%M:%S').time()
    current_time = datetime.now().time()

    if hora_inicio <= current_time <= hora_fin:
        return jsonify({"message": "Student cannot be deleted during its scheduled time"}), 403

    result = deleteStudentFromClassEndpoint(id_clase, ci_alumno)
    return jsonify(result)
    