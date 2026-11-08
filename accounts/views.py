# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

def student_login(request):
    if request.user.is_authenticated:
        return redirect('exams_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('exams_dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/student_login.html')

def student_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('student_login')

@staff_member_required
def create_user_account(request):
    """Staff-only view to quickly register new student or teacher accounts."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_staff = request.POST.get('is_staff') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already in use.")
        else:
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff
            )
            role = "Staff" if is_staff else "Student"
            messages.success(request, f"{role} account for '{username}' created successfully.")
            return redirect('central_dashboard')

    return render(request, 'accounts/create_user.html')