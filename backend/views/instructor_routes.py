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
@instructor_bp.route("/instructors/<int:instructor_id>", methods=["GET"])
@jwt_required()
def getInstructorById(instructor_id):
    instructor = getInstructorByIdEndpoint(instructor_id)
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
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    if not all([ci, nombre, apellido]):
        return jsonify({"message": "All fields are required"}), 400

    success = addInstructorEndpoint(ci, nombre, apellido)
    if success:
        return jsonify({'message': 'Instructor added successfully'}), 201
    else:
        return jsonify({'message': 'Error adding instructor'}), 500

# Modificar un instructor, incluido el ID (CI)
@instructor_bp.route("/instructors/modify", methods=["PUT"])
@jwt_required()
def modifyInstructor():
    data = request.json
    current_ci = data.get("current_ci")  # CI actual del instructor
    new_ci = data.get("new_ci")          # Nuevo CI, si aplica
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    if not all([current_ci, nombre, apellido]):
        return jsonify({"message": "All fields are required"}), 400

    success = modifyInstructorEndpoint(current_ci, new_ci, nombre, apellido)
    if success:
        return jsonify({'message': 'Instructor modified successfully'}), 200
    else:
        return jsonify({'message': 'Instructor not found or no changes made'}), 404

# Eliminar un instructor
@instructor_bp.route("/instructors/delete/<int:instructor_id>", methods=["DELETE"])
@jwt_required()
def deleteInstructor(instructor_id):
    success = deleteInstructorEndpoint(instructor_id)
    if success:
        return jsonify({'message': 'Instructor deleted successfully'}), 200
    else:
        return jsonify({'message': 'Instructor not found'}), 404
