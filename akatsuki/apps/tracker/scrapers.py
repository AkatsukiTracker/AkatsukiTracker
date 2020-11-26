import requests
from bs4 import BeautifulSoup

class FalabellaInitialScraper():
    tienda = "falabella"
    def __init__(self, link):
        self.link = link
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        codigo = ""
        for i in link[47:]:
            if i == "/":
                break
            codigo += i
        self.nombreProducto = ""
        for i in link[47+len(codigo)+1:]:
            if i == "/":
                break
            elif i == "-":
                self.nombreProducto += " "
            else:
                self.nombreProducto += i   
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
                path_tarjeta = selectText + "." + jsx + ".price-1 > div > span"
                p_oferta = soup.select(path_oferta)[0].text
                p_normal = soup.select(path_tarjeta)[0].text
  
        try:
            self.p_normal = p_normal
            self.path_normal = path_normal
        except:
            pass
        else:
            try:
                self.p_tarjeta = p_tarjeta
                self.path_tarjeta = path_tarjeta
            except:
                pass
            try:
                self.p_oferta = p_oferta
                self.path_oferta = path_oferta
            except:
                pass          


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

class FalabellaScraper():

    def __init__(self, link, path):
        soup = BeautifulSoup(requests.get(link).content, features="html.parser") 
        self.status = 0
        try:
            self.precio = soup.select(path)[0].text
        except:
            codigo = ""
            for i in link[47:]:
                if i == "/":
                    break
                codigo += i
            selectText = ("#testId-pod-prices-{} > ol > li").format(codigo)
            jsx = soup.select(selectText)[0].attrs["class"][0]

            self.path = selectText + "." + jsx + path[-21:]
            self.precio = soup.select(self.path)[0].text
            self.status = 1
    
    def check_status(self):
        return self.status

    def get_precio(self):
        return self.precio

    def get_precio_and_path(self):
        return (self.precio, self.path)
