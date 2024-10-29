from django.shortcuts import render, HttpResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Student
from .forms import ClassForm, StudentForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout


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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Change to your login URL
    else:
        form = UserRegistrationForm()
    return render(request, 'samsapp/register.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'samsapp/user_list.html', {'users': users})

def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information updated successfully!')
            return redirect('user_list')  # Change to your user list URL
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'samsapp/user_update.html', {'form': form})

def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'User account deleted successfully!')
    return redirect('user_list')  # Change to your user list URL

def login_view(request):
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


def logout_view(request):
    logout(request)
    return redirect('login')