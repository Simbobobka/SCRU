from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parsing.urls')),    
    path('', include('user_management.urls')),    
    path('account/', include('django.contrib.auth.urls')),    
]
