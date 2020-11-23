import requests
from bs4 import BeautifulSoup

class FalabellaScraper():
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

        p_tarjeta = "sin ofertas de tarjeta"
        p_oferta = "sin ofertas"
        p_normal = "si vé esto, algo salió mal"

        jsx = soup.select(selectText)[0].attrs["class"][0]

        if len(data) == 1:
            p_normal = soup.select(selectText +" > div > span")[0].text

        elif len(data) == 3:
            p_tarjeta = soup.select(selectText + "." + jsx + ".price-0 > div > span")[0].text
            p_oferta = soup.select(selectText + "." + jsx + ".price-1 > div > span")[0].text
            p_normal = soup.select(selectText + "." + jsx + ".price-2 > div > span")[0].text

        elif len(data) == 2:
            try:
                data[-2]["data-internet-price"]
            except:
                p_tarjeta = soup.select(selectText + "." + jsx + ".price-0 > div > span")[0].text
                p_normal = soup.select(selectText + "." + jsx + ".price-1 > div > span")[0].text
            else:
                p_tarjeta = soup.select(selectText + "." + jsx + ".price-0 > div > span")[0].text
                p_normal = soup.select(selectText + "." + jsx + ".price-1 > div > span")[0].text
  

        self.p_tarjeta = p_tarjeta
        self.p_oferta = p_oferta
        self.p_normal = p_normal


    def get_link(self):
        return self.link
    
    def get_precios(self):
        return [self.p_tarjeta, self.p_oferta, self.p_normal]

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda




                    




