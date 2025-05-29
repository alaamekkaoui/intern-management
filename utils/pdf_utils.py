from fpdf import FPDF
import io
import openpyxl
from openpyxl.workbook import Workbook

def add_iav_logo(pdf):
    # Add the IAV logo centered at the top
    logo_path = 'static/images/iav.png'
    page_width = pdf.w - 2 * pdf.l_margin
    logo_width = 40
    x = (pdf.w - logo_width) / 2
    pdf.image(logo_path, x=x, y=10, w=logo_width)
    pdf.ln(30)  # Add space below the logo

def export_teachers_pdf(teachers):
    pdf = FPDF()
    pdf.add_page()
    add_iav_logo(pdf)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Teachers List', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'First Name', 1)
    pdf.cell(40, 10, 'Last Name', 1)
    pdf.cell(60, 10, 'Email', 1)
    pdf.cell(30, 10, 'Phone', 1)
    pdf.cell(0, 10, 'Department', 1, ln=True)
    pdf.set_font('Arial', '', 12)
    for t in teachers:
        pdf.cell(40, 10, str(t.get('first_name', '')), 1)
        pdf.cell(40, 10, str(t.get('last_name', '')), 1)
        pdf.cell(60, 10, str(t.get('email', '')), 1)
        pdf.cell(30, 10, str(t.get('phone', '')), 1)
        pdf.cell(0, 10, str(t.get('department_name', '')), 1, ln=True)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def sample_teacher_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Teachers"
    # Header
    ws.append(["First Name", "Last Name", "Email", "Phone", "Department"])
    # Sample row
    ws.append(["John", "Doe", "john.doe@example.com", "1234567890", "Computer Science"])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def export_teachers_xlsx(teachers):
    wb = Workbook()
    ws = wb.active
    ws.title = "Teachers"
    ws.append(["First Name", "Last Name", "Email", "Phone", "Department"])
    for t in teachers:
        ws.append([
            t.get('first_name', ''),
            t.get('last_name', ''),
            t.get('email', ''),
            t.get('phone', ''),
            t.get('department_name', '')
        ])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def import_teachers_from_xlsx(file):
    from models.teacher import Teacher
    from models.department import Department
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    count = 0
    errors = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row = list(row)
        if len(row) < 5 or all(cell is None for cell in row):
            errors.append(f"Ligne {i}: Données manquantes ou ligne vide.")
            continue
        first_name, last_name, email, phone, department_name = row[:5]
        if not (first_name and last_name and email and department_name):
            errors.append(f"Ligne {i}: Données manquantes.")
            continue
        department = Department.get_by_name(department_name)
        if not department:
            errors.append(f"Ligne {i}: Département '{department_name}' introuvable.")
            continue
        success = Teacher.add_teacher(first_name, last_name, department['id'], email, phone)
        if success:
            count += 1
        else:
            errors.append(f"Ligne {i}: Erreur lors de l'ajout de l'enseignant.")
    return count, errors

def export_internships_xlsx(internships):
    wb = Workbook()
    ws = wb.active
    ws.title = "Internships"
    ws.append(["Title", "Teacher", "Start Date", "End Date", "Status", "Car", "Intern Type"])
    for i in internships:
        ws.append([
            i.get('title', ''),
            f"{i.get('first_name', '')} {i.get('last_name', '')}",
            i.get('start_date', ''),
            i.get('end_date', ''),
            i.get('status', ''),
            i.get('car_model', ''),
            i.get('intern_type', '')
        ])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def export_cars_xlsx(cars):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cars"
    ws.append(["Name", "Model", "Type", "Brand", "License Plate", "Cost/Day", "Available Count"])
    for c in cars:
        ws.append([
            c.get('name', ''),
            c.get('model', ''),
            c.get('car_type', ''),
            c.get('brand', ''),
            c.get('license_plate', ''),
            c.get('average_cost_per_day', ''),
            c.get('available_count', '')
        ])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def export_departments_xlsx(departments):
    wb = Workbook()
    ws = wb.active
    ws.title = "Departments"
    ws.append(["Name"])
    for d in departments:
        ws.append([d.get('name', '')])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def sample_department_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Departments"
    ws.append(["Name"])
    ws.append(["Mathematics"])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def import_departments_from_xlsx(file):
    from models.department import Department
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    count = 0
    errors = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row = list(row)
        if len(row) < 1 or not row[0]:
            errors.append(f"Ligne {i}: Nom du département manquant.")
            continue
        name = row[0]
        existing = Department.get_by_name(name)
        if existing:
            errors.append(f"Ligne {i}: Département '{name}' existe déjà.")
            continue
        success = Department.add_department(name)
        if success:
            count += 1
        else:
            errors.append(f"Ligne {i}: Erreur lors de l'ajout du département.")
    return count, errors

