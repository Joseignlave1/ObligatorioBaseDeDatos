from __init__ import get_db_connection

def getAllActivitiesEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM actividades")
    activities = cursor.fetchall()
    cursor.close()
    connection.close()
    return activities

def getActivityByIdEndpoint(activity_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    #Consulta parametrizada
    query = "SELECT * FROM actividades where id = %s"
    cursor.execute(query, (activity_id,)) #Pasamos el id de la actividad como una tupla de un solo elemento
    activity = cursor.fetchone()
    cursor.close()
    connection.close()
    return activity