# run.py
import sys
from pathlib import Path
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from backend.views.auth_routes import auth_bp
from backend.views.activity_routes import activity_bp
from backend.views.shift_routes import shift_bp
from backend.views.student_routes import student_bp
from backend.views.class_routes import class_bp
from backend.views.auth_routes import auth_bp
from backend.views.equipment_routes import equipment_bp

from backend.views.instructor_routes import instructor_bp



# Añade el directorio raíz del proyecto a `sys.path`
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = create_app()
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix = '/api')
app.register_blueprint(activity_bp, url_prefix = '/api')
app.register_blueprint(shift_bp, url_prefix = '/api')
app.register_blueprint(student_bp, url_prefix = '/api')
app.register_blueprint(class_bp, url_prefix = '/api')
app.register_blueprint(equipment_bp, url_prefix="/api")
app.register_blueprint(instructor_bp, url_prefix="/api")


#Errores cuando no se envia el token
@jwt.unauthorized_loader

def unauthorized_response(callback):
    return jsonify({
        "error": "Missing token"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)
