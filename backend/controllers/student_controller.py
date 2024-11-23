from ..db_connection import get_db_connection
from datetime import datetime
#Formatear las fechas para que el backend las envie en formato YYYY/MM/DD

def format_date(date):
    return date.strftime('%Y-%m-%d') if date else None

def getAllStudentsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    students = cursor.fetchall()
    cursor.close()
    connection.close()

    for student in students:
        if student['fecha_nacimiento']:
            student['fecha_nacimiento'] = format_date(student['fecha_nacimiento'])
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

def addStudentToClass(id_clase, ci_alumno, id_equipamiento):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento) VALUES (%s, %s, %s)"
    cursor.execute(query, (id_clase, ci_alumno, id_equipamiento))
    connection.commit()
    cursor.close() 
    connection.close() 
    return {"message": f"Student with CI {ci_alumno} added to class {id_clase}"}

def deleteStudentFromClassEndpoint(id_clase, ci_alumno):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE from alumno_clase WHERE id_clase = %s and ci_alumno = %s"
    cursor.execute(query, (id_clase, ci_alumno))
    connection.commit()
    if cursor.rowcount == 0:
        return {"message": f"No record found for Student with CI {ci_alumno} in class {id_clase}"}, 404
    cursor.close()
    connection.close()
    return {"message": f"Student with CI {ci_alumno} deleted from class {id_clase}"}