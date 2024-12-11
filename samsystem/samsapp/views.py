import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Class
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import UserRegistrationForm, UserUpdateForm, StudentForm, ClassForm, LoginForm
from .models import Notification, ClassList
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Student
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponseForbidden

from .forms import AttendanceForm
from .models import Attendance

@login_required(login_url='login')
def mark_attendance(request, student_id, class_id):
    try:
        student = Student.objects.get(id=student_id)
        class_instance = Class.objects.get(id=class_id)
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            class_name=class_instance,
            date=request.POST.get('date', None),
        )
        
        if request.method == "POST":
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance.status = form.cleaned_data.get('status', 'A')  # default to 'Absent'
                attendance.save()
                messages.success(request, 'Attendance marked successfully!')
                return redirect('class_list')  # Or whichever view makes sense
            else:
                messages.error(request, 'There was an error marking attendance. Please try again.')
                return render(request, 'attendance/mark.html', {'form': form, 'attendance': attendance})

        else:
            form = AttendanceForm()  # Display empty form if it's GET request

        return render(request, 'attendance/mark.html', {'form': form, 'attendance': attendance})

    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('student_list')  # Adjust as needed
    except Class.DoesNotExist:
        messages.error(request, "Class not found.")
        return redirect('class_list')  # Adjust as needed
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('class_list')  # Adjust as needed



@login_required(login_url='login')
def home(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]  # Show last 5 notifications
    
    context = {
        'user': user,
        'notifications': notifications,
        'total_notifications': notifications.count(),
    }

    return render(request, 'home.html', context)


# Use the login_required decorator for views that require login
@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    
    # Handle form submission for adding a new student
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # After saving, redirect to the same page to refresh the student list
    else:
        form = StudentForm()

    # Render the student list along with the form
    return render(request, 'samsapp/student_list.html', {'students': students, 'form': form})

@login_required(login_url='login')
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_create')  # After saving, redirect to student list
    else:
        form = StudentForm()

    # Render the student list along with the form
    return render(request, 'samsapp/student_list.html', {'form': form})


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

# @login_required(login_url='login')
# def student_delete(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method == "POST":
#         student.delete()
#         messages.success(request, 'Student deleted successfully.')
#         return redirect('student_list')
#     return render(request, 'samsapp/student_list.html')

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
        student = get_object_or_404(Student, pk=pk)

        # Create a response object for PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_report_{student.student_id}.pdf"'

        # Create a PDF document with the given filename
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Create data for the table (headers and student info)
        data = [
            ['Student ID', 'Name', 'Email', 'Birth Date', 'Enrollment Date'],
            [
                student.student_id,
                student.student_fullname or '',
                student.student_email or '',
                student.birth_date or '',
                student.enrollment_date or ''
            ]
        ]

        # Create a table with the data
        table = Table(data)

        # Apply some styling to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body row background
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add gridlines
        ])
        
        # Apply style to the table
        table.setStyle(style)

        # Build the PDF document with the table
        elements = [table]
        doc.build(elements)

        return response

    except Exception as e:
        print(f"Error generating report: {e}")
        return HttpResponse("Error generating report.", status=500)

# @login_required(login_url='login')

# def student_report(request, pk):
#     try:
#         student = get_object_or_404(Student, pk=pk)
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="student_report_{student.student_id}.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Student ID', 'Name', 'Email', 'Birth Date', 'Enrollment Date'])

#         writer.writerow([
#             student.student_id,
#             student.student_fullname or '',
#             student.student_email or '',
#             student.birth_date or '',
#             student.enrollment_date or ''
#         ])

#         return response
#     except Exception as e:
#         print(f"Error generating report: {e}")
#         return HttpResponse("Error generating report.", status=500)
    
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
@login_required(login_url='login')
def user_list(request):
    if request.user.is_staff:
        users = User.objects.all()
    else:
        users = User.objects.values('username', 'email')  # Only expose username and email
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
                    next_url = 'class_list'  # Ensure this view is defined in your urlpatterns
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'samsapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def manage_notifications(request):
    # Fetch all notifications ordered by creation time
    notifications = Notification.objects.all().order_by('-created_at')

    # Count unread notifications for the badge
    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'samsapp/manage_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required(login_url='login')
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return redirect('manage_notifications')

@login_required(login_url='login')
def class_list(request):
    classes = Class.objects.all()
    unread_count = Notification.objects.filter(is_read=False).count()
    return render(request, 'samsapp/class_list.html', {'classes': classes, 'unread_count': unread_count})


def password_recovery(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "password_recovery.html")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "password_recovery.html")

        try:
            user = User.objects.get(username=username, email=email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password successfully reset. You can now log in.")
            return HttpResponseRedirect(reverse("login"))
        except User.DoesNotExist:
            messages.error(request, "User with the provided username and email does not exist.")
            return render(request, "password_recovery.html")

    return render(request, "samsapp/password_recovery.html")



