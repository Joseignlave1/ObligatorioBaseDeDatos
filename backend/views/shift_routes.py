from flask import Blueprint, jsonify, request
from ..controllers.shift_controller import (
    getAllShiftsEndpoint,
    getShiftByIdEndpoint,
    addShiftEndpoint,
    modifyShiftEndpoint,
    deleteShiftEndpoint
)

shift_bp = Blueprint('shift_bp', __name__)

@shift_bp.route("/shifts/all", methods=['GET'])
def getAllShifts():
    shifts = getAllShiftsEndpoint()
    return jsonify(shifts)

@shift_bp.route("/shifts/<int:shift_id>", methods=['GET'])
def getShiftById(shift_id):
    shift = getShiftByIdEndpoint(shift_id)
    if shift:
        return jsonify(shift)
    else:
        return jsonify({'message': 'Shift not found'}), 404

@shift_bp.route("/shifts", methods=['POST'])
def addShift():
    data = request.json
    shift_id = data.get('id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    result = addShiftEndpoint(shift_id, start_time, end_time)
    return jsonify(result), 201

@shift_bp.route("/shifts/<int:shift_id>", methods=['PUT'])
def modifyShift(shift_id):
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    result = modifyShiftEndpoint(shift_id, start_time, end_time)
    return jsonify(result)

@shift_bp.route("/shifts/<int:shift_id>", methods=['DELETE'])
def deleteShift(shift_id):
    result = deleteShiftEndpoint(shift_id)
    return jsonify(result)
