from django.db import models
from datetime import timedelta, datetime, date
from django.utils.timezone import localtime


# Create your models here.

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # Automatically increments
    student_fullname = models.CharField(max_length=50)
    student_email = models.EmailField(max_length=50, unique=True)  # Enforce unique emails
    birth_date = models.DateField()
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.student_fullname} (ID: {self.student_id})"




# class Class(models.Model):
#     class_id = models.AutoField(primary_key=True)  # Automatically increments
#     student_id = models.ForeignKey('Student', on_delete=models.CASCADE)  # Relates to the Student model
#     course_code = models.CharField(max_length=50)
#     class_name = models.CharField(max_length=100)
#     class_time = models.DateTimeField()
#     room_number = models.CharField(max_length=10)
#     max_students = models.IntegerField()

#     def __str__(self):
#         return f'{self.class_name} - {self.course_code}'
    
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)  # Relates to the Student model
    course_code = models.CharField(max_length=50)
    class_name = models.CharField(max_length=100)
    class_time = models.DateTimeField()
    room_number = models.CharField(max_length=10)
    max_students = models.IntegerField()

    def __str__(self):
        return f'{self.class_name} - {self.course_code}'
    
class ClassList(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return self.name
    

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add this field
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')])

    def __str__(self):
        return f"{self.student} - {self.class_name} ({self.date})"
