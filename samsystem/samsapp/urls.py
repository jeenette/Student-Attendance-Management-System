from django.urls import path
from . import views

urlpatterns = [
    path('ephan/', views.some_view, name='ephan'),
    path('student/new/', views.student_create, name='student_create'),
    path('student/edit/<int:pk>/', views.student_update, name='student_update'),
    path('student/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/', views.student_list, name='student_list'), 
]
    path('students/', views.student_list, name='student_list'),
    path('student/report/', views.student_report, name='student_report'),
]