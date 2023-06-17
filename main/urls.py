from django.urls import path, include
from .views import StudentListView, StudentDetailView

urlpatterns = [
    path('', StudentListView.as_view()),
    path('<slug:slug>/', StudentDetailView.as_view(), name='table2'),
    path('__debug__/', include('debug_toolbar.urls')),
]
