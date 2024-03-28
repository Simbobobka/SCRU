from django.urls import path 
from parsing.views import index 
from . import views

urlpatterns = [
    path('home', index , name='home'),
    path('sign-up', views.sign_up , name='sign_up'),    
]