def export_departments_pdf(departments):
    pdf = FPDF()
    pdf.add_page()
    add_iav_logo(pdf)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Departments List', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Name', 1, ln=True)
    pdf.set_font('Arial', '', 12)
    for d in departments:
        pdf.cell(0, 10, d.get('name', ''), 1, ln=True)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def export_internships_pdf(internships):
    pdf = FPDF()
    pdf.add_page()
    add_iav_logo(pdf)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Internships List', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Title', 1)
    pdf.cell(40, 10, 'Teacher', 1)
    pdf.cell(25, 10, 'Start', 1)
    pdf.cell(25, 10, 'End', 1)
    pdf.cell(20, 10, 'Status', 1)
    pdf.cell(30, 10, 'Car', 1)
    pdf.cell(0, 10, 'Type', 1, ln=True)
    pdf.set_font('Arial', '', 10)
    for i in internships:
        pdf.cell(30, 10, str(i.get('title', '')), 1)
        pdf.cell(40, 10, f"{i.get('first_name', '')} {i.get('last_name', '')}", 1)
        pdf.cell(25, 10, str(i.get('start_date', '')), 1)
        pdf.cell(25, 10, str(i.get('end_date', '')), 1)
        pdf.cell(20, 10, str(i.get('status', '')), 1)
        pdf.cell(30, 10, str(i.get('car_model', '')), 1)
        pdf.cell(0, 10, str(i.get('intern_type', '')), 1, ln=True)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def export_cars_pdf(cars):
    pdf = FPDF()
    pdf.add_page()
    add_iav_logo(pdf)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Cars List', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Name', 1)
    pdf.cell(25, 10, 'Model', 1)
    pdf.cell(25, 10, 'Type', 1)
    pdf.cell(25, 10, 'Brand', 1)
    pdf.cell(30, 10, 'License', 1)
    pdf.cell(25, 10, 'Cost/Day', 1)
    pdf.cell(0, 10, 'Available', 1, ln=True)
    pdf.set_font('Arial', '', 10)
    for c in cars:
        pdf.cell(30, 10, str(c.get('name', '')), 1)
        pdf.cell(25, 10, str(c.get('model', '')), 1)
        pdf.cell(25, 10, str(c.get('car_type', '')), 1)
        pdf.cell(25, 10, str(c.get('brand', '')), 1)
        pdf.cell(30, 10, str(c.get('license_plate', '')), 1)
        pdf.cell(25, 10, str(c.get('average_cost_per_day', '')), 1)
        pdf.cell(0, 10, str(c.get('available_count', '')), 1, ln=True)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def sample_intern_type_xlsx():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Internship Types"
    ws.append(["Name"])
    ws.append(["Stage terrain"])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def import_intern_types_from_xlsx(file):
    from models.intern_type import InternType
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    count = 0
    errors = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row = list(row)
        if len(row) < 1 or not row[0]:
            errors.append(f"Ligne {i}: Nom du type manquant.")
            continue
        name = row[0]
        # Check for duplicate
        existing = [t for t in InternType.get_all() if t['name'].strip().lower() == name.strip().lower()]
        if existing:
            errors.append(f"Ligne {i}: Type '{name}' existe déjà.")
            continue
        try:
            InternType.add_intern_type(name)
            count += 1
        except Exception as e:
            errors.append(f"Ligne {i}: Erreur lors de l'ajout du type: {e}")
    return count, errors

