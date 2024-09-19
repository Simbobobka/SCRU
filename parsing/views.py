from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .services import Parse
from .models import SavedGoods
import time
def index(request): 
    return render(request, 'index.html') 
#prom 2.2923262119293213 seconds
#allo 4.25605320930481 seconds
#olx 3.3420932292938232 seconds


def parse(request):     
    if request.method == 'POST': 
        form = SearchForm(request.POST)        
        if form.is_valid():               
            parse = Parse(form.cleaned_data.get('site'), form.cleaned_data['product'])    
            start_time = time.time()              
            parse.make_request()  
            print(f"Done in {time.time() - start_time} seconds")
            context = []        
            for site in form.cleaned_data.get('site'):
                context.extend(zip(
                    parse.data[site]['names'], 
                    parse.data[site]['prices'], 
                    parse.data[site]['urls'],
                    parse.data[site]['images']
                ))            
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
        
        return redirect('saved')    

@login_required()
def saved_good(request):
    if request.method == 'GET':
        saved = SavedGoods.objects.filter(user = request.user)
        return render(request, 'saved.html', {"context":saved})
    elif request.method == 'POST':
        saved = SavedGoods.objects.filter(user = request.user, id = request.POST.get('product_id')) 
        if saved.exists():
            saved.delete()
        saved = SavedGoods.objects.filter(user = request.user) 
        return render(request, 'saved.html', {"context":saved})
    

