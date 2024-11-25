from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from backend.controllers.reports_controller import (
    getReportsIncome,
    getPopularActivities,
    getReportsMostBusyShifts
)

reports_bp = Blueprint('reports_bp', __name__)

@reports_bp.route('/reports/income', methods=['GET'])
@jwt_required()
def income_report():
    try:
        result = getReportsIncome()
        return {"success": True, "data": result}, 200
    except Exception as e:
        return {"success": False, "message": str(e)}, 500
    
@reports_bp.route('/reports/popular/activities', methods=['GET'])
def reports_popular_activities():
    try:
        data = getPopularActivities()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@reports_bp.route('/reports/popular/shifts', methods=['GET'])
def reports_most_busy_shifts():
    try:
        data = getReportsMostBusyShifts()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
