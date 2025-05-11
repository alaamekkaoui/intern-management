import mysql.connector
from config import Config

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
