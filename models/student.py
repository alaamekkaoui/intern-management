from config.db import get_db_connection

class Student:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT students.*, 
                   internships.start_date AS internship_start, internships.end_date AS internship_end, 
                   intern_types.name AS intern_type_name, 
                   teachers.first_name AS teacher_first_name, teachers.last_name AS teacher_last_name
            FROM students
            LEFT JOIN internships ON students.internship_id = internships.id
            LEFT JOIN intern_types ON internships.intern_type_id = intern_types.id
            LEFT JOIN teachers ON students.teacher_id = teachers.id
        """)
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

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
    def get_by_id(student_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student

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
