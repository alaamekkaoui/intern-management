from config.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def add_user(username, password, role):
        # Translate role from French selection to database role
        if role == 'Professeur':
            role = 'teacher'
        elif role == 'Logistique':
            role = 'car'
        # No need to modify "admin" as it already matches
        
        try:
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """, (username, hashed_password, role))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error adding user: {e}", "danger")

    @staticmethod
    def get_user_by_username(username):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}", "danger")
            return None

    @staticmethod
    def authenticate(username, password):
        user = User.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        print("Invalid username or password", "danger")
        return None

    @staticmethod
    def create_default_admin():
        # Create an admin account by default
        admin = User.get_user_by_username('admin')
        if not admin:
            User.add_user('admin', 'admin', 'admin')  # Use a better default password in production
    @staticmethod
    def get_all_users():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as a dict
        cursor.execute("SELECT * FROM users")  # Assuming your table is named 'users'
        users = cursor.fetchall()  # Fetch all results
        cursor.close()
        connection.close()
        return users   
      
    @staticmethod
    def get_by_id(user_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()  # Fetch a single user by ID
        cursor.close()
        connection.close()
        return user

    @staticmethod
    def add_dummy_car_user():
        User.add_user('car', 'car', 'car')

    @staticmethod
    def update_profile(user_id, username, role, old_password=None, new_password=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch current user
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return False, "Utilisateur introuvable."
        # If changing password, check old password
        if new_password:
            if not old_password or not check_password_hash(user['password'], old_password):
                cursor.close()
                conn.close()
                return False, "Ancien mot de passe incorrect."
            hashed_password = generate_password_hash(new_password)
            cursor.execute("""
                UPDATE users SET username=%s, role=%s, password=%s WHERE id=%s
            """, (username, role, hashed_password, user_id))
        else:
            cursor.execute("""
                UPDATE users SET username=%s, role=%s WHERE id=%s
            """, (username, role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Profil mis à jour avec succès."

    @staticmethod
    def update(user_id, username, password, role):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    UPDATE users SET username=%s, role=%s, password=%s WHERE id=%s
                """, (username, role, hashed_password, user_id))
            else:
                cursor.execute("""
                    UPDATE users SET username=%s, role=%s WHERE id=%s
                """, (username, role, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}", "danger")
            cursor.close()
            conn.close()
            return False

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
