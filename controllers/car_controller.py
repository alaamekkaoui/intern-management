from flask import render_template, request, redirect, flash
from models.car import Car
from models.internship import Internship
from datetime import date, datetime
from utils.log_utils import log_activity

class CarController:
    # List all cars
    def list_cars(self):
        name = request.args.get('name', '').strip()
        model = request.args.get('model', '').strip()
        car_type = request.args.get('car_type', '').strip()
        availability = request.args.get('availability', '').strip()  # 'available' or 'unavailable'
        cars = Car.get_all()
        today = date.today()
        available_today = {}
        filtered_cars = []
        for car in cars:
            used = 0
            internships = Internship.get_by_car_id(car['id'])
            for i in internships:
                try:
                    start_date = datetime.strptime(i['start_date'], '%Y-%m-%d').date() if isinstance(i['start_date'], str) else i['start_date']
                    end_date = datetime.strptime(i['end_date'], '%Y-%m-%d').date() if isinstance(i['end_date'], str) else i['end_date']
                except Exception:
                    continue
                if start_date <= today <= end_date and i['status'] != 'canceled':
                    used += 1
            available_count = max(car['available_count'] - used, 0)
            available_today[car['id']] = available_count
            # Filtering logic
            if name and name.lower() not in car['name'].lower():
                continue
            if model and model != car['model']:
                continue
            if car_type and car_type.lower() not in car['car_type'].lower():
                continue
            if availability == 'available' and available_count <= 0:
                continue
            if availability == 'unavailable' and available_count > 0:
                continue
            filtered_cars.append(car)
        if name or model or car_type or availability:
            cars = filtered_cars
        return render_template('car/list.html', cars=cars, available_today=available_today, filter_name=name, filter_model=model, filter_car_type=car_type, filter_availability=availability)

    # Show form to add a new car
    def show_add_car_form(self):
        models = Car.get_all_models()
        return render_template('car/add.html', models=models)

    # Add a new car
    def add_car(self, request):
        model = request.form['model']
        if model == 'autre':
            model = request.form['model_custom']
        name = request.form['name']
        car_type = request.form['car_type']
        brand = request.form['brand']
        license_plate = request.form['license_plate']
        average_cost_per_day = request.form['average_cost_per_day']
        available_count = request.form['available_count']

        try:
            Car.add_car(name, model, car_type, brand, license_plate, average_cost_per_day, available_count)
            cars = Car.get_all()
            new_car = next((c for c in cars if c['license_plate'] == license_plate), None)
            log_activity('add', 'car', new_car['id'] if new_car else None)
            flash('La voiture a été ajoutée avec succès!', 'success')
        except Exception as e:
            print(f"Error adding car: {e}")
            flash("Une erreur s'est produite lors de l'ajout de la voiture.", 'danger')

        return redirect('/car')

    # Show details for a single car
    def show_car_details(self, car_id):
        try:
            car_id = int(car_id)
        except (TypeError, ValueError):
            flash("ID de voiture invalide.", "danger")
            return redirect('/car')
        car = Car.get_by_id(car_id)
        internships = Internship.get_by_car_id(car_id)
        return render_template('car/details.html', car=car, internships=internships)

    # Delete a car
    def delete_car(self, car_id):
        try:
            car_id = int(car_id)
        except (TypeError, ValueError):
            flash("ID de voiture invalide.", "danger")
            return redirect('/car')
        try:
            Car.delete_car(car_id)
            log_activity('delete', 'car', car_id)
            flash('La voiture a été supprimée avec succès.', 'success')
        except Exception as e:
            print(f"Error deleting car: {e}")
            flash("Une erreur s'est produite lors de la suppression de la voiture.", 'danger')
        return redirect('/car')

    # Show edit form for a specific car
    def show_edit_car_form(self, car_id):
        try:
            car_id = int(car_id)
        except (TypeError, ValueError):
            flash("ID de voiture invalide.", "danger")
            return redirect('/car')
        car = Car.get_by_id(car_id)
        return render_template('car/edit.html', car=car)

    # Handle editing a car's details
    def edit_car(self, car_id, request):
        try:
            car_id = int(car_id)
        except (TypeError, ValueError):
            flash("ID de voiture invalide.", "danger")
            return redirect('/car')
        name = request.form['name']
        car_type = request.form['car_type']
        brand = request.form['brand']
        license_plate = request.form['license_plate']
        average_cost_per_day = request.form['average_cost_per_day']
        available_count = request.form['available_count']

        try:
            Car.update_car(car_id, name, car_type, brand, license_plate, average_cost_per_day, available_count)
            log_activity('update', 'car', car_id)
            flash('La voiture a été mise à jour avec succès.', 'success')
            return redirect('/car')
        except Exception as e:
            print(f"Error updating car: {e}")
            flash("Une erreur s'est produite lors de la mise à jour de la voiture.", 'danger')
            return redirect(f'/car/edit/{car_id}')
