import requests
from bs4 import BeautifulSoup

def string_to_number(string): #no la mejor funcion, pero weno
    n = ""
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    for i in string:
        if i in numbers:
            n += i
    return int(n)

def seleccionar_scraper_initial(tienda, link):
    if tienda == "www.falabella.com":
        scraper = FalabellaInitialScraper(link)            
        tienda = "falabella"

    elif tienda == "www.abcdin.cl":
        scraper = AbcdinInitialScraper(link)
        tienda = "abcdin"

    elif tienda == "simple.ripley.cl":
        scraper = RipleyInitialScraper(link)
        tienda = "ripley"

    elif tienda == "www.paris.cl":
        scraper = ParisInitialScraper(link)
        tienda = "paris"

    elif tienda == "www.pcfactory.cl":
        scraper = PCFactoryInitialScraper(link)
        tienda = "pcfactory"

    elif tienda == "www.antartica.cl":
        scraper = AntarticaInitialScraper(link)
        tienda = "antartica"

    elif tienda == "www.cruzverde.cl":
        scraper = CruzVerdeInitialScraper(link)
        tienda = "cruzverde"

    elif tienda == "www.sparta.cl":
        scraper = SpartaInitialScraper(link)
        tienda = "sparta"

    return (tienda, scraper)
            

def tiendaDisponible(tienda):
    lista =["www.falabella.com",
            "www.abcdin.cl",
            "simple.ripley.cl",
            "www.paris.cl",
            "www.pcfactory.cl",
            "www.antartica.cl",
            "www.cruzverde.cl",
            "www.sparta.cl",
            "www.lider.cl",
    ]
    if tienda in lista:
        return True
    return False

#Scrapers

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
        
class AbcdinInitialScraper():
    tienda = "abcdin"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.img_link = "https://www.abcdin.cl" + soup.select("div.image_container > span > img#productMainImage")[0].attrs["src"]
        self.nombreProducto = str(soup.select("div#customKitFullWidthSlot56")[0].text).strip().split('\t')[0].split('\n')[0]

        disponibilidad = str(soup.select("div#productPageShoppingCart")[0].text).strip()
        if disponibilidad != "Producto Agotado":
          disponibilidad = "Producto Disponible"

        # Oferta = Internet, Tarjeta = Abcvisa
        path_oferta = "div.internetPrice > div > span"
        path_normal = "div.normalPrice > div"
        path_tarjeta = "div.detailContainer > div > div > div"

        precio_oferta = soup.select(path_oferta)[1].text.strip()
        precio_normal = soup.select(path_normal)[0].text.strip()

        try:
          precio_tarjeta = soup.select(path_tarjeta)[5].text.strip()
          self.p_tarjeta = string_to_number(precio_tarjeta)
        except:
          precio_tarjeta = 'Oferta no disponible'
          self.p_tarjeta = precio_tarjeta

        self.p_oferta = string_to_number(precio_oferta)
        self.p_normal = string_to_number(precio_normal)

        self.path_oferta = path_oferta
        self.path_normal = path_normal
        self.path_tarjeta = path_tarjeta

    def get_link(self):
        return self.link

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        try:
            paths["precio_oferta_tarjeta"] = self.path_tarjeta
        except:
            pass
        return paths

    def get_img(self):
        return self.img_link

class RipleyInitialScraper():
    tienda = "ripley"
    def __init__(self,link):
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      path = ".product-info > ul > li > span"
      section = soup.select(path)
      descuento = "No hay descuentos"
      precios = []

      self.nombreProducto = soup.select("section.product-header.visible-xs > h1")[0].text
      self.img_link = 'https:' + soup.select("div.item > img")[0].attrs["data-src"]

      precio_normal = ''
      precio_internet = 'Oferta no disponible'
      precio_ripley = 'Oferta no disponible'

      i = 0
      while i < len(section):
        pago = soup.select(path)[i].text
        precio = soup.select(path)[i+1].text
        precios.append((pago,precio))
        i += 2

      for par in precios:
        pago,precio = par
        if pago == "Normal":
          precio_normal = precio.strip()
        elif pago == "Internet":
          precio_internet = precio.strip()
        elif pago == "Tarjeta Ripley o Chek":
          precio_ripley = precio.strip()
        elif pago == "Descuento":
          descuento = precio.strip()

      if precio_normal == '' and precio_internet != 'Oferta no disponible':
        precio_normal = precio_internet
        precio_internet = 'Oferta no disponible'

      self.p_normal = precio_normal
      self.p_oferta = precio_internet
      self.p_tarjeta = precio_ripley
      self.path = path


    def get_link(self):
        return self.link

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = (self.path,1)
        paths["precio_oferta_internet"] = (self.path,3)
        paths["precio_oferta_tarjeta"] = (self.path,5)
        return paths

    def get_img(self):
        return self.img_link

