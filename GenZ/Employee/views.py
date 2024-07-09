from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EmployeeSignupForm, EmployeeLoginForm


def signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_employee = authenticate(username=username, password=password)
            if authenticated_employee is not None:
                messages.success(request, 'Account created successfully!<br>Please log in!')
                return redirect('Employee:login')
    else:
        form = EmployeeSignupForm()
    return render(request, 'Employee/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            # email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticated_employee = authenticate(request, username=username, password=password)
            if authenticated_employee is not None:
                login(request, authenticated_employee)
                return redirect('Employee:dashboard')
            else:
                error_message = 'Invalid username or password!<br>Please try again!'
                return render(request, 'Employee/login.html', {'form': form, 'error': error_message})
    else:
        form = EmployeeLoginForm()
    return render(request, 'Employee/login.html', {'form': form})

def dashboard_view(request):
    return render(request, 'Employee/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('main:home')