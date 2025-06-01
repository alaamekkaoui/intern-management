from flask import render_template, request, redirect, flash, url_for, session
from models.student import Student
from models.internship import Internship
from models.intern_type import InternType

class StudentController:    
    def list_students(self):
        # Get filter parameters
        name = request.args.get('name', '').strip()
        intern_type_id = request.args.get('intern_type_id', '').strip()
        
        # Get all students with their related data
        students = Student.get_all()
        internships = Internship.get_all()
        
        # Apply filters
        if name:
            # Improved name search to handle partial matches better
            name_lower = name.lower()
            filtered_students = []
            for student in students:
                full_name = f"{student.get('first_name', '')} {student.get('last_name', '')}".lower()
                if name_lower in full_name or name_lower in student.get('first_name', '').lower() or name_lower in student.get('last_name', '').lower():
                    filtered_students.append(student)
            students = filtered_students
            
        if intern_type_id and intern_type_id.isdigit():
            # Filter by internship type
            students = [s for s in students if str(s.get('intern_type_id', '')) == intern_type_id]
        
        # Get intern types for the filter dropdown
        intern_types = InternType.get_all()
        
        return render_template(
            'student/list.html',
            students=students,
            intern_types=intern_types,
            internships=internships,
            filter_name=name,
            filter_intern_type_id=intern_type_id
        )

    def show_add_student_form(self, internship_id=None):
        from models.teacher import Teacher
        from models.intern_type import InternType
        from models.internship import Internship
        teachers = Teacher.get_all()
        intern_types = InternType.get_all()
        internships = Internship.get_all()
        return render_template('student/add.html', teachers=teachers, intern_types=intern_types, internships=internships, internship_id=internship_id)

    def add_student(self, request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form.get('email')
        phone = request.form.get('phone')
        internship_id = request.form.get('internship_id')
        print(f"[STUDENT ADD] User '{session.get('username')}' added student '{first_name} {last_name}' at {__import__('datetime').datetime.now()}")
        student_id = Student.add_student(first_name, last_name, email, phone)
        if internship_id:
            Student.assign_internship(student_id, internship_id)
        flash('Étudiant ajouté avec succès.', 'success')
        return redirect('/student')

    def show_assign_internship_form(self, student_id):
        student = Student.get_by_id(student_id)
        internships = Internship.get_all()
        return render_template('student/assign_internship.html', student=student, internships=internships)

    def assign_internship(self, student_id, request):
        internship_id = request.form['internship_id']
        Student.assign_internship(student_id, internship_id)
        flash("Stage affecté à l'étudiant (et enseignant associé).", 'success')
        return redirect('/student')

    def import_students_xlsx(self, rows, internship_id=None):
        for row in rows:
            student_id = Student.add_student(row.get('first_name'), row.get('last_name'), row.get('email'), row.get('phone'))
            if internship_id:
                Student.assign_internship(student_id, internship_id)
        flash('Importation des étudiants terminée.', 'success')
        return redirect('/student')

    def add_student_to_internship(self, internship_id, request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form.get('email')
        phone = request.form.get('phone')
        student_id = Student.add_student(first_name, last_name, email, phone)
        Student.assign_internship(student_id, internship_id)
        flash('Étudiant ajouté à ce stage avec succès.', 'success')
        return redirect(f'/internship/details/{internship_id}')

    def edit_student(self, student_id):
        from models.student import Student
        if session.get('role') not in ['admin', 'teacher']:
            flash('Accès refusé.', 'danger')
            return redirect(url_for('student_list'))
        student = Student.get_by_id(student_id)
        if not student:
            flash('Étudiant introuvable.', 'danger')
            return redirect(url_for('student_list'))
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form.get('email', '')
            phone = request.form.get('phone', '')
            internship_id = request.form.get('internship_id')
            print(f"[STUDENT EDIT] User '{session.get('username')}' edited student ID {student_id} at {__import__('datetime').datetime.now()}")
            Student.update_student(student_id, first_name, last_name, email, phone, internship_id)
            flash('Étudiant modifié avec succès.', 'success')
            return redirect(url_for('student_list'))
        from models.intern_type import InternType
        from models.internship import Internship
        intern_types = InternType.get_all()
        internships = Internship.get_all()
        return render_template('student/edit.html', student=student, intern_types=intern_types, internships=internships)

    def delete_student(self, student_id):
        from models.student import Student
        if session.get('role') not in ['admin', 'teacher']:
            flash('Accès refusé.', 'danger')
            return redirect(url_for('student_list'))
        student = Student.get_by_id(student_id)
        if not student:
            flash('Étudiant introuvable.', 'danger')
            return redirect(url_for('student_list'))
        print(f"[STUDENT DELETE] User '{session.get('username')}' deleted student ID {student_id} at {__import__('datetime').datetime.now()}")
        Student.delete_student(student_id)
        flash('Étudiant supprimé avec succès.', 'success')
        return redirect(url_for('student_list'))

    def show_student_details(self, student_id):
        student = Student.get_by_id(student_id)
        if not student:
            flash('Étudiant introuvable.', 'danger')
            return redirect(url_for('student_list'))
        
        # Get internship details if student has one
        internship = None
        if student.get('internship_id'):
            internship = Internship.get_by_id(student['internship_id'])
            
        return render_template('student/details.html', student=student, internship=internship)
