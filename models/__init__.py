from config.config import Config
from config.db import get_db_connection
from models.user import User
from models.internship import Internship
from models.car import Car
from models.student import Student  # Importing Student model
from datetime import date

def create_all_tables():
    try:
        # Connect to MySQL server (no database specified)
        import mysql.connector
        server_conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        server_cursor = server_conn.cursor()
        # Drop and recreate the database
        server_cursor.execute(f"DROP DATABASE IF EXISTS {Config.DB_NAME}")
        server_cursor.execute(f"CREATE DATABASE {Config.DB_NAME}")
        server_cursor.close()
        server_conn.close()

        # Now connect to the new database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Recreate tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(15),
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            model VARCHAR(100) NOT NULL,
            car_type VARCHAR(100) NOT NULL,
            brand VARCHAR(100) NOT NULL,
            license_plate VARCHAR(50) NOT NULL,
            average_cost_per_day DECIMAL(10, 2) NOT NULL,
            available_count INT NOT NULL
        );
        """)

        # Create the intern_types table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS intern_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """)

        # Modify the internships table to include intern_type_id as a foreign key
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            teacher_id INT,
            car_id INT,
            intern_type_id INT,  -- Adding foreign key to intern_types
            status ENUM('pending', 'canceled', 'done') DEFAULT 'pending',
            FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
            FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE SET NULL,
            FOREIGN KEY (intern_type_id) REFERENCES intern_types(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(15),
            internship_id INT,
            teacher_id INT,
            FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE SET NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database dropped, recreated, and all tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")


def insert_dummy_data():
    try:
        # Insert dummy users using add_user method
        User.add_user('teacher', 'teacher', 'teacher')
        User.add_dummy_car_user()
        # Insert dummy departments
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO departments (name) VALUES
            ('Computer Science'),
            ('Mathematics')
        """)
        # Insert dummy teachers
        cursor.execute("""
            INSERT INTO teachers (first_name, last_name, email, phone, department_id) VALUES
            ('Alice', 'Smith', 'alice.smith@example.com', '1234567890', 1),
            ('Bob', 'Johnson', 'bob.johnson@example.com', '0987654321', 2)
        """)
        # Insert dummy cars
        cursor.execute("""
            INSERT INTO cars (name, model, car_type, brand, license_plate, average_cost_per_day, available_count) VALUES
            ('Car A', '4x4', 'SUV', 'Toyota', 'ABC-123', 50.00, 2),
            ('Car B', 'Bus', 'Minibus', 'Mercedes', 'XYZ-789', 120.00, 1)
        """)
        # Insert dummy intern types
        cursor.execute("""
            INSERT INTO intern_types (name) VALUES
            ('Research'),
            ('Fieldwork')
        """)
        # Insert dummy internships
        cursor.execute("""
            INSERT INTO internships (title, start_date, end_date, teacher_id, car_id, intern_type_id, status) VALUES
            ('AI Research', '2024-07-01', '2024-08-01', 1, 1, 1, 'pending'),
            ('Math Fieldwork', '2024-07-15', '2024-08-15', 2, NULL, 2, 'pending')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dummy data inserted successfully.")
    except Exception as e:
        print(f"❌ Error inserting dummy data: {e}")
