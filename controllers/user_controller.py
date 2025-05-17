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
            session['username'] = user['username']
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
        try:
            User.add_user(username, password, role)
            flash('L\'utilisateur a été enregistré avec succès.', 'success')  # Success message
            return redirect('/login')
        except Exception as e:
            flash(f"Une erreur s'est produite lors de l'enregistrement de l'utilisateur: {e}", 'danger')  # Error message
            return redirect('/register')

    # Show the list of users (admin only)
    def list_users(self):
        username = request.args.get('username', '').strip()
        role = request.args.get('role', '').strip()
        users = User.get_all_users()
        if username:
            users = [u for u in users if username.lower() in u.get('username', '').lower()]
        if role:
            users = [u for u in users if u.get('role') == role]
        return render_template('user/list.html', users=users, filter_username=username, filter_role=role)

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

    # Handle inline profile update (username, role, password)
    def update_profile(self, request):
        user_id = session.get('user_id')
        if not user_id:
            flash('Vous devez être connecté.', 'danger')
            return redirect('/login')
        username = request.form['username']
        role = request.form['role']
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        success, message = User.update_profile(user_id, username, role, old_password, new_password)
        if success:
            session['username'] = username
            session['role'] = role
            flash(message, 'success')
        else:
            flash(message, 'danger')
        return redirect('/user')
