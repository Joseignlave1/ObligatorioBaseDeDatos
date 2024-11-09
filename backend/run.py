# run.py
import sys
from pathlib import Path

# Añade el directorio raíz del proyecto a `sys.path`
sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify
from views.activity_routes import activity_bp
from backend import create_app
from flask_jwt_extended import JWTManager
app = create_app()
jwt = JWTManager(app)

app.register_blueprint(activity_bp, url_prefix = '/api')

#Errores cuando no se envia el token

@jwt.unauthorized_loader

def unauthorized_response(callback):
    return jsonify({
        "error": "Missing token"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)
