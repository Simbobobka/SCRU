from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
import requests
from .forms import SearchForm
from .services import Parse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import SavedGoods
from django.contrib.auth.decorators import login_required



@api_view(['GET'])
def index(request): 
    return render(request, 'index.html') 

@api_view(['POST', 'GET'])
def parse(request):     
    if request.method == 'POST': 
        form = SearchForm(request.POST)        
        if form.is_valid():               
            parse = Parse(form.cleaned_data.get('site'), form.cleaned_data['product'])                  
            parse.make_request()  
            context = zip(parse.cleaned_data_name, parse.cleaned_data_price, parse.cleaned_data_url)                         
            return render(request, 'home.html', {"product" : context})        

    elif request.method == 'GET':
        form = SearchForm()
        return render(request, 'parse.html', {'form':form})

@login_required()
def save_good(request):    
    if request.method == 'POST':        
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        url = request.POST.get('product_url')
        
        SavedGoods.objects.create(user=request.user, title=name, price=price, url=url)
        
        return redirect('home')
    return redirect('home')
 