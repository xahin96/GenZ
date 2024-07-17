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
    path("fillIndex/",fillIndex_view,name="fillIndex"),
]
