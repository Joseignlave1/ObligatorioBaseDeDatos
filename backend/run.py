import sys
from pathlib import Path
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Importa flask-cors
from backend.views.auth_routes import auth_bp
from backend.views.activity_routes import activity_bp
from backend.views.shift_routes import shift_bp
from backend.views.student_routes import student_bp
from backend.__init__ import create_app

# Añade el directorio raíz del proyecto a `sys.path`
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = create_app()

# Habilitar CORS para toda la aplicación
CORS(app, resources={
    r"/api/*": {  # Esto permite CORS para todas las rutas que empiecen con /api/
        "origins": ["http://localhost:3000"],  # Permite solicitudes desde tu frontend React
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos permitidos
        "allow_headers": ["Content-Type", "Authorization"]  # Headers permitidos
    }
})

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(activity_bp, url_prefix='/api')
app.register_blueprint(shift_bp, url_prefix='/api')
app.register_blueprint(student_bp, url_prefix='/api')

# Errores cuando no se envía el token
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        "error": "Missing token"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)