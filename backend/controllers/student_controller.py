from ..db_connection import get_db_connection

def getAllStudentsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return students

def getStudentByCi(student_ci):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM alumnos WHERE ci = %s"
    cursor.execute(query, (student_ci,))
    student = cursor.fetchone()
    cursor.close()
    connection.close()
    return student

def addStudentEndpoint(student_ci, nombre, apellido, fecha_nacimiento, telefono, correo): 
    connection = get_db_connection() 
    cursor = connection.cursor() 
    query = "INSERT INTO alumnos (ci, nombre, apellido, fecha_nacimiento, telefono, correo) VALUES (%s, %s, %s, %s, %s, %s)" 
    cursor.execute(query, (student_ci, nombre, apellido, fecha_nacimiento, telefono, correo)) 
    connection.commit()
    cursor.close() 
    connection.close() 
    return {"message": "Alumno agregado exitosamente", "ci": student_ci}

def modifyStudent(student_ci, nombre, apellido, fecha_nacimiento, telefono, correo):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE alumnos SET nombre = %s, apellido = %s, fecha_nacimiento = %s, telefono = %s, correo = %s WHERE ci = %s"
    cursor.execute(query, (nombre, apellido, fecha_nacimiento, telefono, correo, student_ci))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Alumno modificado exitosamente", "ci": student_ci}

def deleteStudent(student_ci):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM alumnos WHERE ci = %s"
    cursor.execute(query, (student_ci,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Alumno eliminado exitosamente", "ci": student_ci}