def export_internship_types_xlsx(internship_types):
    from openpyxl import Workbook
    import io
    wb = Workbook()
    ws = wb.active
    ws.title = "Internship Types"
    ws.append(["Name"])
    for t in internship_types:
        ws.append([t.get('name', '')])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def generate_students_pdf(students):
    pdf = FPDF()
    pdf.add_page()
    add_iav_logo(pdf)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Students List', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'First Name', 1)
    pdf.cell(40, 10, 'Last Name', 1)
    pdf.cell(60, 10, 'Email', 1)
    pdf.cell(30, 10, 'Phone', 1)
    pdf.cell(0, 10, 'Internship', 1, ln=True)
    pdf.set_font('Arial', '', 12)
    for s in students:
        pdf.cell(40, 10, str(s.get('first_name', '')), 1)
        pdf.cell(40, 10, str(s.get('last_name', '')), 1)
        pdf.cell(60, 10, str(s.get('email', '')), 1)
        pdf.cell(30, 10, str(s.get('phone', '')), 1)
        internship = s.get('internship_title', '') if s.get('internship_title') else ''
        pdf.cell(0, 10, internship, 1, ln=True)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def sample_student_xlsx():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Students"
    ws.append(["first_name", "last_name", "email", "phone", "internship_id", "teacher_id"])
    ws.append(["John", "Doe", "john.doe@email.com", "0612345678", 1, 1])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def sample_car_xlsx():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Cars"
    ws.append(["Name", "Model", "Type", "Brand", "License Plate", "Cost/Day", "Available Count"])
    ws.append(["Car A", "4x4", "SUV", "Toyota", "ABC-123", 100.00, 2])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def sample_internship_xlsx():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Internships"
    ws.append(["Title", "Teacher ID", "Intern Type ID", "Car ID", "Start Date", "End Date", "Status", "Num Ordre Mission", "Description", "Destination", "Kilometrage"])
    ws.append(["AI Research", 1, 1, 1, "2024-07-01", "2024-08-01", "pending", "ORD-001", "Research on AI", "Rabat", 120])
    xlsx_io = io.BytesIO()
    wb.save(xlsx_io)
    xlsx_io.seek(0)
    return xlsx_io

def import_cars_from_xlsx(file):
    from models.car import Car
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    count = 0
    errors = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row = list(row)
        if len(row) < 7 or all(cell is None for cell in row):
            errors.append(f"Ligne {i}: Données manquantes ou ligne vide.")
            continue
        name, model, car_type, brand, license_plate, cost_per_day, available_count = row[:7]
        if not (name and model and car_type and brand and license_plate and cost_per_day is not None and available_count is not None):
            errors.append(f"Ligne {i}: Données manquantes.")
            continue
        try:
            success = Car.add_car(name, model, car_type, brand, license_plate, cost_per_day, available_count)
            if success:
                count += 1
            else:
                errors.append(f"Ligne {i}: Erreur lors de l'ajout de la voiture.")
        except Exception as e:
            errors.append(f"Ligne {i}: Erreur lors de l'ajout de la voiture: {e}")
    return count, errors

def import_internships_from_xlsx(file):
    from models.internship import Internship
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    count = 0
    errors = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        row = list(row)
        if len(row) < 11 or all(cell is None for cell in row):
            errors.append(f"Ligne {i}: Données manquantes ou ligne vide.")
            continue
        title, teacher_id, intern_type_id, car_id, start_date, end_date, status, num_ordre_mission, description, destination, kilometrage = row[:11]
        if not (title and teacher_id and intern_type_id and start_date and end_date and status):
            errors.append(f"Ligne {i}: Données obligatoires manquantes.")
            continue
        try:
            success = Internship.add_internship(teacher_id, intern_type_id, car_id, start_date, end_date, num_ordre_mission, description, destination, kilometrage)
            if success:
                count += 1
            else:
                errors.append(f"Ligne {i}: Erreur lors de l'ajout du stage.")
        except Exception as e:
            errors.append(f"Ligne {i}: Erreur lors de l'ajout du stage: {e}")
    return count, errors