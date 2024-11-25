from ..db_connection import get_db_connection

def getReportsIncome():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT 
        a.descripcion AS actividad,
        COALESCE(SUM(e.costo), 0.00) AS ingresos_totales
    FROM alumno_clase ac
    INNER JOIN clase c ON ac.id_clase = c.id
    INNER JOIN actividades a ON c.id_actividad = a.id
    LEFT JOIN equipamiento e ON ac.id_equipamiento = e.id
    GROUP BY a.descripcion
    ORDER BY ingresos_totales DESC
    """
    cursor.execute(query)
    incomes = cursor.fetchall()
    cursor.close()
    connection.close()
    return incomes

def getPopularActivities():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            a.descripcion AS actividad,
            COUNT(ac.id_clase) AS inscripciones
        FROM actividades a
        LEFT JOIN clase c ON a.id = c.id_actividad
        LEFT JOIN alumno_clase ac ON c.id = ac.id_clase
        GROUP BY a.id, a.descripcion
        ORDER BY inscripciones DESC;
    """

    cursor.execute(query)
    result = cursor.fetchall()
    # Formateamos los resultados
    activities = [{"actividad": row[0], "inscripciones": row[1]} for row in result]
    cursor.close()
    connection.close()
    return activities

def getReportsMostBusyShifts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT 
            t.id AS turno_id,  -- Agregar la ID del turno
            t.hora_inicio,
            t.hora_fin,
            COUNT(ac.id_clase) AS inscripciones
        FROM turnos t
        LEFT JOIN clase c ON t.id = c.id_turno
        LEFT JOIN alumno_clase ac ON c.id = ac.id_clase
        GROUP BY t.id, t.hora_inicio, t.hora_fin
        ORDER BY inscripciones DESC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    shifts = [{"turno_id": row['turno_id'], "hora_inicio": row['hora_inicio'], "hora_fin": row['hora_fin'], "inscripciones": row['inscripciones']} for row in result]
    cursor.close()
    connection.close()
    return shifts
