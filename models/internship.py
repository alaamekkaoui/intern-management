from config.db import get_db_connection

class Internship:
    @staticmethod
    def get_all():
        """Fetch all internships with teacher, car, and intern_type details."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT internships.*, teachers.first_name, teachers.last_name, teachers.email, 
                       cars.model AS car_model, cars.license_plate, intern_types.name AS intern_type
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
            # First verify if teacher exists - could be ID or full name
            if teacher_id:
                try:
                    # Try to use it as an ID first
                    teacher_id = int(teacher_id)
                    cursor.execute("SELECT id FROM teachers WHERE id = %s", (teacher_id,))
                    cursor.fetchone()  # Always fetch result to clear buffer
                except (ValueError, TypeError):
                    # If not a valid ID, try to find by full name
                    if isinstance(teacher_id, str):
                        names = teacher_id.split()
                        if len(names) >= 2:
                            first_name = names[0]
                            last_name = ' '.join(names[1:])
                            cursor.execute("""
                                SELECT id FROM teachers 
                                WHERE first_name = %s AND last_name = %s
                            """, (first_name, last_name))
                            result = cursor.fetchone()
                            if result:
                                teacher_id = result[0]
                            else:
                                print(f"Teacher {teacher_id} not found")
                                return False
                        else:
                            print(f"Invalid teacher name format: {teacher_id}")
                            return False
                    else:
                        print(f"Invalid teacher ID/name format: {teacher_id}")
                        return False

            # Verify if intern_type_id exists
            if intern_type_id:
                try:
                    intern_type_id = int(intern_type_id)
                    cursor.execute("SELECT id FROM intern_types WHERE id = %s", (intern_type_id,))
                    cursor.fetchone()  # Always fetch result to clear buffer
                    if not cursor.rowcount:
                        print(f"Intern type ID {intern_type_id} does not exist")
                        return False
                except (ValueError, TypeError):
                    print(f"Invalid intern type ID format: {intern_type_id}")
                    return False

            # Verify if car_id exists
            if car_id:
                try:
                    car_id = int(car_id)
                    cursor.execute("SELECT id FROM cars WHERE id = %s", (car_id,))
                    cursor.fetchone()  # Always fetch result to clear buffer
                    if not cursor.rowcount:
                        print(f"Car ID {car_id} does not exist")
                        return False
                except (ValueError, TypeError):
                    print(f"Invalid car ID format: {car_id}")
                    return False

            # Update the internship with NULL handling
            cursor.execute("""
                UPDATE internships
                SET teacher_id = %s,
                    intern_type_id = %s,
                    car_id = %s,
                    start_date = %s,
                    end_date = %s
                WHERE id = %s
            """, (
                teacher_id if teacher_id else None,
                intern_type_id if intern_type_id else None,
                car_id if car_id else None,
                start_date,
                end_date,
                internship_id
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating internship: {e}")
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def delete_internship(internship_id):
        """Delete an internship after handling related records."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # First update any students associated with this internship
            cursor.execute("UPDATE students SET internship_id = NULL WHERE internship_id = %s", (internship_id,))
            
            # Then delete the internship
            cursor.execute("DELETE FROM internships WHERE id = %s", (internship_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting internship: {e}")
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_id(internship_id):
        connection = get_db_connection()  # Make sure this function is defined correctly
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM internships WHERE id = %s', (internship_id,))
        internship = cursor.fetchone()
        connection.close()
        return internship

    @staticmethod
    def is_car_available(car_id, start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM internships
            WHERE car_id = %s
            AND status NOT IN ('canceled', 'done')
            AND (
                (start_date <= %s AND end_date >= %s) OR
                (start_date <= %s AND end_date >= %s) OR
                (start_date >= %s AND end_date <= %s)
            )
        """, (car_id, start_date, start_date, end_date, end_date, start_date, end_date))
        (count,) = cursor.fetchone()
        cursor.close()
        conn.close()
        return count == 0

    @staticmethod
    def get_by_teacher_id(teacher_id):
        """Fetch all internships for a specific teacher, with car and intern_type details."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT internships.*, cars.model AS car_model, cars.license_plate, intern_types.name AS intern_type
                FROM internships
                LEFT JOIN cars ON internships.car_id = cars.id
                LEFT JOIN intern_types ON internships.intern_type_id = intern_types.id
                WHERE internships.teacher_id = %s
            """, (teacher_id,))
            internships = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching internships for teacher {teacher_id}: {e}")
            internships = []
        finally:
            cursor.close()
            conn.close()
        return internships

    @staticmethod
    def get_by_car_id(car_id):
        """Fetch all internships for a specific car, with teacher and intern_type details."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT internships.*, teachers.first_name, teachers.last_name, teachers.email, intern_types.name AS intern_type
                FROM internships
                JOIN teachers ON internships.teacher_id = teachers.id
                LEFT JOIN intern_types ON internships.intern_type_id = intern_types.id
                WHERE internships.car_id = %s
            """, (car_id,))
            internships = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching internships for car {car_id}: {e}")
            internships = []
        finally:
            cursor.close()
            conn.close()
        return internships