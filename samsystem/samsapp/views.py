from django.shortcuts import render, HttpResponse

import csv
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()
    print(students)  # Check the output in the console
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

def student_report(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Birth Date', 'Enrollment Date'])

        students = Student.objects.all()
        for student in students:
            writer.writerow([
                student.student_fullname or '',  # Handle empty fields
                student.student_email or '',
                student.birth_date or '',
                student.enrollment_date or ''
            ])

        return response
    except Exception as e:
        # Log the error or print it for debugging
        print(f"Error generating report: {e}")
        return HttpResponse("Error generating report.", status=500)


def some_view(request):
    return HttpResponse("Hello, this is the Ephan view!")