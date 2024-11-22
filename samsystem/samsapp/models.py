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
    
class ClassList(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return self.name
    

class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('P', 'Present'),
        ('L', 'Late'),
        ('A', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ATTENDANCE_CHOICES, default='A')

    def is_late(self, actual_time):
        """
        Checks if the student is late based on class time and actual attendance time.
        """
        class_time = localtime(self.class_name.class_time).time()
        late_time = (datetime.combine(date.today(), class_time) + timedelta(minutes=15)).time()
        return actual_time > late_time

    def __str__(self):
        return f"{self.student.student_fullname} - {self.get_status_display()} on {self.date}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'class_name')  # Ensure a student can only enroll in a class once

    def __str__(self):
        return f"{self.student.student_fullname} enrolled in {self.class_name.class_name}"