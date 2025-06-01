from flask import request, url_for, flash, render_template, send_file
from controllers.car_controller import CarController
from models.car import Car
from utils.utils import role_required
from utils.pdf_utils import export_cars_xlsx, export_cars_pdf, sample_car_xlsx, import_cars_from_xlsx # Assuming pdf_utils contains import logic too

def register_car_routes(app):
    car_controller = CarController()

    @app.route('/car')
    @role_required('admin', 'car')
    def car_list():
        return car_controller.list_cars()

    @app.route('/car/add', methods=['GET', 'POST'])
    @role_required('admin', 'car')
    def add_car():
        if request.method == 'POST':
            return car_controller.add_car(request)
        return car_controller.show_add_car_form()

    @app.route('/car/edit/<int:car_id>', methods=['GET', 'POST'])
    @role_required('admin', 'car')
    def edit_car(car_id):
        if request.method == 'POST':
            return car_controller.edit_car(car_id, request)
        return car_controller.show_edit_car_form(car_id)

    @app.route('/car/delete/<int:car_id>', methods=['POST'])
    @role_required('admin', 'car')
    def delete_car(car_id):
        return car_controller.delete_car(car_id)

    @app.route('/car/<int:car_id>')
    def car_details(car_id):
        return car_controller.show_car_details(car_id)

    @app.route('/car/export/xlsx')
    def export_cars_xlsx_route():
        cars = Car.get_all()
        xlsx_io = export_cars_xlsx(cars)
        return send_file(xlsx_io, as_attachment=True, download_name='cars.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @app.route('/car/export/pdf')
    def export_cars_pdf_route():
        cars = Car.get_all()
        pdf_io = export_cars_pdf(cars)
        return send_file(pdf_io, as_attachment=True, download_name='cars.pdf', mimetype='application/pdf')

    @app.route('/car/sample/xlsx')
    def sample_car_xlsx_route():
        xlsx_io = sample_car_xlsx()
        return send_file(xlsx_io, as_attachment=True, download_name='sample_car_import.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetla.sheet')

    @app.route('/car/import/xlsx', methods=['GET', 'POST'])
    def import_cars_xlsx():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or not file.filename.endswith('.xlsx'):
                flash('Veuillez sélectionner un fichier XLSX valide.', 'danger')
                return redirect(url_for('car_list'))
            count, errors = import_cars_from_xlsx(file)
            if errors:
                flash(f"Import partiel: {count} voitures ajoutées. Erreurs: {errors}", 'warning')
            else:
                flash(f"{count} voitures importées avec succès!", 'success')
            return redirect(url_for('car_list'))
        return render_template('car/list.html') # Assuming the import form is on the list page or linked from it. If it's a separate page, this template path needs adjustment. 