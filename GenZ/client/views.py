from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .chat import get_answer_from_openai


# Create your views here.
def index(request,company_name):
    contents = Content.objects.all().order_by('-pk')
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
    contents = Content.objects.all().order_by('-pk')
    questions = Question.objects.filter(content=content_id).order_by('-pk')
    return render(request,'index.html',{'contents':contents,'questions':questions,'content_id':content_id,'company_name':company_name})
