import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, flash
from models import create_all_tables, insert_dummy_data
from models.user import User
from routes import init_routes  


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY',)

# ------------------------------------------------------
# Define the route for the index page (your home page)
@app.route('/')
def index():
    return render_template('index.html')  
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

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
