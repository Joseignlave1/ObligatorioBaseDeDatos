from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from controllers.activity_controller import getAllActivitiesEndpoint, getActivityByIdEndpoint

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route("/activities/all", methods = ['GET'])
@jwt_required()
def getAllActivities():
    activities = getActivitiesEndpoint()
    if activities:
        return jsonify(activities)
    else:
        return jsonify({'activity': 'There are no activities'}), 404

@activity_bp.route("/activities/<int:activity_id>", methods = ['GET'])
@jwt_required()
def getActivityById(activity_id):
    activity = getActivityByIdEndpoint(activity_id)
    #si existe actividad con esa id
    if activity:
        return jsonify(activity)
    else:
        return jsonify({'activity' : 'Activity not found '}), 404