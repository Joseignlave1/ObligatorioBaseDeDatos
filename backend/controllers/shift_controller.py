from ..db_connection import get_db_connection


def getAllShiftsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Devuelve solo HH:mm
    cursor.execute("SELECT id, TIME_FORMAT(hora_inicio, '%H:%i') AS hora_inicio, TIME_FORMAT(hora_fin, '%H:%i') AS hora_fin FROM turnos")
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

    # Convertimos los campos de tipo TIME a cadenas sin segundos
    if shift:
        if "hora_inicio" in shift:
            shift["hora_inicio"] = shift["hora_inicio"].strftime('%H:%M')  # Solo HH:mm
        if "hora_fin" in shift:
            shift["hora_fin"] = shift["hora_fin"].strftime('%H:%M')  # Solo HH:mm

    cursor.close()
    connection.close()
    return shift



def addShiftEndpoint(shift_id, hora_inicio, hora_fin):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO turnos (id, hora_inicio, hora_fin) VALUES (%s, %s, %s)"
    cursor.execute(query, (shift_id, hora_inicio, hora_fin))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Turno agregado exitosamente", "id": shift_id}


def modifyShiftEndpoint(shift_id, hora_inicio, hora_fin):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE turnos SET hora_inicio = %s, hora_fin = %s WHERE id = %s"
    cursor.execute(query, (hora_inicio, hora_fin, shift_id))
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
