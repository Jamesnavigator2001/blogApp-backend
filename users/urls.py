from .views import (
    StudentLoginView, RegisterStudentView,
    SuperAdminLoginView, RegisterTeacherView,
    TeacherLoginView, GetAllStudents, GetAllTeachers
)
from django.urls import path


urlpatterns = [
       # Student endpoints
    path('api/students/login/', StudentLoginView.as_view(), name='login_student'),
    path('api/students/register/', RegisterStudentView.as_view(), name='register_student'),
    path('api/students/', GetAllStudents.as_view(), name='get_all_students'),

    # Teacher endpoints
    path('api/teachers/register/', RegisterTeacherView.as_view(), name='register_teacher'),
    path('api/teachers/login/', TeacherLoginView.as_view(), name='login_teacher'),
    path('api/teachers/', GetAllTeachers.as_view(), name='get_all_teachers'),  

     # Super admin
    path('api/super-admin-login/', SuperAdminLoginView.as_view(), name='super_admin_login'),
]