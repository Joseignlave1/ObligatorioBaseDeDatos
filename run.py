# run.py
from flask import Flask
from backend.views.activity_routes import activity_bp
from backend import create_app

app = create_app()

app.register_blueprint(activity_bp, url_prefix = '/api')

if __name__ == '__main__':
    app.run(debug=True)
