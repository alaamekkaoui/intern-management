from flask import render_template, request, redirect, flash
from models.internship import Internship
from models.car import Car
from models.teacher import Teacher

class InternshipController:
    # List all internships
    def list_internships(self):
        internships = Internship.get_all()
        return render_template('internship/list.html', internships=internships)

    # Show form to add a new internship
    def show_add_internship_form(self):
        teachers = Teacher.get_all()  # Get list of teachers
        car_types = Car.get_all_types()  # Get available car types
        return render_template('internship/add.html', teachers=teachers, car_types=car_types)

    # Add a new internship
    def add_internship(self, request):
        teacher_id = request.form['teacher_id']
        intern_type = request.form['intern_type']
        car_needed = 'car_needed' in request.form
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Add internship
        if Internship.add_internship(teacher_id, intern_type, car_needed, start_date, end_date):
            flash('Le stage a été ajouté avec succès!', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de l'ajout du stage.", 'danger')  # Error message

        return redirect('/internship')

    # Show form to add internship types (e.g., 'fieldwork', 'labwork')
    def show_add_internship_type_form(self):
        return render_template('internship/add_type.html')

    # Add a new internship type
    def add_internship_type(self, request):
        type_name = request.form['type_name']
        
        # Add internship type
        if Internship.add_type(type_name):
            flash('Le type de stage a été ajouté avec succès!', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de l'ajout du type de stage.", 'danger')  # Error message

        return redirect('/internship/types')

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
        return render_template('internship/edit.html', internship=internship)

    # Handle editing an internship's details
    def edit_internship(self, internship_id, request):
        internship_type = request.form['internship_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Update internship in the database
        if Internship.update(internship_id, internship_type, start_date, end_date):
            flash('Internship updated successfully.', 'success')  # Success message
            return redirect('/internship')
        else:
            flash("An error occurred while updating the internship.", 'danger')  # Error message
            return redirect(f'/internship/edit/{internship_id}')