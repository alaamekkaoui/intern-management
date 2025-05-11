from db import get_db_connection

class Internship:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM internships")
        internships = cursor.fetchall()
        cursor.close()
        conn.close()
        return internships

    @staticmethod
    def add_internship(teacher_id, intern_type, car_needed, start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO internships (teacher_id, intern_type, car_needed, start_date, end_date, state)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """, (teacher_id, intern_type, car_needed, start_date, end_date))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_internship(internship_id, state):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE internships
            SET state = %s
            WHERE id = %s
        """, (state, internship_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def cancel_internship(internship_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE internships
            SET state = 'canceled'
            WHERE id = %s
        """, (internship_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_internship(internship_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM internships WHERE id = %s", (internship_id,))
        conn.commit()
        cursor.close()
        conn.close()