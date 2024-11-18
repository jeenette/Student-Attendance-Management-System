import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Class, Student
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import UserRegistrationForm, UserUpdateForm, StudentForm, ClassForm, LoginForm

# Use the login_required decorator for views that require login
@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'samsapp/student_list.html', {'students': students})

@login_required(login_url='login')
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'samsapp/student_form.html', {'form': form})

@login_required(login_url='login')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'samsapp/student_form.html', {'form': form, 'is_update': True})

        #cleaned_data = super().clean()
        #birth_date = cleaned_data.get('birth_date')
        #enrollment_date = cleaned_data.get('enrollment_date')

        #if birth_date and enrollment_date:
            #if birth_date == enrollment_date:
               # raise ValidationError("Birth date and enrollment date cannot be the same.")
        
        #return cleaned_data
@login_required(login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return redirect('student_list')

@login_required(login_url='login')
def student_report(request, pk):
    try:
        # Get the specific student by ID
        student = get_object_or_404(Student, pk=pk)
        
        # Create the HTTP response with CSV content type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="student_report_{student.student_id}.csv"'

        writer = csv.writer(response)
        # Add the header row including Student ID
        writer.writerow(['Student ID', 'Name', 'Email', 'Birth Date', 'Enrollment Date'])

        # Write the specific student's data to the CSV, including Student ID
        writer.writerow([
            student.student_id,  # Include the Student ID here
            student.student_fullname or '',
            student.student_email or '',
            student.birth_date or '',
            student.enrollment_date or ''
        ])

        return response
    except Exception as e:
        print(f"Error generating report: {e}")
        return HttpResponse("Error generating report.", status=500)
    
def some_view(request):
    return HttpResponse("Hello, this is the Ephan view!")

@login_required(login_url='login')
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'samsapp/class_list.html', {'classes': classes})

@login_required(login_url='login')
def class_add(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'samsapp/class_form.html', {'form': form})

@login_required(login_url='login')
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

@login_required(login_url='login')
def class_delete(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        class_instance.delete()
        return redirect('class_list')
    return render(request, 'samsapp/class_confirm_delete.html', {'class': class_instance})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'samsapp/register.html', {'form': form})

@login_required(login_url='login')
def user_list(request):
    users = User.objects.all()
    return render(request, 'samsapp/user_list.html', {'users': users})

@login_required(login_url='login')
def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information updated successfully!')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'samsapp/user_update.html', {'form': form})

@login_required(login_url='login')
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, 'User account deleted successfully!')
        return redirect('user_list')
    return render(request, 'samsapp/user_confirm_delete.html', {'user': user})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')  # Get the 'next' parameter
                if not next_url:  # If 'next' is empty, fallback to user_list
                    next_url = 'user_list'  # Ensure this view is defined in your urlpatterns
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'samsapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
