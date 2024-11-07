# app/routes.py
from flask import Blueprint
import mysql.connector
main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return "<h1>Hello, World!</h1>"

@main.route("/users")
def usersFromDatabase():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='rootpassword',
            host='127.0.0.1',
            database='parte2Practico2BaseDeDatos'
        )
        cursor = cnx.cursor()
        query = "SELECT * FROM usuarioPruebaPractico2"
        cursor.execute(query)

        # Construir la respuesta HTML
        html = "<h1>Usuarios:</h1><ul>"
        for el in cursor:
            # Crear un elemento de lista por cada usuario
            html += f"<li>{el}</li>"
        html += "</ul>"

        cursor.close()
        cnx.close()

        return html

    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return "<h1>Error al conectar a la base de datos</h1>", 500
