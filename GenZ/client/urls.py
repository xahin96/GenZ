from django.urls import path, include

from . views import *

urlpatterns = [
    path("",index,name="home"),
    path("submit",submit,name="submit"),
    path("<int:content_id>/",content,name="content"),
    path("<int:content_id>/submit", question, name="question"),
]
