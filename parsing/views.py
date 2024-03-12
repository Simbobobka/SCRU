from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import requests
import re
from .forms import SearchForm
from rest_framework.response import Response
from rest_framework import status
from .services import Parse

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
        return render(request, 'parse.html', {"product" : context, 'form':form})        

    elif request.method == 'GET':
        form = SearchForm()
        return render(request, 'parse.html', {'form':form})