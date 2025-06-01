from flask import request, redirect, url_for, flash, render_template, send_file
from controllers.student_controller import StudentController
from models.student import Student
from utils.utils import role_required
from utils.pdf_utils import sample_student_xlsx

def register_student_routes(app):
    student_controller = StudentController()

    @app.route('/student')
    @role_required('admin', 'teacher', 'car')
    def student_list():
        return student_controller.list_students()

    @app.route('/student/add', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def add_student():
        internship_id = request.args.get('internship_id')
        if request.method == 'POST':
            student_id = student_controller.add_student(request) # Assuming add_student returns the new student_id
            if student_id and internship_id:
                 # Need to ensure Student model has assign_internship method or call controller method
                Student.assign_internship(student_id, internship_id) # Assuming Student.assign_internship exists
            return redirect(url_for('student_list')) # Redirect to the student list after adding
        return student_controller.show_add_student_form(internship_id=internship_id)

    @app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def edit_student(student_id):
        # Assuming StudentController().edit_student handles both GET (showing form) and POST (processing form)
        return student_controller.edit_student(student_id, request) # Pass request object

    @app.route('/student/delete/<int:student_id>', methods=['POST'])
    @role_required('admin')
    def delete_student(student_id):
        # Assuming StudentController().delete_student handles the deletion
        return student_controller.delete_student(student_id)

    @app.route('/student/sample/xlsx')
    def sample_student_xlsx_route():
        xlsx_io = sample_student_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_student_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 