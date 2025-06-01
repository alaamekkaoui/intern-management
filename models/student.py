from config.db import get_db_connection

class Student:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.*,
                i.id as internship_id,
                i.start_date as internship_start_date,
                i.end_date as internship_end_date,
                it.id as intern_type_id,
                it.name as intern_type_name,
                t.id as teacher_id,
                t.first_name as teacher_first_name,
                t.last_name as teacher_last_name
            FROM students s
            LEFT JOIN internships i ON s.internship_id = i.id
            LEFT JOIN intern_types it ON i.intern_type_id = it.id
            LEFT JOIN teachers t ON i.teacher_id = t.id
            ORDER BY s.last_name, s.first_name
        """)
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

    @staticmethod
    def get_by_id(student_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.*,
                i.id as internship_id,
                i.start_date as internship_start_date,
                i.end_date as internship_end_date,
                it.id as intern_type_id,
                it.name as intern_type_name,
                t.id as teacher_id,
                t.first_name as teacher_first_name,
                t.last_name as teacher_last_name
            FROM students s
            LEFT JOIN internships i ON s.internship_id = i.id
            LEFT JOIN intern_types it ON i.intern_type_id = it.id
            LEFT JOIN teachers t ON i.teacher_id = t.id
            WHERE s.id = %s
        """, (student_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student

    @staticmethod
    def add_student(first_name, last_name, email=None, phone=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO students (first_name, last_name, email, phone)
            VALUES (%s, %s, %s, %s)
            """,
            (first_name, last_name, email, phone)
        )
        student_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return student_id

    @staticmethod
    def assign_internship(student_id, internship_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get the teacher_id from the internship
        cursor.execute("SELECT teacher_id FROM internships WHERE id = %s", (internship_id,))
        row = cursor.fetchone()
        teacher_id = row[0] if row else None
        # Assign internship and teacher to student
        cursor.execute(
            """
            UPDATE students SET internship_id = %s, teacher_id = %s WHERE id = %s
            """,
            (internship_id, teacher_id, student_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def import_from_xlsx(rows):
        # rows: list of dicts with keys: first_name, last_name, email, phone
        conn = get_db_connection()
        cursor = conn.cursor()
        for row in rows:
            cursor.execute(
                """
                INSERT INTO students (first_name, last_name, email, phone)
                VALUES (%s, %s, %s, %s)
                """,
                (row.get('first_name'), row.get('last_name'), row.get('email'), row.get('phone'))
            )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_student(student_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_student(student_id, first_name, last_name, email, phone, internship_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if internship_id:
            # Get the teacher_id from the internship
            cursor.execute("SELECT teacher_id FROM internships WHERE id = %s", (internship_id,))
            row = cursor.fetchone()
            teacher_id = row[0] if row else None
            cursor.execute(
                """
                UPDATE students SET first_name = %s, last_name = %s, email = %s, phone = %s, internship_id = %s, teacher_id = %s WHERE id = %s
                """,
                (first_name, last_name, email, phone, internship_id, teacher_id, student_id)
            )
        else:
            cursor.execute(
                """
                UPDATE students SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE id = %s
                """,
                (first_name, last_name, email, phone, student_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
