from config.db import get_db_connection

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
    def add_car(name, model, car_type, brand, license_plate, average_cost_per_day, available_count):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cars (name, model, car_type, brand, license_plate, average_cost_per_day, available_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, model, car_type, brand, license_plate, average_cost_per_day, available_count))
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
    def update_car(car_id, name, car_type, brand, license_plate, average_cost_per_day, available_count):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cars
            SET name = %s,
                car_type = %s,
                brand = %s,
                license_plate = %s,
                average_cost_per_day = %s,
                available_count = %s
            WHERE id = %s
        """, (name, car_type, brand, license_plate, average_cost_per_day, available_count, car_id))
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
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT car_type FROM cars")
        car_types = cursor.fetchall()
        cursor.close()
        conn.close()
        return car_types

    @staticmethod
    def get_all_models():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT model FROM cars")
        models = cursor.fetchall()
        cursor.close()
        conn.close()
        return models
