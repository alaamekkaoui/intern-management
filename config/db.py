import mysql.connector
from config.config import Config

def get_db_connection():
    try:
        # First, connect without specifying a database
        init_conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        init_cursor = init_conn.cursor()
        init_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        init_cursor.close()
        init_conn.close()

        # Now connect to the specific database
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(50),
            internship_id INT,
            teacher_id INT,
            FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE SET NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    conn.commit()
    cursor.close()
    conn.close()
