from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required

from ..controllers.shift_controller import (
    getAllShiftsEndpoint,
    getShiftByIdEndpoint,
    addShiftEndpoint,
    modifyShiftEndpoint,
    deleteShiftEndpoint
)

shift_bp = Blueprint('shift_bp', __name__)

@shift_bp.route("/shifts/all", methods=['GET'])
@jwt_required()
def getAllShifts():
    shifts = getAllShiftsEndpoint()
    return jsonify(shifts)

@shift_bp.route("/shifts/<int:shift_id>", methods=['GET'])
@jwt_required()
def getShiftById(shift_id):
    shift = getShiftByIdEndpoint(shift_id)
    if shift:
        return jsonify(shift)
    else:
        return jsonify({'message': 'Shift not found'}), 404

@shift_bp.route("/shifts", methods=['POST'])
@jwt_required()
def addShift():
    data = request.json
    shift_id = data.get('id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    result = addShiftEndpoint(shift_id, start_time, end_time)
    return jsonify(result), 201

@shift_bp.route("/shifts/<int:shift_id>", methods=['PUT'])
@jwt_required()
def modifyShift(shift_id):
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    result = modifyShiftEndpoint(shift_id, start_time, end_time)
    return jsonify(result)

@shift_bp.route("/shifts/<int:shift_id>", methods=['DELETE'])
@jwt_required()
def deleteShift(shift_id):
    result = deleteShiftEndpoint(shift_id)
    return jsonify(result)
