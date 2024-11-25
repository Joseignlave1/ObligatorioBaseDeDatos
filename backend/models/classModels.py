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

from datetime import datetime, timedelta

def getShiftByIdForModify(shift_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM turnos WHERE id = %s"
    cursor.execute(query, (shift_id,))
    shift = cursor.fetchone()

    if shift:
        # Convertir hora_inicio
        if "hora_inicio" in shift:
            if isinstance(shift["hora_inicio"], timedelta):  # Si es timedelta
                total_seconds = int(shift["hora_inicio"].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                shift["hora_inicio"] = f"{hours:02}:{minutes:02}"
            elif hasattr(shift["hora_inicio"], 'strftime'):  # Si es datetime.time
                shift["hora_inicio"] = shift["hora_inicio"].strftime('%H:%M')

        # Convertir hora_fin
        if "hora_fin" in shift:
            if isinstance(shift["hora_fin"], timedelta):  # Si es timedelta
                total_seconds = int(shift["hora_fin"].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                shift["hora_fin"] = f"{hours:02}:{minutes:02}"
            elif hasattr(shift["hora_fin"], 'strftime'):  # Si es datetime.time
                shift["hora_fin"] = shift["hora_fin"].strftime('%H:%M')

    cursor.close()
    connection.close()
    return shift
