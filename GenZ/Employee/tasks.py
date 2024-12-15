# Employee/tasks.py

from celery import shared_task
from django.conf import settings
from .models import Task,UploadedFile, Organization
import time
from .chat import *
import time
import uuid

import openai
import openai.embeddings_utils
import pinecone
from dotenv import load_dotenv
import logging
from PyPDF2 import PdfReader
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from django.conf import settings
media_path = settings.MEDIA_ROOT
pc = Pinecone(api_key='cbce143e-7f60-4ba2-8b50-cb10eb3004a8')
load_dotenv()

openai.api_key = "sk-proj-1yFkH3wOlBhkDY7xwWyyT3BlbkFJXoUpo2iJQbJplPN8665L"

@shared_task
def long_running_task(task_title, organization_id, employee_id):
    from django.db import connection
    connection.ensure_connection()
    task_obj = Task.objects.create(
        task_title=task_title,
        organization_id=organization_id,
        employee_id=employee_id,
    )
    time.sleep(10)  # Simulating a long-running task
    print('ok2')
    Task.objects.filter(id=task_obj.id).update(
        task_status='COMPLETED'
    )
    return "Task completed"

@shared_task
def train_task(task_title, organization_id, employee_id, company_name):
    from django.db import connection
    connection.ensure_connection()
    task_obj = Task.objects.create(
        task_title=task_title,
        organization_id=organization_id,
        employee_id=employee_id,
    )
    # time.sleep(10)  # Simulating a long-running task
    files = UploadedFile.objects.filter(organization=Organization.objects.get(name=company_name))
    file_paths = []
    for file in files:
        if not file.trained:
            file_paths.append(os.path.splitext(os.path.basename(file.file.name))[0])
            file.trained = True
            file.save()
    print(file_paths)
    documents = load_documents(company_name, file_paths)
    fill_pinecone_index(company_name, documents)
    print('ok2')
    Task.objects.filter(id=task_obj.id).update(
        task_status='COMPLETED'
    )
    return "Task completed"


@shared_task
def untrain_task(task_title, organization_id, employee_id, company_name):
    from django.db import connection
    connection.ensure_connection()
    task_obj = Task.objects.create(
        task_title=task_title,
        organization_id=organization_id,
        employee_id=employee_id,
    )
    # time.sleep(10)  # Simulating a long-running task
    clear_index(company_name)
    files = UploadedFile.objects.filter(organization=Organization.objects.get(name=company_name))
    for file in files:
        if file.trained:
            file.trained = False
            file.save()
    print('ok2')
    Task.objects.filter(id=task_obj.id).update(
        task_status='COMPLETED'
    )
    return "Task completed"