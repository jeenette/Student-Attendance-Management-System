"""
URL configuration for samsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from samsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('samsapp.urls')),
    
    # Additional views (these should be managed in samsapp.urls)
    path('ephan/', views.some_view, name='ephan'),
 # Student URLs
    path('student/new/', views.student_create, name='student_create'),
    path('student/edit/<int:pk>/', views.student_update, name='student_update'),
    path('student/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/', views.student_list, name='student_list'),
    path('student/report/', views.student_report, name='student_report_overview'),
    path('student/report/<int:pk>/', views.student_report, name='student_report'),
    
    
    # Class URLs
    path('classes/add/', views.class_add, name='class_add'),
    path('classes/update/<int:class_id>/', views.class_update, name='class_update'),
    path('classes/delete/<int:class_id>/', views.class_delete, name='class_delete'),
    path('classes/', views.class_list, name='class_list'),
    
    # User management
    path('register/', views.register, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('users/update/<int:user_id>/', views.user_update, name='user_update'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    
    # Authentication
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),

# Attendance
 path('', views.home, name='home'),

 # Attendance tracking page
    path('attendance/tracking/', views.attendance_tracking, name='attendance_tracking'),
    
    # Account settings page
    path('account/settings/', views.account_settings, name='account_settings'),
  

path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
   
]

