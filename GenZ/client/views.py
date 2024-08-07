from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from Employee.models import Organization, Employee
from .models import *
from .chat import get_answer_from_openai


# Create your views here.
def index(request,company_name):
    organization = Organization.objects.filter(domain_name=company_name).first()
    employees = Employee.objects.filter(organization=organization)
    users = User.objects.filter(employee__in=employees)
    contents = Content.objects.filter(created_by__in=users).order_by('-pk')
    return render(request, 'index.html', {'contents': contents,'company_name':company_name})


def submit(request,company_name):
    if request.method == 'POST':
        content = request.POST.get('content')
        data = Content.objects.create(content=content)
        data.save()
        ai_answer = get_answer_from_openai(company_name,content)
        question = Question.objects.create(question=content,content=data,answer=ai_answer)
        question.save()
        return redirect('/client/'+company_name+'/' + str(data.id))
    # contents = Content.objects.all().order_by('-pk')
    # #return render(request, 'index.html', {'contents': contents})


def question(request,company_name,content_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        ai_answer = get_answer_from_openai(company_name, content)
        question = Question.objects.create(question=content, content=Content.objects.get(pk=content_id),answer=ai_answer)
        question.save()
        contents = Content.objects.all().order_by('-pk')
        questions = Question.objects.filter(content=content_id).order_by('-pk')
        return render(request, 'index.html', {'contents': contents, 'questions': questions, 'content_id': content_id,'company_name':company_name})


def content(request,company_name,content_id):
    organization = Organization.objects.filter(domain_name=company_name).first()
    employees = Employee.objects.filter(organization=organization)
    users = User.objects.filter(employee__in=employees)
    contents = Content.objects.filter(created_by__in=users).order_by('-pk')
    questions = Question.objects.filter(content_id=content_id, created_by__in=users).order_by('-pk')
    return render(request, 'index.html', {'contents': contents, 'questions': questions, 'content_id': content_id, 'company_name': company_name})
