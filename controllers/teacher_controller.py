from flask import render_template, request, redirect, flash
from models.teacher import Teacher
from models.department import Department

class TeacherController:
    # List all teachers
    def list_teachers(self):
        teachers = Teacher.get_all()
        return render_template('teacher/list.html', teachers=teachers)

    # Show form to add a new teacher
    def show_add_teacher_form(self):
        departments = Department.get_all()
        return render_template('teacher/add.html', departments=departments)

    # Add a new teacher
    def add_teacher(self, request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form.get('department')
        email = request.form['email']
        phone = request.form['phone']

        # Attempt to add the teacher
        try:
            Teacher.add_teacher(first_name, last_name, department_id, email, phone)
            flash('L\'enseignant a été ajouté avec succès!', 'success')
        except Exception as e:
            flash(f"Une erreur s'est produite lors de l'ajout de l'enseignant: {str(e)}", 'danger')

        return redirect('/teacher')

    # Update teacher information
    def edit_teacher(self, teacher_id, request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form.get('department')
        email = request.form['email']
        phone = request.form['phone']

        # Attempt to update teacher info
        try:
            Teacher.update_teacher(teacher_id, first_name, last_name, department_id, email, phone)
            flash('Les informations de l\'enseignant ont été mises à jour avec succès.', 'success')
        except Exception as e:
            flash(f"Une erreur s'est produite lors de la mise à jour des informations de l'enseignant: {str(e)}", 'danger')

        return redirect('/teacher')

    # Delete a teacher
    def delete_teacher(self, teacher_id):
        try:
            Teacher.delete_teacher(teacher_id)
            flash('L\'enseignant a été supprimé avec succès.', 'success')
        except Exception as e:
            flash(f"Une erreur s'est produite lors de la suppression de l'enseignant: {str(e)}", 'danger')

        return redirect('/teacher')
