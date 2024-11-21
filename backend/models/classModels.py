from ..db_connection import get_db_connection

def getClassesWithInstructorInShift(ci_instructor, id_shift):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clase WHERE ci_instructor = %s and id_turno = %s"
    cursor.execute(query, (ci_instructor, id_shift))
    classes = cursor.fetchone()
    cursor.close()
    connection.close()
    return classes
