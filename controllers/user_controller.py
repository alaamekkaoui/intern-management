from flask import render_template, request, redirect, session, flash
from models.user import User

class UserController:
    # Show login form
    def show_login_form(self):
        return render_template('user/login.html')

    # Handle user login
    def login(self, request):
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash('Bienvenue, vous êtes connecté.', 'success')  # Success message
            return redirect('/')
        else:
            flash("Nom d'utilisateur ou mot de passe invalide.", 'danger')  # Error message
            return redirect('/login')

    # Handle user logout
    def logout(self):
        session.clear()
        flash('Vous avez été déconnecté avec succès.', 'success')  # Success message
        return redirect('/login')

    # Show registration form (admin only)
    def show_register_form(self):
        return render_template('user/register.html')

    # Register new user (admin only)
    def register(self, request):
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        # Create new user and handle success/failure
        if User.create(username, password, role):
            flash('L\'utilisateur a été enregistré avec succès.', 'success')  # Success message
            return redirect('/login')
        else:
            flash("Une erreur s'est produite lors de l'enregistrement de l'utilisateur.", 'danger')  # Error message
            return redirect('/register')

    # Show the list of users (admin only)
    def list_users(self):
        users = User.get_all_users()
        return render_template('user/list.html', users=users)

    # Show edit form for a specific user (admin only)
    def show_edit_user_form(self, user_id):
        user = User.get_by_id(user_id)
        return render_template('user/edit.html', user=user)

    # Handle editing a user's details (admin only)
    def edit_user(self, user_id, request):
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if User.update(user_id, username, password, role):
            flash('Utilisateur mis à jour avec succès.', 'success')  # Success message
            return redirect('/user')
        else:
            flash("Une erreur s'est produite lors de la mise à jour de l'utilisateur.", 'danger')  # Error message
            return redirect(f'/user/edit/{user_id}')
