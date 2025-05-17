from flask import render_template, request, redirect, flash
from models.internship import Internship
from models.car import Car
from models.teacher import Teacher
from models.intern_type import InternType  # Import the InternshipType model

class InternshipController:
    # List all internships
    def list_internships(self):
        teacher_name = request.args.get('teacher_name', '').strip()
        intern_type_id = request.args.get('intern_type_id', '').strip()
        car_needed = request.args.get('car_needed', '').strip()
        status = request.args.get('status', '').strip()

        internships = Internship.get_all()
        # Filter by teacher name (partial match, case-insensitive)
        if teacher_name:
            internships = [i for i in internships if teacher_name.lower() in (i.get('first_name', '') + ' ' + i.get('last_name', '')).lower()]
        # Filter by intern_type_id
        if intern_type_id:
            internships = [i for i in internships if str(i.get('intern_type_id')) == intern_type_id]
        # Filter by car_needed (Oui/Non)
        if car_needed == '1':
            internships = [i for i in internships if i.get('car_id')]
        elif car_needed == '0':
            internships = [i for i in internships if not i.get('car_id')]
        # Filter by status
        if status:
            internships = [i for i in internships if i.get('status') == status]

        teachers = Teacher.get_all()
        cars = Car.get_all()
        intern_types = InternType.get_all()
        return render_template('internship/list.html', internships=internships, teachers=teachers, cars=cars, intern_types=intern_types)

    # Show form to add a new internship
    def show_add_internship_form(self,intern_types):
        teachers = Teacher.get_all()  # Get list of teachers
        cars = Car.get_all()
        return render_template('internship/add.html', teachers=teachers, cars=cars, intern_types=intern_types)

    # Add a new internship
    def add_internship(self, request):
        teacher_id = request.form['teacher_id']
        intern_type_id = request.form['intern_type_id']  # Get the intern_type_id (foreign key)
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # If car_needed is checked, get car_id, else set to None
        car_id = request.form['car_id'] if 'car_needed' in request.form and request.form.get('car_id') else None
        
        # Check car availability if a car is selected
        if car_id:
            if not Internship.is_car_available(car_id, start_date, end_date):
                flash("Cette voiture est déjà réservée entre ces dates.", "danger")
                return redirect('/internship/add')

        # Add internship
        if Internship.add_internship(teacher_id, intern_type_id, car_id, start_date, end_date):
            flash('Le stage a été ajouté avec succès!', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de l'ajout du stage.", 'danger')  # Error message

        return redirect('/internship')

    # Show form to add internship types (e.g., 'fieldwork', 'labwork')
    def show_add_internship_type_form(self,intern_types):
        return render_template('/internship/add_internship_type.html', intern_types=intern_types)

    
    # Cancel an internship (update status to canceled)
    def cancel_internship(self, internship_id):
        # Try to update the internship status to canceled
        if Internship.update_status(internship_id, 'canceled'):
            flash('Le stage a été annulé avec succès.', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de l'annulation du stage.", 'danger')  # Error message

        return redirect('/internship')

    # Delete an internship
    def delete_internship(self, internship_id):
        # Try to delete the internship
        if Internship.delete_internship(internship_id):
            flash('Le stage a été supprimé avec succès.', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de la suppression du stage.", 'danger')  # Error message

        return redirect('/internship')

    # Mark internship as done
    def mark_as_done(self, internship_id):
        # Mark internship as done
        if Internship.update_status(internship_id, 'done'):
            flash('Le stage a été marqué comme terminé.', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de la mise à jour du stage.", 'danger')  # Error message

        return redirect('/internship')

    # Show edit form for a specific internship
    def show_edit_internship_form(self, internship_id):
        internship = Internship.get_by_id(internship_id)
        if internship is None:
            flash("Le stage demandé n'existe pas.", "danger")
            return redirect('/internship')
        teachers = Teacher.get_all()
        cars = Car.get_all()
        intern_types = InternType.get_all()  # Get all internship types
        return render_template('internship/edit.html', internship=internship, teachers=teachers, cars=cars, intern_types=intern_types)

    # Handle editing an internship's details
    def edit_internship(self, internship_id, request):
        teacher_id = request.form['teacher_id']
        intern_type_id = request.form['intern_type_id']  # Get the intern_type_id (foreign key) for update
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # If car_needed is checked, get car_id, else set to None
        car_id = request.form['car_id'] if 'car_needed' in request.form and request.form.get('car_id') else None

        # Update internship in the database
        if Internship.update_internship(internship_id, teacher_id, intern_type_id, car_id, start_date, end_date):
            flash('Internship updated successfully.', 'success')  # Success message
            return redirect('/internship')
        else:
            flash("An error occurred while updating the internship.", 'danger')  # Error message
            return redirect(f'/internship/edit/{internship_id}')

    
    def add_internship_type(self, request):
        type_name = request.form['type_name']

        # Check if the internship type already exists
        existing_intern_type = InternType.query.filter_by(name=type_name).first()

        if existing_intern_type:
            # If the type exists, flash a message and don't add it
            flash(f"Le type de stage '{type_name}' existe déjà.", 'danger')  # Error message
        else:
            # Add internship type (if it doesn't exist)
            if InternType.add_type(type_name):  # Calling the InternshipType model to add the type
                flash('Le type de stage a été ajouté avec succès!', 'success')  # Success message
            else:
                flash("Une erreur s'est produite lors de l'ajout du type de stage.", 'danger')  # Error message

        return redirect('/internship/types')

    # Show details for a single internship
    def show_internship_details(self, internship_id):
        internship = Internship.get_by_id(internship_id)
        if not internship:
            flash("Le stage demandé n'existe pas.", "danger")
            return redirect('/internship')
        # Get teacher name
        teacher = Teacher.get_by_id(internship['teacher_id']) if internship.get('teacher_id') else None
        internship['teacher_name'] = f"{teacher['first_name']} {teacher['last_name']}" if teacher else 'N/A'
        # Get intern type name
        intern_type = InternType.get_by_id(internship['intern_type_id']) if internship.get('intern_type_id') else None
        internship['intern_type_name'] = intern_type['name'] if intern_type else 'N/A'
        return render_template('internship/details.html', internship=internship)
