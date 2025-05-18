from config.db import get_db_connection

class Teacher:
    @staticmethod
    def get_all():
        """Get all teachers along with their department name."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT teachers.*, departments.name as department_name
                FROM teachers
                LEFT JOIN departments ON teachers.department_id = departments.id
            """)
            teachers = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching teachers: {e}")
            teachers = []
        finally:
            cursor.close()
            conn.close()
        return teachers

    @staticmethod
    def add_teacher(first_name, last_name, department_id, email, phone):
        """Add a new teacher to the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teachers (first_name, last_name, department_id, email, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, department_id, email, phone))
            conn.commit()
            return True  # Return True on success
        except Exception as e:
            print(f"Error adding teacher: {e}")
            return False  # Return False on failure
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(teacher_id):
        """Get a teacher by their ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT teachers.*, departments.name as department_name
                FROM teachers
                LEFT JOIN departments ON teachers.department_id = departments.id
                WHERE teachers.id = %s
            """, (teacher_id,))
            teacher = cursor.fetchone()
        except Exception as e:
            print(f"Error fetching teacher with ID {teacher_id}: {e}")
            teacher = None
        finally:
            cursor.close()
            conn.close()
        return teacher

    @staticmethod
    def update_teacher(teacher_id, first_name, last_name, department_id, email, phone):
        """Update a teacher's details."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teachers
                SET first_name = %s, last_name = %s, department_id = %s, email = %s, phone = %s
                WHERE id = %s
            """, (first_name, last_name, department_id, email, phone, teacher_id))
            conn.commit()
            return True  # Return True on success
        except Exception as e:
            print(f"Error updating teacher with ID {teacher_id}: {e}")
            return False  # Return False on failure
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_teacher(teacher_id):
        """Delete a teacher by their ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            conn.commit()
            return True  # Return True on success
        except Exception as e:
            print(f"Error deleting teacher with ID {teacher_id}: {e}")
            return False  # Return False on failure
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_email(email):
        """Get a teacher by their email."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM teachers WHERE email = %s
            """, (email,))
            teacher = cursor.fetchone()
        except Exception as e:
            print(f"Error fetching teacher with email {email}: {e}")
            teacher = None
        finally:
            cursor.close()
            conn.close()
        return teacher

    @staticmethod
    def get_by_name(first_name, last_name):
        """Get a teacher by their first and last name."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM teachers WHERE first_name = %s AND last_name = %s
            """, (first_name, last_name))
            teacher = cursor.fetchone()
        except Exception as e:
            print(f"Error fetching teacher with name {first_name} {last_name}: {e}")
            teacher = None
        finally:
            cursor.close()
            conn.close()
        return teacher