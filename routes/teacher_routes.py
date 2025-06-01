from flask import request, redirect, url_for, flash, render_template, send_file
from controllers.teacher_controller import TeacherController
from models.teacher import Teacher
from models.department import Department # Needed for edit route
from utils.utils import role_required
from utils.pdf_utils import export_teachers_pdf, export_teachers_xlsx, import_teachers_from_xlsx, sample_teacher_xlsx

def register_teacher_routes(app):
    teacher_controller = TeacherController()

    @app.route('/teacher')
    @role_required('admin', 'teacher')
    def teacher_list():
        return teacher_controller.list_teachers()

    @app.route('/teacher/add', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def add_teacher():
        if request.method == 'POST':
            return teacher_controller.add_teacher(request)
        return teacher_controller.show_add_teacher_form()

    @app.route('/teacher/<int:teacher_id>')
    @role_required('admin', 'teacher')
    def teacher_details(teacher_id):
        return teacher_controller.show_teacher_details(teacher_id)

    @app.route('/teacher/edit/<int:teacher_id>', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def edit_teacher(teacher_id):
        if request.method == 'POST':
            return teacher_controller.edit_teacher(teacher_id, request)
        teacher = Teacher.get_by_id(teacher_id)
        departments = Department.get_all()  # Use plural 'departments'
        print("Route list of departments", departments)  # Debugging output
        return render_template('teacher/edit.html', teacher=teacher, departments=departments)


    @app.route('/teacher/delete/<int:teacher_id>', methods=['POST'])
    @role_required('admin')
    def delete_teacher(teacher_id):
        return teacher_controller.delete_teacher(teacher_id)

    @app.route('/teacher/export/pdf')
    def export_teachers_pdf_route():
        teachers = Teacher.get_all()
        pdf_io = export_teachers_pdf(teachers)
        return send_file(pdf_io, as_attachment=True, download_name='teachers.pdf', mimetype='application/pdf')

    @app.route('/teacher/export/xlsx')
    def export_teachers_xlsx_route():
        teachers = Teacher.get_all()
        xlsx_io = export_teachers_xlsx(teachers)
        return send_file(xlsx_io, as_attachment=True, download_name='teachers.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/teacher/import/xlsx', methods=['GET', 'POST'])
    def import_teachers_xlsx():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or not file.filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(request.url)
            count, errors = import_teachers_from_xlsx(file)
            if errors:
                flash(f"Import partiel: {count} enseignants ajoutés. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} enseignants importés avec succès!", 'success')
            return redirect(url_for('teacher_list'))
        return render_template('teacher/import_xlsx.html')

    @app.route('/teacher/sample/xlsx')
    def sample_teacher_xlsx_route():
        xlsx_io = sample_teacher_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_teacher_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 