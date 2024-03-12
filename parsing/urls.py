from django.urls import path 
from . import views 

urlpatterns = [
    path('parse', views.parse),    
    path('', views.index),    
]