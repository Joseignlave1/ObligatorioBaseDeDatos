from flask import Blueprint, jsonify
from backend.controllers.activity_controller import getActivities

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route("/activity", methods = ['GET'])

def getAllActivities():
    activities = getActivities()
    return jsonify(activities)