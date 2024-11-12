from flask import Flask
from backend.views.user_routes import main

from backend.config.config import JWT_KEY
def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config['JWT_SECRET_KEY'] = JWT_KEY
    return app