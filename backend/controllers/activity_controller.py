from venv import create

from ..db_connection import get_db_connection

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

def modifyActivityEndpoint(activity_id, description, cost):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE actividades SET descripcion = %s, costo = %s WHERE id = %s"
    cursor.execute(query, (description, cost, activity_id))
    updatedActivity = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Turno modificado exitosamente", "id": activity_id}



def addActivity(description, cost, minimumAge):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO actividades(descripcion, costo, edad_minima) VALUES (%s, %s, %s)"
    cursor.execute(query, (description, cost, minimumAge))
    createdActivityId = cursor.lastrowid
    createdActivity = {
        "id": createdActivityId,
        "description": description,
        "cost": cost,
        "minimumAge": minimumAge
    }
    connection.commit()
    cursor.close()
    connection.close()
    return createdActivity

