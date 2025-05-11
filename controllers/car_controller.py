from flask import render_template, request, redirect, flash
from models.car import Car

class CarController:
    # List all cars
    def list_cars(self):
        cars = Car.get_all()  # Fetch all cars from the database
        return render_template('car/list.html', cars=cars)

    # Show form to add a new car
    def show_add_car_form(self):
        return render_template('car/add.html')

    # Add a new car
    def add_car(self, request):
        name = request.form['name']
        car_type = request.form['type']
        cost_per_day = request.form['cost_per_day']
        
        # Adding the car to the database
        if Car.add_car(name, car_type, cost_per_day):
            flash('La voiture a été ajoutée avec succès!', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de l'ajout de la voiture.", 'danger')  # Error message

        return redirect('/car')

    # Show details for a single car (optional)
    def show_car_details(self, car_id):
        car = Car.get_by_id(car_id)
        return render_template('car/details.html', car=car)

    # Delete a car (optional)
    def delete_car(self, car_id):
        if Car.delete_car(car_id):
            flash('La voiture a été supprimée avec succès.', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de la suppression de la voiture.", 'danger')  # Error message
        
        return redirect('/car')

     # Show edit form for a specific car
    def show_edit_car_form(self, car_id):
        car = Car.get_by_id(car_id)
        return render_template('car/edit.html', car=car)

    # Handle editing a car's details
    def edit_car(self, car_id, request):
        model = request.form['model']
        make = request.form['make']
        year = request.form['year']
        availability = request.form['availability']

        # Update car in the database
        if Car.update(car_id, model, make, year, availability):
            flash('Car updated successfully.', 'success')  # Success message
            return redirect('/car')
        else:
            flash("An error occurred while updating the car.", 'danger')  # Error message
            return redirect(f'/car/edit/{car_id}')