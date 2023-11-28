from django.urls import path, include
from .views import StudentListView, StudentDetailView, \
    MainListView, TeacherProfileView, StudentProfileView, \
    login_view, logout_view, TeacherGroupView, \
    StudentGradesView, teacher_subject_grades, \
    update_grade, calculate_and_save_result, calculate_and_save_result_srsone


urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home', MainListView.as_view(), name='home'),
    path('students', StudentListView.as_view()),
    path('teacher_groups/<slug:slug>/', TeacherGroupView.as_view(), name='teacher_groups'),
    path('<slug:slug>/', StudentDetailView.as_view(), name='table2'),
    path('grades/<slug:slug>/', StudentGradesView.as_view(), name='grades'),
    path('teacher/<str:teacher_url>/<str:group_link>/grades/', teacher_subject_grades, name='teacher_subject_grades'),
    path('teacher/<str:teacher_url>/<str:group_link>/grades/update_grade/', update_grade, name='update_grade'),
    path('teacher/<slug:teacher_url>/<slug:group_link>/grades/calculate/', calculate_and_save_result,
         name='calculate_and_save_result'),
    path('teacher/<slug:teacher_url>/<slug:group_link>/grades/calculate_srsone/', calculate_and_save_result_srsone,
         name='calculate_and_save_result_srsone'),
    path('teacher_profile/<slug:slug>/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('student_profile/<slug:slug>/', StudentProfileView.as_view(), name='student_profile'),
    path('__debug__/', include('debug_toolbar.urls')),
]
