from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Class, Student
from .forms import ClassForm, StudentForm, UserRegistrationForm, UserUpdateForm, LoginForm
import csv
from django.contrib.auth.models import User

# Public views: login and register
def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_list')  # Redirect to user list if already logged in
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_list')  # Redirect to a view after successful login
    else:
        form = LoginForm()
    return render(request, 'samsapp/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('user_list')  # Redirect to user list if already logged in
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'samsapp/register.html', {'form': form})

# Protected views (only accessible to logged-in users)
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'samsapp/user_list.html', {'users': users})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'samsapp/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'samsapp/student_form.html', {'form': form})

@login_required
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

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')

@login_required
def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student.student_id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Name', 'Email', 'Birth Date', 'Enrollment Date'])
    writer.writerow([
        student.student_id,
        student.student_fullname or '',
        student.student_email or '',
        student.birth_date or '',
        student.enrollment_date or ''
    ])
    return response

@login_required
def some_view(request):
    return HttpResponse("Hello, this is the Ephan view!")

@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'samsapp/class_list.html', {'classes': classes})

@login_required
def class_add(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'samsapp/class_form.html', {'form': form})

@login_required
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

@login_required
def class_delete(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        class_instance.delete()
        return redirect('class_list')
    return render(request, 'samsapp/class_confirm_delete.html', {'class': class_instance})

@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information updated successfully!')
            return redirect('user_list')  # Redirect to user list after update
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'samsapp/user_update.html', {'form': form})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, 'User account deleted successfully!')
        return redirect('user_list')
    
    # Render confirmation page for GET request
    return render(request, 'samsapp/user_delete.html', {'user': user})



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
