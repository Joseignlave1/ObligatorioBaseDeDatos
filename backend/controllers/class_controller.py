from ..db_connection import get_db_connection

def getAllClassesEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clase")
    classes = cursor.fetchall()
    cursor.close()
    connection.close()
    return classes

def getClassByIdEndpoint(class_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clase WHERE id = %s"
    cursor.execute(query, (class_id,))
    oneClass = cursor.fetchone()
    cursor.close()
    connection.close()
    return oneClass

def addClassEndpoint(ci_instructor, id_activity, id_shift, dictated): 
    connection = get_db_connection() 
    cursor = connection.cursor() 
    query = "INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada) VALUES (%s, %s, %s, %s)" 
    cursor.execute(query, (ci_instructor, id_activity, id_shift, dictated)) 
    connection.commit()
    cursor.close() 
    connection.close() 
    return {"message": f"La clase ha sido agregada correctamente"}

def modifyClassEndpoint(class_id, ci_instructor, id_activity, id_shift, dictated):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE clase SET ci_instructor = %s, id_actividad = %s, id_turno = %s, dictada = %s WHERE id = %s"
    cursor.execute(query, (ci_instructor, id_activity, id_shift, dictated, class_id))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Class successfully updated", "id": class_id}

def deleteClassEndpoint(class_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM clase WHERE id = %s"
    cursor.execute(query, (class_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"La clase ha sido eliminada"}


