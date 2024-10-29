from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # Automatically increments
    student_fullname = models.CharField(max_length=50)
    student_email = models.EmailField(max_length=50)
    birth_date = models.DateField()
    enrollment_date = models.DateField()

    def __str__(self):
        return self.student_fullname


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)  # Automatically increments
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)  # Relates to the Student model
    course_code = models.CharField(max_length=50)
    class_name = models.CharField(max_length=100)
    class_time = models.DateTimeField()
    room_number = models.CharField(max_length=10)
    max_students = models.IntegerField()

    def __str__(self):
        return f'{self.class_name} - {self.course_code}'

