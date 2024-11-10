from flask import Flask
from views.user_routes import main

##Funcion encargada de realizar la conexion con la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        user = DB_CONFIG['user'],
        password = DB_CONFIG['password'],
        host = DB_CONFIG['host'],
        database = DB_CONFIG['database']
    )

    return connection

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    return app