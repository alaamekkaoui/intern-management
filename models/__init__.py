from db import get_db_connection

def create_all_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

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
            model VARCHAR(100),
            plate_number VARCHAR(20) NOT NULL UNIQUE
        )
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

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
