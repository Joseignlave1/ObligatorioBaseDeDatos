from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.controllers.activity_controller import getAllActivitiesEndpoint, getActivityByIdEndpoint, modifyActivityEndpoint, addActivityEndpoint, deleteActivityEndpoint

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route("/activities/all", methods = ['GET'])
@jwt_required()
def getAllActivities():
    activities = getAllActivitiesEndpoint()
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

@activity_bp.route("/activities/<int:activity_id>", methods=['PUT'])
@jwt_required()
def modifyActivityById(activity_id):
    data = request.json
    description = data.get("description")
    cost = data.get("cost")
    minimum_age = data.get("minimumAge")

    updatedActivity = modifyActivityEndpoint(activity_id, description, cost, minimum_age)

    if updatedActivity:
        return jsonify(updatedActivity)
    else:
        return jsonify({'activity': 'Activity not found'}), 404

@activity_bp.route("/activities", methods = ['POST'])
@jwt_required()
def createActivity():
    data = request.json
    description = data.get("description")
    cost = float(data.get("cost"))
    minimumAge = int(data.get("minimumAge"))
    createdActivity = addActivityEndpoint(description, cost, minimumAge)

    if createdActivity:
        return jsonify({'Activity' : 'The activity was created succesfully'}, createdActivity), 201
    else:
        return jsonify({'activity' : 'There was a problem creating the activity'}), 400

@activity_bp.route("/activities/<int:activity_id>", methods=['DELETE'])
@jwt_required()
def deleteActivity(activity_id):
    deletedActivity = deleteActivityEndpoint(activity_id)
    if deletedActivity:
        return jsonify(deletedActivity), 200
    else:
        return jsonify({"activity": "Activity not found"}), 404
