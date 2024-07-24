from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EmployeeSignupForm, EmployeeLoginForm, UploadFileForm
from .models import Task
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import UserProfileForm


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
    if request.user.is_authenticated:
        return redirect('Employee:dashboard')

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

    return render(request, 'Employee/train.html', {'form': form})


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

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=organization)
        if form.is_valid():
            organization.save()
            form.save()
            return redirect('Employee:profile', domain_name=organization.domain_name)
    else:
        form = UserProfileForm(instance=organization)

    return render(request, 'Employee/edit_profile.html', {'form': form})


def organization_delete(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if request.method == 'POST':
        organization.delete()
        return redirect('organization_list')
    return render(request, 'Employee/delete.html', {'organization': organization})
