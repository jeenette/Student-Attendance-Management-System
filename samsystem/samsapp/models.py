from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # Automatically increments
    student_id = models.AutoField(primary_key=True)
    student_fullname = models.CharField(max_length=50)
    student_email = models.EmailField(max_length=50)
    birth_date = models.DateField()
    enrollment_date = models.DateField()

    def __str__(self):
        return self.student_fullname
