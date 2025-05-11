from db import get_db_connection

class InternType:
    # Get all internship types
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM intern_types")  # Assuming your table is named 'intern_types'
        intern_types = cursor.fetchall()
        cursor.close()
        conn.close()
        return intern_types

    # Add a new internship type
    @staticmethod
    def add_intern_type(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO intern_types (name)
            VALUES (%s)
        """, (name,))
        conn.commit()
        cursor.close()
        conn.close()

    # Get internship type by ID
    @staticmethod
    def get_by_id(intern_type_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM intern_types WHERE id = %s", (intern_type_id,))
        intern_type = cursor.fetchone()
        cursor.close()
        conn.close()
        return intern_type

    # Update an internship type
    @staticmethod
    def update_intern_type(intern_type_id, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE intern_types
            SET name = %s
            WHERE id = %s
        """, (name, intern_type_id))
        conn.commit()
        cursor.close()
        conn.close()

    # Delete an internship type
    @staticmethod
    def delete_intern_type(intern_type_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM intern_types WHERE id = %s", (intern_type_id,))
        conn.commit()
        cursor.close()
        conn.close()
