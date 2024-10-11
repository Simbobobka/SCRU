import aiohttp
import asyncio
from bs4 import BeautifulSoup


class Parse():

    urls = {
        "allo": "https://allo.ua/",
        "olx": "https://www.olx.ua/",
        "prom": "https://prom.ua/",
    }

    site_classes_of_names = {
        "prom": "M3v0L BXDW- sMgZR",
        "allo": "product-card__title",
        "olx": "css-1wxaaza",
    }

    site_classes_of_price = {
        "prom": "bkjEo", 
        "allo": "v-pb__cur",
        "olx": "css-13afqrm"
    }
    
    site_classes_of_url = {
        "prom": "_0cNvO jwtUM",
        "allo": "product-card__title",
        "olx": "css-1ut25fa",
    }
    
    site_classes_of_images = {
        "prom": "DucV3 _0-uxM Zd5Aq",
        "allo": "is-active",
        "olx": "css-8wsg1m",
    }

    def __init__(self, site: str, product: str): 
        self.site = site
        self.product = product
        self.data = {
            name: {"names": [], "prices": [], "urls": [], "images": []} for name in site
        }
        self._url = {name: self.urls[name] + self.__get_full_url(name) for name in site}

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    def scrape_data(self, site_name, soup):
        name_elements = soup.find_all(class_=self.site_classes_of_names[site_name])
        
        self.data[site_name]["names"] = [
            name.text + f"in the - {site_name}" for name in name_elements
        ]
        price_elements = soup.find_all(
            class_=self.site_classes_of_price[site_name],
            attrs={"data-qaid": "product_price"} if site_name == "prom" else None, #exception
        )
        self.data[site_name]["prices"] = [price.text for price in price_elements]
                
        url_elements = soup.find_all(
            "a",
            class_=self.site_classes_of_url[site_name],
            target="_self" if site_name == "prom" else None, #exception
        )
        self.data[site_name]["urls"] = [
            self.urls[site_name] + url["href"] for url in url_elements
        ]

        picture_elements = soup.find_all(
            "picture", class_=self.site_classes_of_images[site_name]
        )
        for picture in picture_elements:
            self.data[site_name]["images"].append(picture.find("img")["src"])

    def __get_full_url(self, name: str)-> str:   
        search_term = self.product.replace(" ", "%20")
        if name == "prom":
            return f"ua/search?search_term={search_term}"
        elif name == "allo":
            return f"/ua/catalogsearch/result/?q={search_term}"
        elif name == "olx":
            return f'uk/q-{self.product.replace(" ", "-")}/'

    async def fetch_site_data(self, session, site_name):
        html = await self.fetch(session, self._url[site_name])
        soup = BeautifulSoup(html, "html.parser")
        self.scrape_data(site_name, soup)

    async def make_request(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for site_name in self._url:
                tasks.append(self.fetch_site_data(session, site_name))
            await asyncio.gather(*tasks)
