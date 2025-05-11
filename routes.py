from flask import render_template, request
from controllers.car_controller import CarController
from controllers.department_controller import DepartmentController
from controllers.internship_controller import InternshipController
from controllers.user_controller import UserController
from controllers.teacher_controller import TeacherController
from models.department import Department
from models.teacher import Teacher
#from models.teacher import Teacher


def init_routes(app):
    car_controller = CarController()
    department_controller = DepartmentController()
    internship_controller = InternshipController()
    user_controller = UserController()
    teacher_controller = TeacherController()

    # -------------------------------------------------Car routes-------------------------------------------------
    @app.route('/car')
    def car_list():
        return car_controller.list_cars()

    @app.route('/car/add', methods=['GET', 'POST'])
    def add_car():
        if request.method == 'POST':
            return car_controller.add_car(request)
        return car_controller.show_add_car_form()

    @app.route('/car/edit/<int:car_id>', methods=['GET', 'POST'])
    def edit_car(car_id):
        if request.method == 'POST':
            return car_controller.edit_car(car_id, request)
        return car_controller.show_edit_car_form(car_id)

    @app.route('/car/delete/<int:car_id>', methods=['POST'])
    def delete_car(car_id):
        return car_controller.delete_car(car_id)
    # -------------------------------------------------Department routes-------------------------------------------------
    @app.route('/department')
    def department_list():
        return department_controller.list_departments()

    @app.route('/department/add', methods=['GET', 'POST'])
    def add_department():
        if request.method == 'POST':
            return department_controller.add_department(request)
        return department_controller.show_add_department_form()

    @app.route('/department/edit/<int:department_id>', methods=['GET', 'POST'])
    def edit_department(department_id):
        if request.method == 'POST':
            return department_controller.edit_department(department_id, request)
        return department_controller.show_edit_department_form(department_id)

    @app.route('/department/delete/<int:department_id>', methods=['POST'])
    def delete_department(department_id):
        # Call the controller's delete_department method
        return department_controller.delete_department(department_id)


        # -------------------------------------------------Teacher routes-------------------------------------------------
    @app.route('/teacher')
    def teacher_list():
        return teacher_controller.list_teachers()

    @app.route('/teacher/add', methods=['GET', 'POST'])
    def add_teacher():
        if request.method == 'POST':
            return teacher_controller.add_teacher(request)
        return teacher_controller.show_add_teacher_form()

    @app.route('/teacher/details/<int:teacher_id>')
    def teacher_details(teacher_id):
        return teacher_controller.show_teacher_details(teacher_id)

    @app.route('/teacher/edit/<int:teacher_id>', methods=['GET', 'POST'])
    def edit_teacher(teacher_id):
        if request.method == 'POST':
            return teacher_controller.edit_teacher(teacher_id, request)
        teacher = Teacher.get_by_id(teacher_id)
        departments = Department.get_all()  # Use plural 'departments'
        print("Route list of departments", departments)  # Debugging output
        return render_template('teacher/edit.html', teacher=teacher, departments=departments)


    @app.route('/teacher/delete/<int:teacher_id>', methods=['POST'])
    def delete_teacher(teacher_id):
        return teacher_controller.delete_teacher(teacher_id)
    
    # -------------------------------------------------Internship routes-------------------------------------------------
    @app.route('/internship')
    def internship_list():
        return internship_controller.list_internships()

    @app.route('/internship/add', methods=['GET', 'POST'])
    def add_internship():
        if request.method == 'POST':
            return internship_controller.add_internship(request)
        return internship_controller.show_add_internship_form()

    @app.route('/internship/edit/<int:internship_id>', methods=['GET', 'POST'])
    def edit_internship(internship_id):
        if request.method == 'POST':
            return internship_controller.edit_internship(internship_id, request)
        return internship_controller.show_edit_internship_form(internship_id)

    @app.route('/internship/delete/<int:internship_id>', methods=['POST'])
    def delete_internship(internship_id):
        return internship_controller.delete_internship(internship_id)

    @app.route('/internship/cancel/<int:internship_id>', methods=['POST'])
    def cancel_internship(internship_id):
        return internship_controller.cancel_internship(internship_id)

    @app.route('/internship/mark_done/<int:internship_id>', methods=['POST'])
    def mark_as_done(internship_id):
        return internship_controller.mark_as_done(internship_id)

    @app.route('/internship/types/add', methods=['GET', 'POST'])
    def add_internship_type():
        if request.method == 'POST':
            return internship_controller.add_internship_type(request)
        return internship_controller.show_add_internship_type_form()

    # -------------------------------------------------User routes-------------------------------------------------
    @app.route('/login', methods=['GET', 'POST'])
    def login_user():
        if request.method == 'POST':
            return user_controller.login(request)
        return user_controller.show_login_form()

    @app.route('/logout')
    def logout_user():
        return user_controller.logout()
    
    @app.route('/register')
    def register_user():
        return user_controller.register()

    @app.route('/user')
    def list_users():
        return user_controller.list_users()

    @app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        if request.method == 'POST':
            return user_controller.edit_user(user_id, request)
        return user_controller.show_edit_user_form(user_id)