from db import get_db_connection

class Internship:
    @staticmethod
    def get_all():
        """Fetch all internships with teacher, car, and intern_type details."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT internships.*, teachers.first_name, teachers.last_name, teachers.email, 
                       cars.model AS car_model, cars.plate_number, intern_types.name AS intern_type
                FROM internships
                JOIN teachers ON internships.teacher_id = teachers.id
                LEFT JOIN cars ON internships.car_id = cars.id
                LEFT JOIN intern_types ON internships.intern_type_id = intern_types.id
            """)
            internships = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching internships: {e}")
            internships = []
        finally:
            cursor.close()
            conn.close()
        return internships

    @staticmethod
    def add_internship(teacher_id, intern_type_id, car_id, start_date, end_date):
        """Add a new internship with the intern_type_id as a foreign key."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO internships (teacher_id, car_id, start_date, end_date, status, intern_type_id)
                VALUES (%s, %s, %s, %s, 'pending', %s)
            """, (teacher_id, car_id, start_date, end_date, intern_type_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding internship: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_status(internship_id, status):
        """Update the status of an internship."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE internships
                SET status = %s
                WHERE id = %s
            """, (status, internship_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating internship status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_internship(internship_id, teacher_id, intern_type_id, car_id, start_date, end_date):
        """Update internship details, including intern_type_id as a foreign key."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE internships
                SET teacher_id = %s, intern_type_id = %s, car_id = %s, start_date = %s, end_date = %s
                WHERE id = %s
            """, (teacher_id, intern_type_id, car_id, start_date, end_date, internship_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating internship: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_internship(internship_id):
        """Delete an internship."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM internships WHERE id = %s", (internship_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting internship: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(internship_id):
        connection = get_db_connection()  # Make sure this function is defined correctly
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM internships WHERE id = %s', (internship_id,))
        internship = cursor.fetchone()
        connection.close()
        return internship