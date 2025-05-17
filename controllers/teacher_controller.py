from flask import render_template, request, redirect, flash
from models.teacher import Teacher
from models.department import Department
from models.internship import Internship

class TeacherController:
    # List all teachers
    def list_teachers(self):
        name = request.args.get('name', '').strip()
        department_id = request.args.get('department_id', '').strip()
        teachers = Teacher.get_all()
        # Filter by name (partial match, case-insensitive)
        if name:
            teachers = [t for t in teachers if name.lower() in (t.get('first_name', '') + ' ' + t.get('last_name', '')).lower()]
        # Filter by department_id
        if department_id:
            teachers = [t for t in teachers if str(t.get('department_id')) == department_id]
        departments = Department.get_all()
        return render_template('teacher/list.html', teachers=teachers, departments=departments, filter_name=name, filter_department_id=department_id)

    # Show form to add a new teacher
    def show_add_teacher_form(self):
        departments = Department.get_all()
        return render_template('teacher/add.html', departments=departments)

    # Add a new teacher with check for existing teacher
    def add_teacher(self, request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form.get('department')
        email = request.form['email']
        phone = request.form['phone']

        existing_teacher_by_email = Teacher.get_by_email(email)
        if existing_teacher_by_email:
            flash('Un enseignant avec cet email existe déjà.', 'danger')
            return redirect('/teacher/add')

        # Check if the teacher already exists by name (first and last name)
        existing_teacher_by_name = Teacher.get_by_name(first_name, last_name)

        if existing_teacher_by_name:
            flash('Un enseignant avec ce nom existe déjà.', 'danger')
            return redirect('/teacher/add')
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

    # Show details for a single teacher
    def show_teacher_details(self, teacher_id):
        teacher = Teacher.get_by_id(teacher_id)
        internships = Internship.get_by_teacher_id(teacher_id)
        departments = Department.get_all()
        return render_template('teacher/details.html', teacher=teacher, internships=internships, departments=departments)
