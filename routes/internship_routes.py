from flask import request, redirect, url_for, flash, render_template, send_file
from controllers.internship_controller import InternshipController
from models.internship import Internship
from models.intern_type import InternType # Needed for add/edit routes
from utils.utils import role_required
from utils.pdf_utils import export_internships_xlsx, export_internships_pdf, sample_internship_xlsx, import_internships_from_xlsx, export_single_internship_pdf

def register_internship_routes(app):
    internship_controller = InternshipController()

    @app.route('/internship')
    @role_required('admin', 'teacher', 'car')
    def internship_list():
        return internship_controller.list_internships()

    @app.route('/internship/add', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def add_internship():
        if request.method == 'POST':
            return internship_controller.add_internship(request)
        # Fetch intern types from the database
        intern_types = InternType.get_all()
        return internship_controller.show_add_internship_form(intern_types)

    @app.route('/internship/edit/<int:internship_id>', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def edit_internship(internship_id):
        if request.method == 'POST':
            return internship_controller.edit_internship(internship_id, request)
        # Fetch intern types from the database
        intern_types = InternType.get_all()
        return internship_controller.show_edit_internship_form(internship_id)

    @app.route('/internship/delete/<int:internship_id>', methods=['POST'])
    @role_required('admin')
    def delete_internship(internship_id):
        return internship_controller.delete_internship(internship_id)

    @app.route('/internship/cancel/<int:internship_id>', methods=['POST'])
    @role_required('admin', 'teacher')
    def cancel_internship(internship_id):
        return internship_controller.cancel_internship(internship_id)

    @app.route('/internship/mark_done/<int:internship_id>', methods=['POST'])
    @role_required('admin', 'teacher')
    def mark_as_done(internship_id):
        return internship_controller.mark_as_done(internship_id)

    @app.route('/internship/details/<int:internship_id>')
    @role_required('admin', 'teacher', 'car')
    def internship_details(internship_id):
        return internship_controller.show_internship_details(internship_id)

    @app.route('/internship/export/xlsx')
    def export_internships_xlsx_route():
        internships = Internship.get_all()
        xlsx_io = export_internships_xlsx(internships)
        return send_file(xlsx_io, as_attachment=True, download_name='internships.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/internship/export/pdf')
    def export_internships_pdf_route():
        internships = Internship.get_all()
        pdf_io = export_internships_pdf(internships)
        return send_file(pdf_io, mimetype='application/pdf')

    @app.route('/internship/export/pdf/<int:internship_id>')
    def export_single_internship_pdf_route(internship_id):
        internship = Internship.get_by_id(internship_id)
        if not internship:
            flash('Internship not found!', 'danger')
            return redirect(url_for('internship_list'))
        pdf_io = export_single_internship_pdf(internship)
        return send_file(pdf_io, mimetype='application/pdf')

    @app.route('/internship/sample/xlsx')
    def sample_internship_xlsx_route():
        xlsx_io = sample_internship_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_internship_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/internship/import/xlsx', methods=['GET', 'POST'])
    def import_internships_xlsx():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or not file.filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(request.url)
            count, errors = import_internships_from_xlsx(file)
            if errors:
                flash(f"Import partiel: {count} stages ajoutés. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} stages importés avec succès!", 'success')
            return redirect(url_for('internship_list'))
        return render_template('internship/list.html') 