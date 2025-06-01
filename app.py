from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, flash, session
from models import create_all_tables, insert_dummy_data
from models.user import User
from models.internship import Internship
from models.department import Department
from models.teacher import Teacher
from models.car import Car
from models.intern_type import InternType
from routes import init_app
from config.config import Config
from config.db import get_db_connection, create_tables

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database connection and create tables
with app.app_context():
    conn = get_db_connection()
    if conn:
        create_tables()
        conn.close()

# Initialize the database and create tables and register all routes from the routes package
init_app(app)

# Context processor to inject current year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# ------------------------------------------------------
# Define the route for the index page (your home page)
@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login_user'))
    role = session.get('role')
    counts = {}
    if role in ['admin', 'teacher', 'car']:
        counts['internship_count'] = len(Internship.get_all())
    if role in ['admin', 'teacher']:
        counts['teacher_count'] = len(Teacher.get_all())
        counts['department_count'] = len(Department.get_all())
        counts['intern_type_count'] = len(InternType.get_all())
    if role in ['admin', 'car']:
        counts['car_count'] = len(Car.get_all())
    if role == 'admin':
        counts['user_count'] = len(User.get_all_users())
    if role in ['admin', 'teacher', 'car']:
        from models.student import Student
        counts['student_count'] = len(Student.get_all())
    current_year = datetime.now().year
    return render_template('index.html', **counts, current_year=current_year)  
# ------------------------------------------------------
# Route to create the default admin if it doesn't exist
@app.route('/create_default_admin')
def create_default_admin():
    User.create_default_admin() 
    flash('Default admin created!', 'success')
    return redirect(url_for('index'))  

# Route to reset the database
@app.route('/reset_database', methods=['POST'])
def reset_database():
    create_all_tables()
    flash('Database has been reset!', 'success')
    return redirect(url_for('index'))

# Route to insert dummy data
@app.route('/insert_dummy_data', methods=['POST'])
def insert_dummy_data_route():
    insert_dummy_data()
    flash('Dummy data inserted!', 'success')
    return redirect(url_for('index'))


@app.route('/debug', methods=['GET', 'POST'])
def debug_route():
    debug_mode = os.getenv('DEBUG_MODE') 
    debug_code = os.getenv('DEBUG_CODE')
    print("--------------------Debug mode:", debug_mode)
    if debug_mode == 'False':
        return render_template('404.html'), 404
    if debug_mode == 'True':
        current_year = datetime.now().year
        if request.method == 'POST':
            code = request.form.get('code')
            if code == debug_code:
                return render_template('debug.html', success=True, debug_mode=True, current_year=current_year)
            else:
                return render_template('debug.html', success=False, debug_mode=True, current_year=current_year)
        return render_template('debug.html', debug_mode=True, current_year=current_year)
    return render_template('404.html'), 404
# ------------------------------------------------------

if __name__ == '__main__':
    app.run(port=5001 ,host="0.0.0.0", debug=True)
