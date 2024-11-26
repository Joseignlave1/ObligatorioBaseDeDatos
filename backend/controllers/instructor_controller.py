from venv import create
from ..db_connection import get_db_connection


def getAllInstructorsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM instructores")
    instructors = cursor.fetchall()
    cursor.close()
    connection.close()
    return instructors


def getInstructorByIdEndpoint(instructor_ci):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM instructores WHERE ci = %s"
    cursor.execute(query, (instructor_ci,))
    instructor = cursor.fetchone()
    cursor.close()
    connection.close()
    return instructor


def addInstructorEndpoint(ci, nombre, apellido):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO instructores (ci, nombre, apellido) VALUES (%s, %s, %s)"
    cursor.execute(query, (ci, nombre, apellido))
    connection.commit()
    cursor.close()
    connection.close()
    return cursor.rowcount > 0


def modifyInstructorEndpoint(instructor_ci, nombre, apellido):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE instructores SET nombre = %s, apellido = %s WHERE ci = %s"
    cursor.execute(query, (nombre, apellido, instructor_ci))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Instructor modificado exitosamente", "ci": instructor_ci} 


def deleteInstructorEndpoint(instructor_ci):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM instructores WHERE ci = %s"
    cursor.execute(query, (instructor_ci,))
    connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    connection.close()
    return rows_affected > 0
