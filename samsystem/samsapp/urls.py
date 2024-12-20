from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ephan/', views.some_view, name='ephan'),
   path('home/', views.home, name='home'),
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
    path('manage-notifications/', views.manage_notifications, name='manage_notifications'),
  
     path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('submit-attendance/', views.submit_attendance, name='submit_attendance'),  # Ensure this line exists


    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),
    

    # Attendance tracking page
    path('attendance/tracking/', views.attendance_tracking, name='attendance_tracking'),
    path('get_students_for_class/<int:class_id>/', views.get_students_for_class, name='get_students_for_class'),


    # Account settings page
   path('account/settings/', views.account_settings, name='account_settings'),
    
 path('dashboard/', views.dashboard, name='dashboard'),
 path('profile/', views.profile_view, name='profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_view, name='search_view'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)