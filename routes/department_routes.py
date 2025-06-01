from flask import request, redirect, url_for, flash, render_template, send_file
from controllers.department_controller import DepartmentController
from models.department import Department
from utils.pdf_utils import export_departments_pdf, export_departments_xlsx, sample_department_xlsx, import_departments_from_xlsx
from utils.utils import role_required

def register_department_routes(app):
    department_controller = DepartmentController()

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

    @app.route('/department/export/pdf')
    def export_departments_pdf_route():
        departments = Department.get_all()
        pdf_io = export_departments_pdf(departments)
        return send_file(pdf_io, as_attachment=True, download_name='departments.pdf', mimetype='application/pdf')

    @app.route('/department/export/xlsx')
    def export_departments_xlsx_route():
        departments = Department.get_all()
        xlsx_io = export_departments_xlsx(departments)
        return send_file(xlsx_io, as_attachment=True, download_name='departments.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/department/sample/xlsx')
    def sample_department_xlsx_route():
        xlsx_io = sample_department_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_department_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/department/import/xlsx', methods=['GET', 'POST'])
    @role_required('admin', 'teacher', 'car')
    def import_departments_xlsx():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or not file.filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(request.url) # Use request.url to redirect back to the current page on error
            count, errors = import_departments_from_xlsx(file)
            if errors:
                flash(f"Import partiel: {count} départements ajoutés. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} départements importés avec succès!", 'success')
            return redirect(url_for('department_list'))
        return render_template('department/import_xlsx.html') 