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
        'olx': 'css-1wxaaza'
    }    
    site_classes_of_price = {        
        'prom': 'bkjEo',    
        'allo': 'v-pb__cur',
        'olx': 'css-13afqrm'
    }
    site_classes_of_url = {        
        'prom': '_0cNvO jwtUM',        
        'allo': 'product-card__title',
        'olx': 'css-z3gu2d'
    }

    def __init__(self, site, product):
        self.site = site
        self.product = product
        self.data = {name : {'names': [], 'prices': [], 'urls': []} for name in site}       
        self._url = {name: self.urls[name] + self.__get_full_url(name) for name in site}               
        
    def scrape_data(self, site_name, soup):
        name_elements = soup.find_all(class_ = self.site_classes_of_names[site_name])
        self.data[site_name]['names'] = [name.text + f'in the - {site_name}' for name in name_elements]        
        
        price_elements = soup.find_all(class_= self.site_classes_of_price[site_name], attrs={"data-qaid": "product_price"} if site_name == 'prom' else None)
        self.data[site_name]['prices'] = [price.text for price in price_elements]        
        
        url_elements = soup.find_all('a', class_ = self.site_classes_of_url[site_name], target='_self' if site_name == 'prom' else None) # target tag 
        self.data[site_name]['urls'] = [self.urls[site_name] + url['href'] for url in url_elements]

    def __get_full_url(self, name):
        search_term = self.product.replace(' ', '%20')
        if name == 'prom':
            return f'ua/search?search_term={search_term}'
        elif name == 'allo':
            return f'/ua/catalogsearch/result/?q={search_term}'
        elif name == 'olx':
            return f'uk/q-{self.product.replace(" ", "-")}/'      
                           
    def make_request(self):        
        for site_name in self._url:  
            html = requests.get(self._url[site_name])
            html = requests.get(html.url)
            soup = BeautifulSoup(html.text, "html.parser")               
            self.scrape_data(site_name, soup)
        
