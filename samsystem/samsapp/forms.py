from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_fullname', 'student_email', 'birth_date', 'enrollment_date']
