import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EmployeeSignupForm, EmployeeLoginForm, UploadFileForm
from .models import Task
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import UserProfileForm

from .models import Task, Employee, UploadedFile, Organization
from .tasks import long_running_task
from .chat import *
import os

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
                org_name = Organization.objects.filter(name=username.split('@')[1].split('.')[0]).first().name
                index_status = create_pinecone_index(org_name)
                if index_status:
                    print("index with name ",org_name," created successfully")
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
        if request.user.is_authenticated:
            return redirect('Employee:dashboard')
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
    files = UploadedFile.objects.filter(organization=request.user.employee.organization)
    return render(request, 'Employee/train.html', {'form': form, 'files': files,'organization': request.user.employee.organization.name})


def logout_view(request):
    logout(request)
    return redirect('main:home')


def tasklist_view(request):
    employee = request.user.employee
    organization = employee.organization
    tasks = Task.objects.filter(organization=organization)
    return render(request, 'Employee/tasklist.html',
                  {'tasks': tasks, 'employee': employee, 'organization': organization})


def dashboard_view(request):
    return render(request, 'Employee/dashboard.html')


def profile_view(request, domain_name):
    organization = get_object_or_404(Organization, domain_name=domain_name)

    context = {

        'organization': organization,
    }
    return render(request, 'Employee/profile.html', context)


def edit_profile(request, domain_name):
    organization = get_object_or_404(Organization, domain_name=domain_name)
    print(organization.name)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=organization)
        if form.is_valid():
            organization.save()
            form.save()
            return redirect('Employee:profile', domain_name=organization.domain_name)
    else:
        form = UserProfileForm(instance=organization)

    return render(request, 'Employee/edit_profile.html', {'form': form, 'organization': organization})


def organization_delete(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if request.method == 'POST':
        organization.delete()
        return redirect('organization_list')
    return render(request, 'Employee/delete.html', {'organization': organization})


def fillIndex_view(request):
    user = request.user
    print(user)
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        print('here')
        messages.error(request, "Employee profile not found.")
        return redirect('Employee:train')  # Redirect to an appropriate page if the employee profile is not found

    company_name = Employee.objects.get(user=user).organization.name
    print(company_name)
    index_status = create_pinecone_index(company_name)
    if not index_status:
        files = UploadedFile.objects.filter(organization=Organization.objects.get(name=company_name))
        file_paths = []
        for file in files:
            if not file.trained:
                file_paths.append(os.path.splitext(os.path.basename(file.file.name))[0])
                file.trained = True
                file.save()
        print(file_paths)
        documents = load_documents(company_name,file_paths)
        # print(documents)
        fill_pinecone_index(company_name, documents)

    return redirect('Employee:train')


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
