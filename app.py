import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for
from models import create_all_tables
from models.user import User
from routes import init_routes  


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY',)

create_all_tables()

init_routes(app)

# ------------------------------------------------------
# Define the route for the index page (your home page)
@app.route('/')
def index():
    # This will render the main page of your app or dashboard
    return render_template('index.html')  # Ensure you have an 'index.html' template

# ------------------------------------------------------
# Route to create the default admin if it doesn't exist
@app.route('/create_default_admin')
def create_default_admin():
    User.create_default_admin()  # Ensure the admin user is created if not already present
    return redirect(url_for('index'))  # Redirect to the index page after creating the admin

if __name__ == '__main__':
    app.run(debug=True)
