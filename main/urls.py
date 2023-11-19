from django.urls import path, include
from .views import StudentListView, StudentDetailView, \
    MainListView, TeacherProfileView, StudentProfileView, \
    login_view, logout_view, TeacherGroupView, \
    StudentGradesView, teacher_subject_grades, get_grade, save_grade


urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home', MainListView.as_view(), name='home'),
    path('students', StudentListView.as_view()),
    path('teacher_groups/<slug:slug>/', TeacherGroupView.as_view(), name='teacher_groups'),
    path('<slug:slug>/', StudentDetailView.as_view(), name='table2'),
    path('grades/<slug:slug>/', StudentGradesView.as_view(), name='grades'),
    path('teacher/<str:teacher_url>/<str:group_link>/grades/', teacher_subject_grades, name='teacher_subject_grades'),
    path('get_grade/', get_grade, name='get_grade'),
    path('save_grade/', save_grade, name='save_grade'),
    path('teacher_profile/<slug:slug>/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('student_profile/<slug:slug>/', StudentProfileView.as_view(), name='student_profile'),
    path('__debug__/', include('debug_toolbar.urls')),
]
