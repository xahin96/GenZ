from django.urls import path
from .views import signup_view, login_view

app_name='Employee'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]