class ParisInitialScraper():
    tienda = "paris"
    def __init__(self,link):
      fuente = requests.get(url).text
      soup = BeautifulSoup(fuente,features="html.parser")

      nombre_prod = soup.select("h1")[0].text.strip().split('\n')[2]

      img = soup.select("div.product-image-wrapper.sticky#pdp-image-wrapper > a")[0].attrs["href"]

      precio_normal = ''
      precio_internet = 'Oferta no disponible'
      precio_cencosud = 'Oferta no disponible'

      path = ".item-price"
      cant_precios = len(soup.select(path))

      #Casos posibles
      self.caso1 = False
      self.caso2 = False
      self.caso3 = False
      self.caso4 = False

      #Caso 1, un único precio
      if cant_precios == 1:
        precio_normal = soup.select(path)[0].text.strip()
        self.path_normal = path
        self.caso1 = True
        self.p_normal = precio_normal

      #Dos precios
      elif cant_precios == 2:
        #Opción 1: Oferta Internet/Temporal y Precio Normal (Caso 2)
        try:
          precio_normal = soup.select(path + ".price-normal > span")[0].text
          precio_internet = soup.select(path)[0].text.strip().split('\n')[0]

          self.path_normal = path + ".price-normal > span"
          self.path_oferta = path
          self.caso2 = True
          self.p_normal = precio_normal
          self.p_oferta = precio_internet

        #Opción 2: Oferta Cencosud y Precio Normal (Caso 3)
        except:
          precio_cencosud = soup.select(path + ".offer-price.price-tc.cencosud-price-2")[0].text.strip().split('\n')[0]
          precio_normal = soup.select(path + "> div > span")[0].text

          self.path_tarjeta = path + ".offer-price.price-tc.cencosud-price-2"
          self.path_normal = path + "> div > span"
          self.caso3 = True
          self.p_tarjeta = precio_cencosud
          self.p_normal = precio_normal

      #Caso 4, tres precios
      elif cant_precios == 3:
        precio_internet = soup.select(path + "> div > span")[0].text
        precio_normal = soup.select(path + ".price-normal > span")[0].text
        precio_cencosud = soup.select(path + ".offer-price.price-tc.cencosud-price-2")[0].text.strip().split('\n')[0]

        self.path_oferta = path + "> div > span"
        self.path_normal = path + ".price-normal > span"
        self.path_tarjeta = path + ".offer-price.price-tc.cencosud-price-2"
        self.caso4 = True
        self.p_oferta = precio_internet
        self.p_normal = precio_normal
        self.p_tarjeta = precio_cencosud

    def get_link(self):
      return self.link

    def get_precios(self):
        precios = dict()

        if self.caso4:
          precios["precio_normal"] = self.p_normal
          precios["precio_oferta_internet"] = self.p_oferta
          precios["precio_oferta_tarjeta"] = self.p_tarjeta

        elif self.caso3:
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
          precios["precio_normal"] = self.p_normal

        elif self.caso2:
          precios["precio_normal"] = self.p_normal
          precios["precio_oferta_internet"] = self.p_oferta

        else:
           precios["precio_normal"] = self.p_normal

        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        if self.caso4:
          paths["precio_normal"] = self.path_normal
          paths["precio_oferta_internet"] = self.path_oferta
          paths["precio_oferta_tarjeta"] = self.path_tarjeta

        elif self.caso3:
          paths["precio_oferta_tarjeta"] = self.path_tarjeta
          paths["precio_normal"] = self.path_normal

        elif self.caso2:
          paths["precio_normal"] = self.path_normal
          paths["precio_oferta_internet"] = self.path_oferta

        else:
           paths["precio_normal"] = self.path_normal

        return paths

    def get_img(self):
        return self.img_link

class PCFactoryInitialScraper():
    tienda = "pcfactory"
    def __init__(self,link):
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("div.ficha_titulos > h1 > span")[0].text + ' ' + soup.select("div.ficha_titulos > h1 > span")[1].text
      self.img_link = "https://www.pcfactory.cl" + soup.select("li > img")[3].attrs["src"]

      path = "div.ficha_producto_precio_wrap > div > h2"
      cant_precios = len(soup.select(path))

      if cant_precios == 2:
        precio_efectivo = soup.select(path)[0].text.strip().replace(' ','')
        precio_normal = soup.select(path)[1].text.strip().replace(' ','')

      else:
        precio_efectivo = soup.select(path)[0].text.strip().replace(' ','')
        precio_internet = soup.select(path)[1].text.strip().replace(' ','')
        precio_normal = soup.select(path)[2].text.strip().replace(' ','')
        self.p_internet = precio_internet

      self.p_efectivo = precio_efectivo
      self.p_normal = precio_normal
      self.path = path

    def get_link(self):
      return self.link

    def get_precios(self):
        precios = dict()
        precios["precio_efectivo"] = self.p_efectivo
        precios["precio_normal"] = self.p_normal
        try:
          precios["precio_internet"] = self.p_internet
        except:
          pass
        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        paths["unico_path"] = self.path
        return paths

    def get_img(self):
        return self.img_link

class AntarticaInitialScraper():
    tienda = "antartica"
    def __init__(self,link):
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("span.txtTitulosRutaSeccionLibros")[0].text
      id = soup.select("span.txt")[1].text.split(' ')[1]
      self.img_link = "https://www.antartica.cl/antartica/gfx_libros/144/" + id + ".jpg"

      path_club = "div.precioClubfichaV"
      path_internet = "div.precioAhoraFicha"
      path_normal = "div.precioAntes"

      try:
        precio_club = soup.select(path_club)[0].text.strip().replace(',','.')
      except:
        precio_club = "Oferta no disponible"

      precio_internet = soup.select(path_internet)[0].text.split(' ')[1]
      precio_normal = soup.select(path_normal)[0].text.split(' ')[1]

      self.p_oferta = precio_internet
      self.p_normal = precio_normal
      self.p_club = precio_club

      self.path_club = path_club
      self.path_oferta = path_internet
      self.path_normal = path_normal

    def get_link(self):
        return self.link

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        if self.p_club != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_club
        return precios

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        if self.p_club != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_club
        return paths

    def get_img(self):
        return self.img_link

