from db import get_db_connection

class Car:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        cursor.close()
        conn.close()
        return cars

    @staticmethod
    def add_car(car_type, average_cost_per_day, available_count):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cars (car_type, average_cost_per_day, available_count)
            VALUES (%s, %s, %s)
        """, (car_type, average_cost_per_day, available_count))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_id(car_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        cursor.close()
        conn.close()
        return car

    @staticmethod
    def update_car(car_id, car_type, average_cost_per_day, available_count):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cars
            SET car_type = %s, average_cost_per_day = %s, available_count = %s
            WHERE id = %s
        """, (car_type, average_cost_per_day, available_count, car_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_car(car_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_all_types():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT type FROM cars")  # Assuming 'cars' table has a 'type' column
        car_types = cursor.fetchall()
        cursor.close()
        connection.close()
        return car_types
