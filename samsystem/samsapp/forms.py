from django import forms
from .models import Student
from .models import Class


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_fullname', 'student_email', 'birth_date', 'enrollment_date']
        
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['student_id', 'course_code', 'class_name', 'class_time', 'room_number', 'max_students']

