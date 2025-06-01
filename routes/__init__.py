from .car_routes import register_car_routes
from .department_routes import register_department_routes
from .teacher_routes import register_teacher_routes
from .internship_routes import register_internship_routes
from .user_routes import register_user_routes
from .internship_type_routes import register_internship_type_routes
from .misc_routes import register_misc_routes
from .student_routes import register_student_routes

def init_app(app):
    register_car_routes(app)
    register_department_routes(app)
    register_teacher_routes(app)
    register_internship_routes(app)
    register_user_routes(app)
    register_internship_type_routes(app)
    register_misc_routes(app)
    register_student_routes(app) 