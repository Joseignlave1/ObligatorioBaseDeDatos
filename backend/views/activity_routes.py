from flask import Blueprint, jsonify
from backend.controllers.activity_controller import getActivitiesEndpoint, getActivityByIdEndpoint

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route("/activities/all", methods = ['GET'])

def getAllActivities():
    activities = getActivitiesEndpoint()
    return jsonify(activities)

@activity_bp.route("/activities/<int:activity_id>", methods = ['GET'])

def getActivityById(activity_id):
    activity = getActivityByIdEndpoint(activity_id)
    #si existe actividad con esa id
    if activity:
        return jsonify(activity)
    else:
        return jsonify({'activity' : 'Activity not found '}), 404