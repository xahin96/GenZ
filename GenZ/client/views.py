from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *


# Create your views here.
def index(request):
    contents = Content.objects.all().order_by('-pk')
    return render(request, 'index.html', {'contents': contents})


def submit(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        data = Content.objects.create(content=content)
        data.save()
        question = Question.objects.create(question=content,content=data)
        question.save()
        return redirect('/client/' + str(data.id))
    # contents = Content.objects.all().order_by('-pk')
    # #return render(request, 'index.html', {'contents': contents})

def question(request,content_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        question = Question.objects.create(question=content, content=Content.objects.get(pk=content_id))
        question.save()
        contents = Content.objects.all().order_by('-pk')
        questions = Question.objects.filter(content=content_id).order_by('-pk')
        return render(request, 'index.html', {'contents': contents, 'questions': questions, 'content_id': content_id})


def content(request,content_id):
    contents = Content.objects.all().order_by('-pk')
    questions = Question.objects.filter(content=content_id).order_by('-pk')
    return render(request,'index.html',{'contents':contents,'questions':questions,'content_id':content_id})
