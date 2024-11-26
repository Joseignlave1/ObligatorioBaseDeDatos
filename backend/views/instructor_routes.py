from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.controllers.instructor_controller import (
    getAllInstructorsEndpoint,
    getInstructorByIdEndpoint,
    addInstructorEndpoint,
    modifyInstructorEndpoint,
    deleteInstructorEndpoint
)

instructor_bp = Blueprint('instructor_bp', __name__)

# Obtener todos los instructores
@instructor_bp.route("/instructors/all", methods=["GET"])
@jwt_required()
def getAllInstructors():
    instructors = getAllInstructorsEndpoint()
    if instructors is not None:
        return jsonify(instructors), 200
    else:
        return jsonify({'message': 'Error retrieving instructors'}), 500

# Obtener un instructor por ID
@instructor_bp.route("/instructors/<int:instructor_ci>", methods=["GET"])
@jwt_required()
def getInstructorByCi(instructor_ci):
    instructor = getInstructorByIdEndpoint(instructor_ci)
    if instructor:
        return jsonify(instructor), 200
    else:
        return jsonify({'message': 'Instructor not found'}), 404

# Agregar un nuevo instructor
@instructor_bp.route("/instructors/add", methods=["POST"])
@jwt_required()
def addInstructor():
    data = request.json
    ci = data.get("ci")
    name = data.get("name")
    last_name = data.get("last_name")
    
    if not all([ci, name, last_name]):
        return jsonify({"message": "All fields are required"}), 400

    success = addInstructorEndpoint(ci, name, last_name)
    if success:
        return jsonify({'message': 'Instructor added successfully'}), 201
    else:
        return jsonify({'message': 'Error adding instructor'}), 500

# Modificar un instructor
@instructor_bp.route("/instructors/modify/<int:instructor_ci>", methods=["PUT"])
@jwt_required()
def modifyInstructor(instructor_ci):
    data = request.json
    name = data.get("name")
    last_name = data.get("last_name")
    
    if not all([name, last_name]):
        return jsonify({"message": "All fields are required"}), 400

    success = modifyInstructorEndpoint(instructor_ci, name, last_name)
    if success:
        return jsonify({'message': 'Instructor modified successfully'}), 200
    else:
        return jsonify({'message': 'Instructor not found or no changes made'}), 404

# Eliminar un instructor
@instructor_bp.route("/instructors/delete/<int:instructor_ci>", methods=["DELETE"])
@jwt_required()
def deleteInstructor(instructor_ci):
    success = deleteInstructorEndpoint(instructor_ci)
    if success:
        return jsonify({'message': 'Instructor deleted successfully'}), 200
    else:
        return jsonify({'message': 'Instructor not found'}), 404
