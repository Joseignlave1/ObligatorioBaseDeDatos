from __init__ import get_db_connection

def getAllStudentsEndpoint():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return students

def getStudentById(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    #Consulta parametrizada
    query = "SELECT * FROM alumnos where id = %s"
    cursor.execute(query, (student_id,)) #Pasamos el id de la actividad como una tupla de un solo elemento
    student = cursor.fetchone()
    cursor.close()
    connection.close()
    return student

def addStudentEndpoint(student_id, first_name, last_name, birth_date, contact_phone, email_address): 
    connection = get_db_connection() 
    cursor = connection.cursor() 
    query = "INSERT INTO alumnos (id, first_name, last_name, birth_date, contact_phone, email_address) VALUES (%s, %s, %s, %s, %s, %s)" 
    cursor.execute(query, (student_id, first_name, last_name, birth_date, contact_phone, email_address)) 
    connection.commit() # Confirmamos la transacción 
    cursor.close() 
    connection.close() 
    return {"message": "Alumno agregado exitosamente", "id": student_id}

def modifyStudent(student_id, first_name, last_name, birth_date, contact_phone, email_address):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE alumnos SET first_name = %s, last_name = %s, birth_date = %s, contact_phone = %s, email_addres = %s WHERE id = %s"
    cursor.execute(query, (first_name, last_name, birth_date, contact_phone, email_address))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Alumno modificado exitosamente", "id": student_id}

def deleteStudent(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM alumnos WHERE id = %s"
    cursor.execute(query, (student_id,))
    connection.commit()  # Confirmamos la transacción
    cursor.close()
    connection.close()
    return {"message": "Alumno eliminado exitosamente", "id": student_id}