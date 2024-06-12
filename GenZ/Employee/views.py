from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import EmployeeSignupForm, EmployeeLoginForm


def signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect('Employee:login')
    else:
        form = EmployeeSignupForm()
    return render(request, 'Employee/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                return render(request, 'Employee/login.html', {'form': form})
    else:
        form = EmployeeLoginForm()
        return render(request, 'Employee/login.html', {'form': form})
