# run.py
from flask import Flask
from views.activity_routes import activity_bp
from views.shift_routes import shift_bp
from views.student_routes import student_bp
#from backend import create_app
from __init__ import create_app

app = create_app()

app.register_blueprint(activity_bp, url_prefix = '/api')
app.register_blueprint(shift_bp, url_prefix = '/api')
app.register_blueprint(student_bp, url_prefix = '/api')

if __name__ == '__main__':
    app.run(debug=True)
