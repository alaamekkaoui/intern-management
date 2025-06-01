from flask import request, redirect, url_for, flash, render_template, send_file
from models.intern_type import InternType
from utils.utils import role_required
from utils.pdf_utils import sample_intern_type_xlsx, import_intern_types_from_xlsx, export_internship_types_xlsx

def register_internship_type_routes(app):
    @app.route('/internship/types')
    @role_required('admin', 'teacher')
    def list_internship_types():
        intern_types = InternType.get_all()  # Fetch all internship types from the database
        return render_template('internship/list_internship_types.html', internship_types=intern_types)

    # Add a new internship type
    @app.route('/internship/types/add', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def add_internship_type():
        if request.method == 'POST':
            name = request.form['type_name']
            InternType.add_intern_type(name)  # Add the new type to the database
            flash('Internship Type added successfully!', 'success')
            return redirect(url_for('list_internship_types'))
        return render_template('internship/add_internship_type.html')

    # Edit an internship type
    @app.route('/internship/types/edit/<int:intern_type_id>', methods=['GET', 'POST'])
    @role_required('admin', 'teacher')
    def edit_internship_type(intern_type_id):
        intern_type = InternType.get_by_id(intern_type_id)  # Get the intern type by ID
        if not intern_type:
            flash('Internship Type not found!', 'danger')
            return redirect(url_for('list_internship_types'))

        if request.method == 'POST':
            name = request.form['type_name']
            InternType.update_intern_type(intern_type_id, name)  # Update the internship type
            flash('Internship Type updated successfully!', 'success')
            return redirect(url_for('list_internship_types'))

        return render_template('internship/edit_internship_type.html', intern_type=intern_type)

    # Delete an internship type
    @app.route('/internship/types/delete/<int:intern_type_id>', methods=['POST'])
    @role_required('admin')
    def delete_internship_type(intern_type_id):
        intern_type = InternType.get_by_id(intern_type_id)  # Fetch the intern type to ensure it exists
        if not intern_type:
            flash('Internship Type not found!', 'danger')
            return redirect(url_for('list_internship_types'))

        InternType.delete_intern_type(intern_type_id)  # Delete the internship type
        flash('Internship Type deleted successfully!', 'success')
        return redirect(url_for('list_internship_types'))

    @app.route('/internship/types/sample/xlsx')
    def sample_intern_type_xlsx_route():
        xlsx_io = sample_intern_type_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_intern_type_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/internship/types/import/xlsx', methods=['GET', 'POST'])
    @role_required('admin', 'teacher', 'car')
    def import_intern_types_xlsx():
        if request.method == 'POST':
            if 'file' not in request.files or not request.files['file'].filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(request.url)
            file = request.files['file']
            count, errors = import_intern_types_from_xlsx(file)
            if errors:
                flash(f"Import partiel: {count} types ajoutés. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} types importés avec succès!", 'success')
            return redirect(url_for('list_internship_types'))
        return render_template('internship/import_xlsx.html')

    @app.route('/internship/types/export/xlsx')
    def export_internship_types_xlsx_route():
        intern_types = InternType.get_all()
        xlsx_io = export_internship_types_xlsx(intern_types)
        return send_file(xlsx_io, as_attachment=True, download_name='internship_types.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 