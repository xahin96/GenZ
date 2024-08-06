from django.shortcuts import render
from Employee.models import *
from client.models import *
from django.utils import timezone


# Create your views here.
def home(request):
    no_of_organization = Organization.objects.count()
    no_of_employee = Employee.objects.count()
    no_of_question = Question.objects.count()
    no_of_task = Task.objects.count()
    updated_on = timezone.now()
    context = {'no_of_organization': no_of_organization,'no_of_employee':no_of_employee,'no_of_questions':no_of_question,'no_of_task':no_of_task,'updated_on':updated_on}
    return render(request, 'main/home.html',context)


