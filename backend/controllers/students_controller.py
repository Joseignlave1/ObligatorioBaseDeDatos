from ..db_connection import get_db_connection

def registerUserEndpoint(email, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO login(email, password) VALUES (%s,%s)"
    cursor.execute(query, (email, password))

    connection.commit()
    rows_affected = cursor.rowcount

    if(rows_affected > 0):
        cursor = connection.cursor(dictionary=True)

        query = "SELECT email FROM login WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
    else:
        user = None
    #recuperamos el usuario para asi ponerlo en la creacion del token jwt
    cursor.close()
    connection.close()
    return user

