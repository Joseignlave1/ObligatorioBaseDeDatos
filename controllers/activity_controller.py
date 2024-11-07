from backend import get_db_connection

def getActivities():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM actividades")
    activities = cursor.fetchall()
    cursor.close()
    connection.close()
    return activities