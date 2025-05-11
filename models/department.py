import traceback
from db import get_db_connection

class Department:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        cursor.close()
        conn.close()
        return departments
    @staticmethod
    def add_department(department_name):
            # Get database connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if the department already exists
            cursor.execute("SELECT * FROM departments WHERE name = %s", (department_name,))
            existing_department = cursor.fetchone()
            if existing_department:
                return False  # Department already exists
            
            # Proceed to add the department
            cursor.execute("INSERT INTO departments (name) VALUES (%s)", (department_name,))
            conn.commit() 
            cursor.close()
            conn.close()
            return True  
            
    @staticmethod
    def update_department(department_id, new_department_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE departments
            SET name = %s
            WHERE id = %s
        """, (new_department_name, department_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_department(department_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM departments WHERE id = %s", (department_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_id(department_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM departments WHERE id = %s", (department_id,))
        department = cursor.fetchone()  # Returns a single row
        cursor.close()
        conn.close()
        return department
    
    @staticmethod
    def get_by_name(department_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM departments WHERE name = %s", (department_name,))
        department = cursor.fetchone()  # Returns a single row or None
        cursor.close()
        conn.close()
        return department
