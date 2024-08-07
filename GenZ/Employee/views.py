import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EmployeeSignupForm, EmployeeLoginForm, UploadFileForm
from .models import Task, Employee, UploadedFile, Organization
from .tasks import long_running_task
from .chat import *


def signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            authenticated_employee = authenticate(request, username=email, password=password)
            if authenticated_employee is not None:
                login(request, authenticated_employee)
                return redirect('Employee:dashboard')
            else:
                error_message = 'Invalid email or password!<br>Please try again!'
                return render(request, 'Employee/login.html', {'form': form, 'error': error_message})
    else:
        form = EmployeeLoginForm()
    return render(request, 'Employee/login.html', {'form': form})


@login_required
def train_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user.employee
            uploaded_file.organization = request.user.employee.organization
            uploaded_file.save()
            return redirect('Employee:train')  # Replace 'profile' with your profile URL name
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.all()
    return render(request, 'Employee/train.html', {'form': form, 'files': files})


def logout_view(request):
    logout(request)
    return redirect('main:home')


def tasklist_view(request):
    employee = request.user.employee
    organization = employee.organization
    tasks = Task.objects.filter(organization=organization)
    return render(request, 'Employee/tasklist.html', {'tasks': tasks, 'employee': employee, 'organization': organization})


def dashboard_view(request):
    return render(request, 'Employee/dashboard.html')


def profile_view(request):
    return render(request, 'Employee/profile.html')


def fillIndex_view(request):
    user = request.user
    company_name = Employee.objects.get(user=user).organization.name
    print(company_name)
    index_status = create_pinecone_index(company_name)
    if index_status:
        UploadedFile.objects.fetch(organization=Organization.objects.get(name=company_name))
        documents = load_documents(company_name)
        print(documents)
        fill_pinecone_index(company_name, documents)

    return redirect('Employee:tasklist')


@login_required
def test_view(request):
    user = request.user
    print(user)
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        print('here')
        messages.error(request, "Employee profile not found.")
        return redirect('Employee:train')  # Redirect to an appropriate page if the employee profile is not found

    organization = employee.organization
    task_title = "Test Task"
    print(employee, organization, task_title)
    long_running_task.delay(task_title, organization.id, employee.user.id)
    print('ok')
    messages.success(request, "Train button clicked and task is running in the background!")
    return redirect('Employee:train')  # Redirect back to the train view or any other appropriate page
