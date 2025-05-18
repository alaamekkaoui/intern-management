from flask import flash, redirect, render_template, request
from models.department import Department
import traceback
from utils.log_utils import log_activity

class DepartmentController:
    # List all departments
    def list_departments(self):
        name = request.args.get('name', '').strip()
        departments = Department.get_all()
        if name:
            departments = [d for d in departments if name.lower() in d.get('name', '').lower()]
        return render_template('department/list.html', departments=departments, filter_name=name)

    # Show form to add a new department
    def show_add_department_form(self):
        return render_template('department/add.html')

    def add_department(self, request):
        name = request.form['name']
        
        try:
            # Check if the department already exists
            existing_department = Department.get_by_name(name)
            if existing_department:
                flash('Le département existe déjà.', 'danger')  # Error message if department already exists
                return redirect('/department/add')  # Redirect back to the add form
            
            # Attempt to add the department
            if not Department.add_department(name):
                flash("Une erreur s'est produite lors de l'ajout du département.", 'danger')  # Error message if adding fails
                print('Error adding department: Failed to add department')  # Log error
            else:
                # Get the new department's ID
                departments = Department.get_all()
                new_department = next((d for d in departments if d.get('name') == name), None)
                log_activity('add', 'department', new_department['id'] if new_department else None)
                flash('Le département a été ajouté avec succès!', 'success')  # Success message
            
        except Exception as e:
            # Handle any unexpected errors that occur during the process
            flash(f"Une erreur s'est produite: {str(e)}", 'danger')  # Flash the error message
            print(f"Error: {str(e)}")  # Log the exception message
            print("Stack trace:")
            print(traceback.format_exc())  # Print the detailed stack trace for debugging
        
        # Redirect back to the department list page
        return redirect('/department')

    # Show form to edit an existing department
    def show_edit_department_form(self, department_id):
        try:
            department_id = int(department_id)
        except (TypeError, ValueError):
            flash("ID de département invalide.", "danger")
            return redirect('/department')
        department = Department.get_by_id(department_id)
        return render_template('department/edit.html', department=department)

    # Edit an existing department
    def edit_department(self, department_id, request):
        try:
            department_id = int(department_id)
        except (TypeError, ValueError):
            flash("ID de département invalide.", "danger")
            return redirect('/department')
        name = request.form['name']
        
        # Check if the department already exists with this name (excluding current department)
        existing_department = Department.get_by_name(name)
        if existing_department and existing_department['id'] != department_id:
            flash('Le département avec ce nom existe déjà.', 'danger')  # Error message if department exists
            return redirect(f'/department/edit/{department_id}')  # Redirect back to the edit form

        # If no errors, update the department
        if Department.update_department(department_id, name):
            log_activity('update', 'department', department_id)
            flash('Le département a été mis à jour avec succès!', 'success')  # Success message
        else:
            flash("Une erreur s'est produite lors de la mise à jour du département.", 'danger')  # Error message
        return redirect('/department')

    # Delete a department
    def delete_department(self, department_id):
        try:
            department_id = int(department_id)
        except (TypeError, ValueError):
            flash("ID de département invalide.", "danger")
            return redirect('/department')
        department = Department.get_by_id(department_id)
        
        if not department:
            flash("Le département n'existe pas.", 'danger')  # Error message if department does not exist
            return redirect('/department')
        
        # If the department exists, proceed with deletion
        Department.delete_department(department_id)
        log_activity('delete', 'department', department_id)
        flash('Le département a été supprimé avec succès.', 'success')  # Success message
        return redirect('/department')
