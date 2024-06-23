from django.shortcuts import render
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
    contents = Content.objects.all().order_by('-pk')
    return render(request, 'index.html', {'contents': contents})
