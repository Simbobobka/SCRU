from django.urls import path 
from . import views 

urlpatterns = [
    path('parse', views.parse, name='parse'),    
    path('home', views.index, name='home'),   
    path('save_good/', views.save_good, name='save_good'), 
]