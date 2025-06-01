from flask import request, redirect, url_for, flash, render_template, send_file
from controllers.student_controller import StudentController
from models.student import Student
from utils.utils import role_required
from utils.pdf_utils import sample_student_xlsx, export_students_xlsx

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
        return student_controller.edit_student(student_id)

    @app.route('/student/delete/<int:student_id>', methods=['POST'])
    @role_required('admin')
    def delete_student(student_id):
        return student_controller.delete_student(student_id)

    @app.route('/student/sample/xlsx')
    def sample_student_xlsx_route():
        xlsx_io = sample_student_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_student_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/student/export/xlsx')
    def export_students_xlsx_route():
        students = Student.get_all() # Fetch all students
        xlsx_io = export_students_xlsx(students) # Use the new function
        return send_file(xlsx_io, as_attachment=True, download_name='students.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/student/import/xlsx', methods=['GET', 'POST'])
    @role_required('admin', 'teacher', 'car')
    def import_students_xlsx():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or not file.filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(request.url)
            internship_id = request.form.get('internship_id')
            count, errors = student_controller.import_students_xlsx(file, internship_id)
            if errors:
                flash(f"Import partiel: {count} étudiants ajoutés. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} étudiants importés avec succès!", 'success')
            return redirect(url_for('student_list'))
        return render_template('student/import_xlsx.html')

    @app.route('/student/<int:student_id>')
    @role_required('admin', 'teacher')
    def student_details(student_id):
        return student_controller.show_student_details(student_id) 