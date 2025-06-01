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
            num_ordre_mission VARCHAR(100),
            description TEXT,
            destination VARCHAR(255),
            kilometrage INT,
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
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Insert dummy users
        User.add_user('teacher', 'teacher', 'teacher')
        User.add_dummy_car_user()

        # 2. Insert dummy cars
        cursor.execute("""
            INSERT INTO cars (name, model, car_type, brand, license_plate, average_cost_per_day, available_count) VALUES
            ('Dacia Logan', 'Logan', 'Berline', 'Dacia', '12345-A-6', 300.00, 2),
            ('Renault Kangoo', 'Kangoo', 'Utilitaire', 'Renault', '67890-B-6', 400.00, 1),
            ('Peugeot Partner', 'Partner', 'Utilitaire', 'Peugeot', '24680-C-6', 350.00, 1)
        """)
        conn.commit()

        # 3. Insert dummy intern types
        cursor.execute("""
            INSERT INTO intern_types (name) VALUES
            ('Stage PFE'),
            ('Stage d''été'),
            ('Stage d''observation'),
            ('Stage professionnel')
        """)
        conn.commit()

        # 4. Insert dummy departments
        cursor.execute("""
            INSERT INTO departments (name) VALUES
            ('Génie Informatique'),
            ('Génie Industriel'),
            ('Génie Civil'),
            ('Génie Électrique'),
            ('Génie Mécanique')
        """)
        conn.commit()

        # 5. Insert dummy teachers
        cursor.execute("""
            INSERT INTO teachers (first_name, last_name, email, phone, department_id) VALUES
            ('Mohammed', 'Alami', 'm.alami@example.com', '0612345678', 1),
            ('Fatima', 'Benani', 'f.benani@example.com', '0698765432', 2),
            ('Karim', 'Chraibi', 'k.chraibi@example.com', '0611223344', 3),
            ('Amina', 'Dahmani', 'a.dahmani@example.com', '0655667788', 4)
        """)
        conn.commit()

        # 6. Insert dummy students
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, phone, teacher_id) VALUES
            ('Youssef', 'El Fathi', 'y.elfathi@example.com', '0611112222', 1),
            ('Sara', 'Benjelloun', 's.benjelloun@example.com', '0622223333', 2),
            ('Omar', 'Tazi', 'o.tazi@example.com', '0633334444', 3),
            ('Laila', 'Mansouri', 'l.mansouri@example.com', '0644445555', 4)
        """)
        conn.commit()

        # 7. Insert dummy internships
        cursor.execute("""
            INSERT INTO internships (title, start_date, end_date, teacher_id, car_id, intern_type_id, status, num_ordre_mission, description, destination, kilometrage) VALUES
            ('Développement Web Full Stack', '2024-07-01', '2024-08-01', 1, 1, 1, 'pending', 'ORD-001', 'Développement d''une application web pour la gestion des stages', 'Casablanca', 120),
            ('Optimisation des Processus Industriels', '2024-07-15', '2024-08-15', 2, 2, 2, 'pending', 'ORD-002', 'Étude et optimisation des processus de production', 'Tanger', 350),
            ('Étude de Structures Bâtiment', '2024-08-01', '2024-09-01', 3, 3, 3, 'pending', 'ORD-003', 'Analyse des structures d''un bâtiment commercial', 'Rabat', 80),
            ('Maintenance Électrique', '2024-08-15', '2024-09-15', 4, 1, 4, 'pending', 'ORD-004', 'Maintenance préventive des systèmes électriques', 'Marrakech', 200)
        """)
        conn.commit()

        cursor.close()
        conn.close()
        print("✅ Dummy data inserted successfully.")
    except Exception as e:
        print(f"❌ Error inserting dummy data: {e}")
