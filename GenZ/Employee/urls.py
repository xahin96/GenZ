from django.urls import path
from .views import *

app_name = 'Employee'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('tasklist/', tasklist_view, name='tasklist'),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("train/", train_view, name="train"),
    path('profile/<str:domain_name>/', profile_view, name='profile'),
    path('profile/<str:domain_name>/edit/', edit_profile, name='edit_profile'),
    path("fillIndex/",fillIndex_view,name="fillIndex"),
    path('test-view/', test_view, name='test_view'),
]
