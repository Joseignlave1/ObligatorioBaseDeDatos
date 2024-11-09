from __init__ import get_db_connection

def getAllShiftsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM turnos")
    shifts = cursor.fetchall()
    cursor.close()
    connection.close()
    return shifts

def getShiftByIdEndpoint(shift_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM turnos WHERE id = %s"
    cursor.execute(query, (shift_id,))
    shift = cursor.fetchone()
    cursor.close()
    connection.close()
    return shift

def addShiftEndpoint(shift_id, start_time, end_time):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO turnos (id, start_time, end_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (shift_id, start_time, end_time))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Turno agregado exitosamente", "id": shift_id}

def modifyShiftEndpoint(shift_id, start_time, end_time):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE turnos SET start_time = %s, end_time = %s WHERE id = %s"
    cursor.execute(query, (start_time, end_time, shift_id))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Turno modificado exitosamente", "id": shift_id}

def deleteShiftEndpoint(shift_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM turnos WHERE id = %s"
    cursor.execute(query, (shift_id,))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Turno eliminado exitosamente", "id": shift_id}
