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
    # Consulta parametrizada
    query = "SELECT * FROM actividades where id = %s"
    cursor.execute(query, (activity_id,))  # Pasamos el id de la actividad como una tupla de un solo elemento
    activity = cursor.fetchone()
    cursor.close()
    connection.close()
    return activity


def modifyActivityEndpoint(activity_id, description, cost, minimum_age):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        UPDATE actividades 
        SET descripcion = %s, costo = %s, edad_minima = %s 
        WHERE id = %s
    """
    cursor.execute(query, (description, cost, minimum_age, activity_id))
    connection.commit()  # Asegurarse de guardar los cambios
    cursor.close()
    connection.close()
    return {"message": "Actividad modificada exitosamente", "id": activity_id}


def addActivityEndpoint(description, cost, minimumAge):
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


def deleteActivityEndpoint(activity_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Primero verificamos si la actividad existe
    query_check = "SELECT * FROM actividades WHERE id = %s"
    cursor.execute(query_check, (activity_id,))
    activity = cursor.fetchone()

    if not activity:
        cursor.close()
        connection.close()
        return None  # Si no existe, devolvemos None para indicar que no fue encontrada

    # Si existe, procedemos a eliminarla
    query_delete = "DELETE FROM actividades WHERE id = %s"
    cursor.execute(query_delete, (activity_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return {"message": "Actividad eliminada exitosamente", "id": activity_id}

