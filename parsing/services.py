from bs4 import BeautifulSoup
import requests

class Parse():
    urls = {
        'allo':'https://allo.ua/', 
        'olx':'https://www.olx.ua/',
        'prom':'https://prom.ua/' 
    }
    site_classes_of_names = {        
        'prom': 'M3v0L BXDW- sMgZR',        
        'allo': 'product-card__title',
        'olx': 'css-16v5mdi er34gjf0'
    }    
    site_classes_of_price = {        
        'prom': 'bkjEo',        
        'allo': 'v-pb__cur',
        'olx': 'css-10b0gli er34gjf0'
    }
    site_classes_of_url = {        
        'prom': '_0cNvO jwtUM',        
        'allo': 'product-card__title',
        'olx': 'css-rc5s2u'
    }

    def __init__(self, site, product):
        self.site = site
        self.product = product
        self.cleaned_data_name = []
        self.cleaned_data_price = []
        self.cleaned_data_url = []
        self.product_data = []                   
        self.url = {name: self.urls[name] + self.get_full_url(name) for name in site}               
        
    def get_full_url(self, name):
        if name == 'prom':
            return ('ua/search?search_term=' + self.product).replace(' ', '%20')
        elif name == 'allo':
            return ('/ua/catalogsearch/result/?q=' + self.product).replace(' ', '%20')
        elif name == 'olx':
            return ('uk/q-' + self.product + '/').replace(' ', '-')
    
    def take_price(self, site_name, soup):        
        self.product_data = soup.find_all(class_ = self.site_classes_of_price[site_name])
        for data in self.product_data:
            self.cleaned_data_price.append(data.text)     

    def take_name(self, site_name, soup):
        self.product_data = soup.find_all(class_ = self.site_classes_of_names[site_name])         
        for data in self.product_data:            
            self.cleaned_data_name.append(data.text + ' in the store - ' + site_name)          
    
    def take_product_url(self, site_name, soup):
        if site_name == 'prom': # only for Prom site due to difference   
            self.product_data = soup.find_all('a', class_ = self.site_classes_of_url[site_name], target='_self') 
        else: 
            self.product_data = soup.find_all('a', class_ = self.site_classes_of_url[site_name])    

        for data in self.product_data:                    
            self.cleaned_data_url.append(self.urls[site_name] + data['href'])
                           
    def make_request(self):        
        for site_name in self.url:            
            html = requests.get(self.url[site_name])
            html = requests.get(html.url)
            soup = BeautifulSoup(html.text, "html.parser")                
            self.take_name(site_name, soup)
            self.take_price(site_name, soup)
            self.take_product_url(site_name, soup)
        
