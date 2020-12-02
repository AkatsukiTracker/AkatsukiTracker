import requests
from bs4 import BeautifulSoup

def string_to_number(string): #no la mejor funcion, pero weno
    n = ""
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    for i in string:
        if i in numbers:
            n += i
    return int(n)

def seleccionar_scraper(url_tienda, link):
    tiendas = [ #formato (url, tienda, scraper_inicial, scraper)
        ("www.falabella.com", "falabella", FalabellaInitialScraper(link), FalabellaScraper(link)),
        ("www.lider.cl", "lider", LiderInitialScraper(link), "algo"),
    ]
    for i in tiendas:
        if i[0] == url_tienda:
            return i

def tiendaDisponible(tienda):
    lista =["www.falabella.com",
            "www.lider.cl",
    ]
    if tienda in lista:
        return True
    return False

class FalabellaInitialScraper():
    tienda = "falabella"
    def __init__(self, link):
        self.link = link
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        codigo = link.split('/')[5]
        self.nombreProducto = link.split('/')[6].replace('-',' ')
        selectText = ("#testId-pod-prices-{} > ol > li").format(codigo)
        data = soup.select(selectText)

        jsx = soup.select(selectText)[0].attrs["class"][0]

        if len(data) == 1:
            path_normal = selectText +" > div > span"
            p_normal = soup.select(path_normal)[0].text         

        elif len(data) == 3:
            path_tarjeta = selectText + "." + jsx + ".price-0 > div > span"
            path_oferta = selectText + "." + jsx + ".price-1 > div > span"
            path_normal = selectText + "." + jsx + ".price-2 > div > span"
            p_tarjeta = soup.select(path_tarjeta)[0].text
            p_oferta = soup.select(path_oferta)[0].text
            p_normal = soup.select(path_normal)[0].text

        elif len(data) == 2:
            try:
                data[-2]["data-internet-price"]
            except:
                path_tarjeta = selectText + "." + jsx + ".price-0 > div > span"
                path_normal = selectText + "." + jsx + ".price-1 > div > span"
                p_tarjeta = soup.select(path_tarjeta)[0].text
                p_normal = soup.select(path_normal)[0].text
            else:
                path_oferta = selectText + "." + jsx + ".price-0 > div > span"
                path_normal = selectText + "." + jsx + ".price-1 > div > span"
                p_oferta = soup.select(path_oferta)[0].text
                p_normal = soup.select(path_normal)[0].text
  
        try:
            self.p_normal = string_to_number(p_normal)
            self.path_normal = path_normal
        except:
            pass
        else:
            try:
                self.p_tarjeta = string_to_number(p_tarjeta)
                self.path_tarjeta = path_tarjeta
            except:
                pass
            try:
                self.p_oferta = string_to_number(p_oferta)
                self.path_oferta = path_oferta
            except:
                pass          
        
        self.img_link = ("https://falabella.scene7.com/is/image/Falabella/{}_1?wid=800&hei=800&qlt=70").format(codigo)
        

    def get_link(self):
        return self.link
    
    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        try:
            precios["precio_oferta_internet"] = self.p_oferta
        except:
            pass
        try:
            precios["precio_oferta_tarjeta"] = self.p_tarjeta
        except:
            pass
        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        try:
            paths["precio_oferta_internet"] = self.path_oferta
        except:
            pass
        try:
            paths["precio_oferta_tarjeta"] = self.path_tarjeta
        except:
            pass
        return paths

    def get_img(self):
        return self.img_link

class FalabellaScraper():

    def __init__(self, link, path):
        soup = BeautifulSoup(requests.get(link).content, features="html.parser") 
        self.status = 0
        try:
            self.precio = string_to_number(soup.select(path)[0].text)
        except:
            codigo = self.link.split('/')[5]
            selectText = ("#testId-pod-prices-{} > ol > li").format(codigo)
            jsx = soup.select(selectText)[0].attrs["class"][0]

            self.path = selectText + "." + jsx + path[-21:]
            try:
                self.precio = string_to_number(soup.select(self.path)[0].text)
                self.status = 1
            except:
                self.status = 2
    
    def check_status(self):
        return self.status
        #Status: 0 = OK, 1 = CHANGED PATH, 2 = NO DISPONIBLE

    def get_precio(self):
        return self.precio

    def get_path(self):
        return self.path


class LiderInitialScraper():
    tienda = "paris"
    def __init__(self,link):
        self.link = link
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        if link.split("/")[3] == "catalogo":
            text = soup.find_all("script")[2].string
            self.nombreProducto = text[text.find("name")+4+3:text.find("image")-3]
            self.img_link = text[text.find("image")+5+3:text.find("description")-3]
            precio = text[text.rfind("price")+5+2:len(text)-2]
            self.path = "script-2-[price]"
        elif link.split("/")[3] == "supermercado":
            codigo = link.split("/")[6]
            self.nombreProducto = soup.select("#span-display-name")[0].text +" "+ soup.select("#span-display-name")[0].next_sibling.text
            self.img_link = "https://images.lider.cl/wmtcl?source=url%5Bfile:/productos/{}a.jpg&sink".format(codigo)
            precio = soup.select("#productPrice > p.price")[0].text
            self.path = "#productPrice > p.price"

        self.precio = string_to_number(precio)

    def get_link(self):
        return self.link

    def get_tienda(self):
        return self.tienda

    def get_nombre(self):
        return self.nombreProducto

    def get_img(self):
        return self.img_link

    def get_precios(self):
        return {"precio_más_bajo":self.precio}

    def get_paths(self):
        return {"precio_más_bajo":self.path}
