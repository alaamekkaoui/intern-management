from flask import request, redirect, url_for, flash, render_template, session, jsonify
from controllers.user_controller import UserController
from utils.utils import role_required

def register_user_routes(app):
    user_controller = UserController()

    @app.route('/login', methods=['GET', 'POST'])
    def login_user():
        if request.method == 'POST':
            return user_controller.login(request)
        return user_controller.show_login_form()

    @app.route('/logout')
    def logout_user():
        return user_controller.logout()

    @app.route('/register', methods=['GET', 'POST'])
    def register_user():
        if request.method == 'POST':
            return user_controller.register(request)
        return user_controller.show_register_form()

    @app.route('/user')
    def list_users():
        return user_controller.list_users()

    @app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
    @role_required('admin')
    def edit_user(user_id):
        if request.method == 'POST':
            return user_controller.edit_user(user_id, request)
        return user_controller.show_edit_user_form(user_id)

    @app.route('/user/update_profile', methods=['POST'])
    @role_required('admin', 'teacher', 'car')
    def update_profile():
        return user_controller.update_profile(request)

    @app.route('/user/delete/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        return user_controller.delete_user(user_id) 