from mysql.connector import connect
from werkzeug.security import generate_password_hash, check_password_hash
from ..db_connection import get_db_connection

def registerEndpoint(email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    #Para no almacenar la contraseña en texto plano en la BD, generamos un hash y almacenamos el hash de la contraseña
    #Por defecto werkzeug utiliza el metodo scrypt para hacer el hashing, no estaba soportado en mi version de python por eso lo cambie

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    query = "INSERT INTO login(correo, contraseña) VALUES (%s,%s)"
    cursor.execute(query, (email, hashed_password))

    connection.commit()
    rows_affected = cursor.rowcount

    if(rows_affected > 0):
        cursor = connection.cursor(dictionary=True)

        query = "SELECT correo FROM login WHERE correo = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
    else:
        user = None
    #recuperamos el usuario para asi ponerlo en la creacion del token jwt
    cursor.close()
    connection.close()
    return user

def loginEndpoint(email, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM login WHERE correo = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    #Comparamos el hash de la contraseña insertada en el login, con el hash de la contraseña pasada por parametro
    if user and check_password_hash(user['contraseña'], password):
        return user
    else:
        return None




