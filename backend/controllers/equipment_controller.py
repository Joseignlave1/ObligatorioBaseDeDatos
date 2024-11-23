from ..db_connection import get_db_connection
import mysql.connector


def getEquipmentByActivityEndpoint(activity_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM equipamiento WHERE id_actividad = %s"
    cursor.execute(query, (activity_id,))
    equipment = cursor.fetchall()
    cursor.close()
    connection.close()
    return equipment


def addEquipmentToActivityEndpoint(activity_id, description, cost):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO equipamiento (id_actividad, descripcion, costo)
        VALUES (%s, %s, %s)
    """
    try:

        cursor.execute(query, (activity_id, description, cost))
        connection.commit()

        # Para verificar si se afectaron filas
        rows_affected = cursor.rowcount
        print(f"Filas afectadas: {rows_affected}")
        return rows_affected > 0
    except mysql.connector.Error as err:
        # Para mostrar errores relacionados con la base de datos
        print(f"Error de base de datos: {err}")
        return False
    finally:
        cursor.close()
        connection.close()


def modifyActivityEquipmentEndpoint(equipment_id, activity_id, description, cost):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            UPDATE equipamiento
            SET descripcion = %s, costo = %s
            WHERE id = %s AND id_actividad = %s
        """
        cursor.execute(query, (description, cost, equipment_id, activity_id))
        connection.commit()

        # Para verificar cuántas filas fueron afectadas
        rows_affected = cursor.rowcount

        cursor.close()
        connection.close()

        # Retornar True si se actualizó al menos una fila
        return rows_affected > 0

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return False


def deleteEquipmentEndpoint(equipment_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "DELETE FROM equipamiento WHERE id = %s"
        cursor.execute(query, (equipment_id,))
        connection.commit()

        rows_affected = cursor.rowcount

        cursor.close()
        connection.close()

        return rows_affected > 0

    except Exception as e:
        print(f"Error al ejecutar la consulta de eliminación: {e}")
        return False
