from django.urls import path 
from parsing.views import index 
from . import views

urlpatterns = [
    path('', index , name='home'),
    path('home', index , name='home'),
    path('sign-up', views.sign_up , name='sign_up'),    
]