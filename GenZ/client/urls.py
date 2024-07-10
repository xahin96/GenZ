from django.urls import path, include

from . views import *
app_name = 'client'

urlpatterns = [
    path("<str:company_name>/",index,name="home"),
    path("<str:company_name>/submit",submit,name="submit"),
    path("<str:company_name>/<int:content_id>/",content,name="content"),
    path("<str:company_name>/<int:content_id>/submit", question, name="question"),
]
