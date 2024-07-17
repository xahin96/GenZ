# Employee/tasks.py

from celery import shared_task
from django.conf import settings
from .models import Task
import time


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
