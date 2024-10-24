from django.shortcuts import render, HttpResponse
import csv
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
import logging

logger = logging.getLogger(__name__)

def student_report(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        ...
    except Student.DoesNotExist:
        logger.error(f"Student with ID {student_id} does not exist.")
        return HttpResponse("Student not found.", status=404)
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return HttpResponse("Error generating report.", status=500)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'samsapp/student_list.html', {'students': students})

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'samsapp/student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'samsapp/student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'samsapp/student_confirm_delete.html', {'student': student})

def student_report(request, student_id):
    try:
        # Retrieve the student with the given student_id
        student = Student.objects.get(student_id=student_id)

        # Prepare the CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{student.student_fullname}_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Birth Date', 'Enrollment Date'])

        # Write the student's data
        writer.writerow([
            student.student_fullname or '',  # Handle empty fields
            student.student_email or '',
            student.birth_date or '',
            student.enrollment_date or ''
        ])

        return response
    except Student.DoesNotExist:
        return HttpResponse("Student not found.", status=404)
    except Exception as e:
        # Log the error or print it for debugging
        print(f"Error generating report: {e}")
        return HttpResponse("Error generating report.", status=500)
def some_view(request):
    return HttpResponse("Hello, this is the Ephan view!")