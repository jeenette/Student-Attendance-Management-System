from django import forms
from .models import Student
from .models import Class
from django.contrib.auth.models import User

from .models import Attendance



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_fullname', 'student_email', 'birth_date', 'enrollment_date']
        
        widgets = {
            'student_fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['student_id', 'course_code', 'class_name', 'class_time', 'room_number', 'max_students']
        widgets = {
            'class_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    # Optionally, customize the student_id field to show student IDs
    student_id = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Select Student")

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_name', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }