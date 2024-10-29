from django.urls import path
from . import views


urlpatterns = [
    path('ephan/', views.some_view, name='ephan'),
    path('student/new/', views.student_create, name='student_create'),
    path('student/edit/<int:pk>/', views.student_update, name='student_update'),
    path('student/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/', views.student_list, name='student_list'), 
    path('student/report/', views.student_report, name='student_report'),
    path('student/report/<int:pk>/', views.student_report, name='student_report'),
    path('classes/add/', views.class_add, name='class_add'),# Class URLs
    path('classes/update/<int:class_id>/', views.class_update, name='class_update'),
    path('classes/delete/<int:class_id>/', views.class_delete, name='class_delete'),
    path('classes/', views.class_list, name='class_list'),
    path('register/', views.register, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('users/update/<int:user_id>/', views.user_update, name='user_update'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('login/', views.login_view, name='login'),  # Add this line
    path('logout/', views.logout_view, name='logout'),

]
    