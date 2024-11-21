from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from backend.controllers.class_controller import (
    getAllClassesEndpoint,
    getClassByIdEndpoint,
    addClassEndpoint,
    modifyClassEndpoint,
    deleteClassEndpoint
)
from backend.models.classModels import (
    getClassesWithInstructorInShift
)
from backend.controllers.activity_controller import (
    getActivityByIdEndpoint
)
from backend.controllers.shift_controller import (
    getShiftByIdEndpoint
)
from backend.controllers.instructor_controller import (
    getInstructorByIdEndpoint
)

class_bp = Blueprint('class_bp', __name__)

@class_bp.route("/classes/all", methods=['GET'])
@jwt_required()
def getAllClasses():
    classes = getAllClassesEndpoint()
    return jsonify(classes)

@class_bp.route("/classes/<int:class_id>", methods=['GET'])
@jwt_required()
def getClassById(class_id):
    oneClass = getClassByIdEndpoint(class_id)
    if oneClass:
        return jsonify(oneClass)
    else:
        return jsonify({'message': 'Class not found'}), 404
    
@class_bp.route("/classes", methods=['POST'])
@jwt_required()
def addClass():
    data = request.json

    if not ('ci_instructor' in data and 
            'id_activity' in data and 
            'id_shift' in data and 
            'dictated' in data):
        return jsonify({'message': 'Missing data for required fields'}), 400
    
    ci_instructor = data.get('ci_instructor')
    id_activity = data.get('id_activity')
    id_shift = data.get('id_shift')
    dictated = data.get('dictated')

    if not isinstance(dictated, bool):
        return jsonify({'message': "'dictated' must be a boolean"}), 400

    instructor = getInstructorByIdEndpoint(ci_instructor)
    activity = getActivityByIdEndpoint(id_activity)
    shift = getShiftByIdEndpoint(id_shift)

    if instructor is None:
        return jsonify({"message": "Instructor not found"}), 404
    if activity is None:
        return jsonify({"message": "Activity not found"}), 404
    if shift is None:
        return jsonify({"message": "Shift not found"}), 404
    
    if (getClassesWithInstructorInShift(ci_instructor, id_shift) is not None):
        return jsonify({"message": "Instructor already has a class in this shift"}), 409

    result = addClassEndpoint(ci_instructor, id_activity, id_shift, dictated)
    return jsonify({'message': 'Class added successfully', 'class': result}), 201

@class_bp.route("/classes/<int:class_id>", methods=['DELETE'])
@jwt_required()
def deleteClassRoute(class_id):
    
    class_data = getClassByIdEndpoint(class_id)
    if class_data is None:
        return jsonify({"message": "Class not found"}), 404

    id_shift = class_data.get("id_turno")
    shift_data = getShiftByIdEndpoint(id_shift)
    if shift_data is None:
        return jsonify({"message": "Shift not found"}), 404

    hora_inicio = shift_data.get('hora_inicio')
    hora_fin = shift_data.get('hora_fin')
    current_time = datetime.now().time()

    if hora_inicio <= current_time <= hora_fin:
        return jsonify({"message": "Class cannot be deleted during its scheduled time"}), 403

    result = deleteClassEndpoint(class_id)
    return jsonify(result)

@class_bp.route("/classes/<int:class_id>", methods=['PUT'])
@jwt_required()
def modifyClass(class_id):
    data = request.json

    if not ('ci_instructor' in data and 
            'id_activity' in data and 
            'id_shift' in data and 
            'dictated' in data):
        return jsonify({'message': 'Missing data for required fields'}), 400
    
    ci_instructor = data.get('ci_instructor')
    id_activity = data.get('id_activity')
    id_shift = data.get('id_shift')
    dictated = data.get('dictated')

    if not isinstance(dictated, bool):
        return jsonify({'message': "'dictated' must be a boolean"}), 400
    
    instructor = getInstructorByIdEndpoint(ci_instructor)
    activity = getActivityByIdEndpoint(id_activity)
    shift = getShiftByIdEndpoint(id_shift)

    if instructor is None:
        return jsonify({"message": "Instructor not found"}), 404
    if activity is None:
        return jsonify({"message": "Activity not found"}), 404
    if shift is None:
        return jsonify({"message": "Shift not found"}), 404
    
    class_data = getClassByIdEndpoint(class_id)
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
        return jsonify({"message": "Class cannot be deleted during its scheduled time"}), 403

    if (getClassesWithInstructorInShift(ci_instructor, id_shift) is not None):
        return jsonify({"message": "Instructor already has a class in this shift"}), 409

    result = modifyClassEndpoint(class_id, ci_instructor, id_activity, id_shift, dictated)
    return jsonify(result)