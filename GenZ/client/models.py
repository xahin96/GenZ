from django.db import models
from django.utils import timezone


# Create your models here.
class Content(models.Model):
    content = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True,default=timezone.now)

    def __str__(self):
        return self.content
class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True,default=timezone.now)
    content = models.ForeignKey(Content, null=True, blank=True,  on_delete=models.CASCADE, related_name='questions')
    answer = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.question


