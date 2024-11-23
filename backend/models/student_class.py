from ..db_connection import get_db_connection

def getClassesWithStudent(ci_student):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clase JOIN alumno_clase ON clase.id = alumno_clase.id_clase WHERE ci_alumno = %s"
    cursor.execute(query, (ci_student,))
    classes = cursor.fetchall()
    cursor.close()
    connection.close()
    return classes
