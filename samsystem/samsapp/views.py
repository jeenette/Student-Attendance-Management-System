from django.shortcuts import render, HttpResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Student
from .forms import ClassForm, StudentForm


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


def some_view(request):
    return HttpResponse("Hello, this is the Ephan view!")

# Class List
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'samsapp/class_list.html', {'classes': classes})

# Create Class
def class_add(request):
    print("class_create view called")  # Print statement for debugging
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form saved successfully")  # Print on successful form save
            return redirect('class_list')
        else:
            print("Form is not valid:", form.errors)  # Print form errors
    else:
        form = ClassForm()
    return render(request, 'samsapp/class_form.html', {'form': form})



# Update Class
def class_update(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        form = ClassForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm(instance=class_instance)
    return render(request, 'samsapp/class_form.html', {'form': form})

# Delete Class
def class_delete(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        class_instance.delete()
        return redirect('class_list')
    return render(request, 'samsapp/class_confirm_delete.html', {'class': class_instance})