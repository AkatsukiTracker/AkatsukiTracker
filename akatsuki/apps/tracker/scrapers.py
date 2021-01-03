import requests
from bs4 import BeautifulSoup
import json

def string_to_number(string): #no la mejor funcion, pero weno
    n = ""
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    for i in string:
        if i in numbers:
            n += i
    return int(n)

def evaluar_precio(precio):
    if precio == 'Oferta no disponible' or precio == "No disponible":
      return precio
    return string_to_number(precio)

def seleccionar_scraper_initial(tienda, link):
    if tienda == "www.falabella.com":
        scraper = FalabellaInitialScraper(link)
        tienda = "falabella"

    elif tienda == "www.lider.cl":
        scraper = LiderInitialScraper(link)
        tienda = "lider"

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
        tienda = "cruz verde"

    elif tienda == "sparta.cl":
        scraper = SpartaInitialScraper(link)
        tienda = "sparta"

    elif tienda == "www.jumbo.cl":
        scraper = JumboInitialScraper(link)
        tienda = "jumbo"

    elif tienda == "store.steampowered.com":
        scraper = SteamInitialScraper(link)
        tienda = "steam"

    elif tienda == "www.tottus.cl":
        scraper = TottusInitialScraper(link)
        tienda = "tottus"

    elif tienda == "bold.cl":
        scraper = BoldInitialScraper(link)
        tienda = "bold"

    elif tienda == "contrapunto.cl":
        scraper = ContrapuntoInitialScraper(link)
        tienda = "contrapunto"

    elif tienda == "www.chevrolet.cl":
        scraper = ChevroletInitialScraper(link)
        tienda = "chevrolet"

    elif tienda == "articulo.mercadolibre.cl":
        scraper = MercadoLibreScraper(link)
        tienda = "mercado libre"

    elif tienda == "www.subaru.cl":
        scraper = SubaruInitialScraper(link)
        tienda = "subaru"

    elif tienda == "www.linio.cl":
        scraper = LinioInitialScraper(link)
        tienda = "linio"

    elif tienda == "www.sodimac.cl":
        scraper = HomecenterSodimacInitialScraper(link)
        tienda = "homecenter sodimac"

    elif tienda == "www.pethappy.cl":
        scraper = PetHappyInitialScraper(link)
        tienda = "pet happy"

    elif tienda == "www.lacasadelvegan.cl":
        scraper = LaCasaDelVeganInitialScraper(link)
        tienda = "la casa del vegan"

    elif tienda == "www.decathlon.cl":
        scraper = DecathlonInitialScaper(link)
        tienda = "decathlon"

    elif tienda == "www.casamarilla.cl":
        scraper = CasaAmarillaInitialScraper(link)
        tienda = "casa amarilla"

    elif tienda == "www.casaroyal.cl":
        tienda = "casa royal"
        scraper = CasaRoyalInitialScraper(link)

    elif tienda == "feriachilenadellibro.cl":
        tienda = "feria chilena del libro"
        scraper = FeriaChilenaDelLibro(link)

    elif tienda == "www.estacionnatural.cl":
        tienda = "estacion natural"
        scraper = EstacionNaturalInitialScraper(link)

    elif tienda == "www.ortopediaonline.cl":
        tienda = "ortopedia online"
        scraper = OrtopediaOnlineInitialScraper(link)

    elif tienda == "www.suzuki.cl":
        tienda = "suzuki"
        scraper = SuzukiInitialScraper(link)

    return (tienda, scraper)

def seleccionar_scraper(tienda, link, path):

    if tienda == "falabella":
        scraper = FalabellaScraper(link,path)

    elif tienda == "lider":
        scraper = LiderScraper(link,path)

    elif tienda == "jumbo":
        scraper = JumboScraper(link,path)

    else:
        scraper = GeneralScraper(link,path)

    return scraper

def tiendaDisponible(tienda):
    lista =["www.falabella.com",
            "www.lider.cl",
            "www.abcdin.cl",
            "simple.ripley.cl",
            "www.paris.cl",
            "www.pcfactory.cl",
            "www.antartica.cl",
            "www.cruzverde.cl",
            "sparta.cl",
            "www.jumbo.cl",
            "store.steampowered.com",
            "www.tottus.cl",
            "bold.cl",
            "contrapunto.cl",
            "www.chevrolet.cl",
            "articulo.mercadolibre.cl",
            "www.subaru.cl",
            "www.linio.cl",
            "www.sodimac.cl",
            "www.pethappy.cl",
            "www.lacasadelvegan.cl",
            "www.decathlon.cl",
            "www.casamarilla.cl",
            "www.casaroyal.cl",
            "feriachilenadellibro.cl",
            "www.estacionnatural.cl",
            "www.ortopediaonline.cl",
            "www.suzuki.cl"
    ]
    if tienda in lista:
        return True
    return False

#Scrapers

class BaseInitialScraper():
    #getters
    def get_link(self):
        return self.link

    def get_nombre(self):
        return self.nombreProducto

    def get_tienda(self):
        return self.tienda

    def get_img(self):
        return self.img_link

class BaseScraper():
    #getters
    def check_status(self):
        return self.status
        #Status: 0 = OK, 1 = CHANGED PATH, 2 = NO DISPONIBLE

    def get_precio(self):
        return self.precio

    def get_path(self):
        return self.path

class GeneralScraper(BaseScraper):
     def __init__(self,link,path):
        #los headers son necesarios ya que Ortopedia Online los requiere
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        fuente = requests.get(link,headers=headers).text
        soup = BeautifulSoup(fuente,features="html.parser")
        self.status = 0
        self.path = path
        ruta,indice = path.split('/')

        try:
            #el .strip().split('\n')[0] es necesario por Paris, ya que a veces se incluyen los descuentos tipo  '17%', lo cual arruina el resultado esperado de string_to_number()
            self.precio = string_to_number(soup.select(ruta)[int(indice)].text.strip().split('\n')[0])
        except:
            self.status = 2

class FalabellaInitialScraper(BaseInitialScraper):
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

class FalabellaScraper(BaseScraper):
    def __init__(self, link, path):
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        self.status = 0
        try:
            self.precio = string_to_number(soup.select(path)[0].text)
        except:
            codigo = link.split('/')[5]
            selectText = ("#testId-pod-prices-{} > ol > li").format(codigo)
            jsx = soup.select(selectText)[0].attrs["class"][0]

            self.path = selectText + "." + jsx + path[-21:]
            try:
                self.precio = string_to_number(soup.select(self.path)[0].text)
                self.status = 1
            except:
                self.status = 2

class LiderInitialScraper(BaseInitialScraper):
    tienda = "lider"
    def __init__(self,link):
        self.link = link
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        if link.split("/")[3] == "catalogo":
            text = soup.find_all("script")[2].string
            self.nombreProducto = text[text.find("name")+4+3:text.find("image")-3]
            img_link = text[text.find("image")+5+3:text.find("description")-3]
            self.img_link = img_link.split(",")[0].replace('http', 'https')
            precio = text[text.rfind("price")+5+2:len(text)-2]
            self.path = "script-2-[price]"
        elif link.split("/")[3] == "supermercado":
            codigo = link.split("/")[6]
            self.nombreProducto = soup.select("#span-display-name")[0].text +" "+ soup.select("#span-display-name")[0].next_sibling.text
            self.img_link = "https://images.lider.cl/wmtcl?source=url%5Bfile:/productos/{}a.jpg&sink".format(codigo)
            precio = soup.select("#productPrice > p.price")[0].text
            self.path = "#productPrice > p.price"

        self.precio = string_to_number(precio)

    def get_precios(self):
        return {"precio_más_bajo":self.precio}

    def get_paths(self):
        return {"precio_más_bajo":self.path}

class LiderScraper(BaseScraper):
    def __init__(self,link,path):
        self.status = 0
        self.path = path
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        try:
            if link.split("/")[3] == "catalogo":
                text = soup.find_all("script")[2].string
                precio = text[text.rfind("price")+5+2:len(text)-2]
            elif link.split("/")[3] == "supermercado":
                precio = soup.select("#productPrice > p.price")[0].text
            self.precio = string_to_number(precio)
        except:
            self.status = 2

class AbcdinInitialScraper(BaseInitialScraper):
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

        self.path_oferta = path_oferta + '/' + '1'
        self.path_normal = path_normal + '/' + '0'
        self.path_tarjeta = path_tarjeta + '/' + '5'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        if self.p_tarjeta != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        if self.p_tarjeta != 'Oferta no disponible':
            paths["precio_oferta_tarjeta"] = self.path_tarjeta
        return paths

class RipleyInitialScraper(BaseInitialScraper):
    tienda = "ripley"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("section.product-header.visible-xs > h1")[0].text
      self.img_link = 'https:' + soup.select("div.item > img")[0].attrs["data-src"]

      path = "span.product-price"
      cant_precios = len(soup.select(path))

      precio_normal = 'No disponible'
      precio_internet = 'Oferta no disponible'
      precio_ripley = 'Oferta no disponible'

      if cant_precios == 3:
        precio_ripley = soup.select(path)[0].text
        precio_internet = soup.select(path)[1].text
        precio_normal = soup.select(path)[2].text.strip()

        self.path_tarjeta = path + '/' + '0'
        self.path_oferta = path + '/' + '1'
        self.path_normal = path + '/' + '2'

      elif cant_precios == 2:
        #Pueden ser 2 combinaciones: Normal/Internet o Internet/Tarjeta (en ese orden)
        tipo_pago = soup.select("span.product-price-type")[0].text

        if tipo_pago == "Normal":
          precio_internet = soup.select(path)[0].text.strip()
          precio_normal = soup.select(path)[1].text.strip()

          self.path_oferta = path + '/' + '0'
          self.path_normal = path + '/' + '1'

        else:
          precio_internet = soup.select(path)[0].text
          precio_ripley = soup.select(path)[1].text.strip()

          self.path_oferta = path + '/' + '0'
          self.path_tarjeta = path + '/' + '1'
      #Solo está el precio normal
      else:
        precio_normal = soup.select(path)[0].text
        self.path_normal = path + '/' + '0'

      self.p_normal = evaluar_precio(precio_normal)
      self.p_oferta = evaluar_precio(precio_internet)
      self.p_tarjeta = evaluar_precio(precio_ripley)

    def get_precios(self):
        precios = dict()
        if self.p_normal != 'No disponible':
          precios["precio_normal"] = self.p_normal
        if self.p_oferta != 'Oferta no disponible':
          precios["precio_oferta_internet"] = self.p_oferta
        if self.p_tarjeta != 'Oferta no disponible':
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_paths(self):
      paths = dict()
      if self.p_normal != 'No disponible':
        paths["precio_normal"] = self.path_normal
      if self.p_oferta != 'Oferta no disponible':
        paths["precio_oferta_internet"] = self.path_oferta
      if self.p_tarjeta != 'Oferta no disponible':
        paths["precio_oferta_tarjeta"] = self.path_tarjeta
      return paths

class ParisInitialScraper(BaseInitialScraper):
    tienda = "paris"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text.strip().split('\n')[2]

      self.img_link = soup.select("div.product-image-wrapper.sticky#pdp-image-wrapper > a")[0].attrs["href"]

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
        self.path_normal = path + '/' + '0'
        self.caso1 = True
        self.p_normal = string_to_number(precio_normal)

      #Dos precios
      elif cant_precios == 2:
        #Opción 1: Oferta Internet/Temporal y Precio Normal (Caso 2)
        try:
          precio_normal = soup.select(path + ".price-normal > span")[0].text
          precio_internet = soup.select(path)[0].text.strip().split('\n')[0]

          self.path_normal = path + ".price-normal > span" + '/' + '0'
          self.path_oferta = path + '/' + '0'
          self.caso2 = True
          self.p_normal = string_to_number(precio_normal)
          self.p_oferta = string_to_number(precio_internet)

        #Opción 2: Oferta Cencosud y Precio Normal (Caso 3)
        except:
          precio_cencosud = soup.select(path + ".offer-price.price-tc.cencosud-price-2")[0].text.strip().split('\n')[0]
          precio_normal = soup.select(path + "> div > span")[0].text

          self.path_tarjeta = path + ".offer-price.price-tc.cencosud-price-2" + '/' + '0'
          self.path_normal = path + "> div > span" + '/' + '0'
          self.caso3 = True
          self.p_tarjeta = string_to_number(precio_cencosud)
          self.p_normal = string_to_number(precio_normal)

      #Caso 4, tres precios
      elif cant_precios == 3:
        precio_internet = soup.select(path + "> div > span")[0].text
        precio_normal = soup.select(path + ".price-normal > span")[0].text
        precio_cencosud = soup.select(path + ".offer-price.price-tc.cencosud-price-2")[0].text.strip().split('\n')[0]

        self.path_oferta = path + "> div > span" + '/' + '0'
        self.path_normal = path + ".price-normal > span" + '/' + '0'
        self.path_tarjeta = path + ".offer-price.price-tc.cencosud-price-2" + '/' + '0'
        self.caso4 = True

        self.p_oferta = string_to_number(precio_internet)
        self.p_normal = string_to_number(precio_normal)
        self.p_tarjeta = string_to_number(precio_cencosud)

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

class PCFactoryInitialScraper(BaseInitialScraper):
    tienda = "pcfactory"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("div.ficha_titulos > h1 > span")[0].text + ' ' + soup.select("div.ficha_titulos > h1 > span")[1].text
      self.img_link = "https://www.pcfactory.cl" + soup.select("li > img")[3].attrs["src"]

      path = "div.ficha_producto_precio_wrap > div > h2"
      cant_precios = len(soup.select(path))

      if cant_precios == 2:
        precio_efectivo = soup.select(path)[0].text.strip().replace(' ','')
        precio_normal = soup.select(path)[1].text.strip().replace(' ','')

        self.path_efectivo = path + '/' + '0'
        self.path_normal = path + '/' + '1'

      else:
        precio_efectivo = soup.select(path)[0].text.strip().replace(' ','')
        precio_internet = soup.select(path)[1].text.strip().replace(' ','')
        precio_normal = soup.select(path)[2].text.strip().replace(' ','')
        self.p_internet = string_to_number(precio_internet)

        self.path_efectivo = path + '/' + '0'
        self.path_internet = path + '/' + '1'
        self.path_normal = path + '/' + '2'

      self.p_efectivo = string_to_number(precio_efectivo)
      self.p_normal = string_to_number(precio_normal)

    def get_precios(self):
        precios = dict()
        precios["precio_efectivo"] = self.p_efectivo
        precios["precio_normal"] = self.p_normal
        try:
          precios["precio_internet"] = self.p_internet
        except:
          pass
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_efectivo"] = self.path_efectivo
        try:
          paths["precio_internet"] = self.path_internet
        except:
          pass
        return paths

class AntarticaInitialScraper(BaseInitialScraper):
    tienda = "antartica"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("span.txtTitulosRutaSeccionLibros")[0].text
      id = soup.select("span.txt")[1].text.split(' ')[1]
      self.img_link = "https://www.antartica.cl/antartica/gfx_libros/144/" + id + ".jpg"

      path_club = "div.precioClubfichaV"
      path_internet = "div.precioAhoraFicha"
      path_normal = "div.precioAntes"

      try:
        precio_club = soup.select(path_club)[0].text.strip()
      except:
        precio_club = "Oferta no disponible"

      precio_internet = soup.select(path_internet)[0].text
      precio_normal = soup.select(path_normal)[0].text

      self.p_oferta = string_to_number(precio_internet)
      self.p_normal = string_to_number(precio_normal)
      self.p_club = evaluar_precio(precio_club)

      self.path_club = path_club + '/' + '0'
      self.path_oferta = path_internet + '/' + '0'
      self.path_normal = path_normal + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        if self.p_club != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_club
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        if self.p_club != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_club
        return paths

class CruzVerdeInitialScraper(BaseInitialScraper):
    tienda = "cruz verde"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1.product-name")[0].text
      self.img_link = soup.select("div.zoom.js-zoom > img")[0].attrs["src"]

      precio_club = 'Oferta no disponible'
      precio_oferta = 'Oferta no disponible'
      precio_normal = ''

      cant_precios = len(soup.select("span.value"))

      #si hay dos precios para este producto: precio de oferta y precio normal
      if cant_precios == 2:
        precio_oferta = soup.select("span.sales > div > span")[0].text
        precio_normal = soup.select("span.original-value")[0].text

        self.path_oferta = "span.sales > div > span" + '/' + '0'
        self.path_normal = "span.original-value" + '/' + '0'

      #si hay 3 precios, dos precios o bien sólo uno
      if cant_precios == 3:
        #si son 3 precios
        try:
          precio_normal = soup.select("span.original-value")[0].text
          precio_oferta = soup.select("span.sales > span")[0].text
          precio_club = soup.select("span.sales > div > span")[0].text

          self.path_normal = "span.original-value" + '/' + '0'
          self.path_oferta = "span.sales > span" + '/' + '0'
          self.path_club = "span.sales > div > span" + '/' + '0'

        except:
          #si son 2 precios: Club Cruz Verde y precio normal
          try:
            #precio_club = soup.select("span.value.pr-2")[1]
            precio_club = soup.select("span.value.pr-2")[0].text
            precio_normal = soup.select("span.price-original > span")[0].text

            self.path_club = "span.value.pr-2" + '/' + '0'
            self.path_normal = "span.price-original > span" + '/' + '0'

            #sólo está el precio normal
          except:
            precio_club = 'Oferta no disponible'
            precio_normal = soup.select("span.value")[2].text
            self.path_normal = "span.value" + '/' + '2'

      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_club = evaluar_precio(precio_club)

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        if self.p_club != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_club
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        if self.p_club != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_club
        return paths

class SpartaInitialScraper(BaseInitialScraper):
    tienda = "sparta"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text.split('div class="block upsell"')[0]
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1 > span")[0].text
      self.img_link = soup.select("div > img")[0].attrs["src"]

      path = "span.price"
      busqueda = soup.select(path)

      if len(busqueda) > 2:
        cant_precios = len(busqueda[:2])
      else:
        cant_precios = len(busqueda)

      if cant_precios == 2:
        precio_oferta = soup.select(path)[0].text
        precio_normal = soup.select(path)[1].text

        #Nota: (path,num) = path e índice
        self.path_oferta = path + '/' + '0'
        self.path_normal = path + '/' + '1'

      else:
        precio_normal = soup.select(path)[0].text
        precio_oferta = "Oferta no disponible"

        self.path_normal = path + '/' + '0'

      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)

    def get_precios(self):
      precios = dict()
      precios["precio_normal"] = self.p_normal
      if self.p_oferta != "Oferta no disponible":
        precios["precio_oferta_internet"] = self.p_oferta
      return precios

    def get_paths(self):
      paths = dict()
      paths["precio_normal"] = self.path_normal
      if self.p_oferta != "Oferta no disponible":
        paths["precio_oferta_internet"] = self.path_oferta
      return paths

class JumboInitialScraper(BaseInitialScraper):
    tienda = "jumbo"
    def __init__(self, link):
        self.link = link
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")

        text = soup.select("body > script")[0].string

        nombre = text[text.find("productName")+11+5:text.find("productReference")-5]
        cantidad = text[text.find("unit_multiplier")+15+5:text.find("promotions")-5]
        unidad = text[text.find("measurement_unit")+20+5:text.find("unit_multiplier")-9]
        marca = text[text.find("brand")+5+5:text.find("SkuData")-5]

        nombreProducto = nombre +" "+ cantidad +" "+ unidad +" "+ marca

        imgUrl = text[text.find("images")+6+20:text.find("imageTag")-5]

        precio = text[text.find("Price")+5+3:text.find("ListPrice")-3]
        precioOferta = text[text.find("ListPrice")+9+3:text.find("PriceWith")-3]

        self.nombreProducto = nombreProducto
        self.img_link = imgUrl
        self.precio = string_to_number(precio)
        self.path_normal = "path_normal"
        if precio != precioOferta:
            self.precio_oferta = string_to_number(precioOferta)
            self.path_oferta = "path_oferta"
        #No hay paths, y la info siempre está en el mismo lugar

    def get_precios(self):
        precios = {"precio_normal": self.precio}
        try:
            precios["precio_oferta"] = self.precio_oferta
        except:
            pass
        return precios

    def get_paths(self):
        paths = {"precio_normal": self.path_normal}
        try:
            paths["precio_oferta"] = self.path_oferta
        except:
            pass
        return paths

class JumboScraper(BaseScraper):
    def __init__(self,link,path):
        self.status = 0
        self.path = path
        soup = BeautifulSoup(requests.get(link).content, features="html.parser")
        text = soup.select("body > script")[0].string
        try:
            if path == "path_normal":
                precio = text[text.find("Price")+5+3:text.find("ListPrice")-3]
            elif path == "path_oferta":
                precio = text[text.find("ListPrice")+9+3:text.find("PriceWith")-3]
            self.precio = string_to_number(precio)
        except:
            self.status = 2

class SteamInitialScraper(BaseInitialScraper):
    tienda = "steam"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente, features="html.parser")

        self.nombreProducto = soup.select("div.apphub_AppName")[0].text
        self.img_link = soup.select("img.game_header_image_full")[0].attrs["src"]

        precio_oferta = "Oferta no disponible"
        path_oferta = ''

        try: #si hay oferta
          path_normal = "div.discount_original_price"
          path_oferta = "div.discount_final_price"
          precio_normal = soup.select(path_normal)[0].text
          precio_oferta = soup.select(path_oferta)[0].text

        except: #no hay oferta
          path_normal = "div.game_purchase_price.price"
          precio_normal = soup.select(path_normal)[0].text.strip()

        self.p_oferta = evaluar_precio(precio_oferta)
        self.p_normal = string_to_number(precio_normal)

        self.path_oferta = path_oferta + '/' + '0'
        self.path_normal = path_normal + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta"] = self.path_oferta
        return paths

class TottusInitialScraper(BaseInitialScraper):
    tienda = "tottus"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.nombreProducto = soup.select("h1")[0].text
        self.img_link = soup.select("div.product-gallery > img")[0].attrs["src"]

        precio_tarjeta = "Oferta no disponible"
        precio_internet = "Oferta no disponible"

        path = "div.ProductPrice.big > span > span"
        path_oferta = ''
        path_tarjeta = ''
        cant_precios = len(soup.select(path))

        if cant_precios == 3:
          precio_tarjeta = soup.select(path)[0].text
          precio_internet = soup.select(path)[1].text
          precio_normal = soup.select(path)[2].text

          path_tarjeta = path + '/' + '0'
          path_oferta = path + '/' + '1'
          path_normal = path + '/' + '2'

        #pueden ser dos combinaciones: Tarjeta/Normal y Internet/Normal
        elif cant_precios == 2:
          diferenciador = soup.select(path)[0].attrs["data-pricerules"]

          if diferenciador == "pricerule13": #Tarjeta/Normal
            precio_tarjeta = soup.select(path)[0].text
            precio_normal = soup.select(path)[1].text

            path_tarjeta = path + '/' + '0'
            path_normal = path + '/' + '1'

          else: #Internet/Normal
            precio_internet = soup.select(path)[0].text
            precio_normal = soup.select(path)[1].text

            path_oferta = path + '/' + '0'
            path_normal = path + '/' + '1'

        #un solo precio
        else:
          precio_normal = soup.select(path)[0].text
          path_normal = path + '/' + '0'

        self.p_tarjeta = evaluar_precio(precio_tarjeta)
        self.p_oferta = evaluar_precio(precio_internet)
        self.p_normal = string_to_number(precio_normal)

        self.path_normal = path_normal
        self.path_oferta = path_oferta
        self.path_tarjeta = path_tarjeta

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        if self.p_tarjeta != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        if self.p_tarjeta != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_tarjeta
        return paths

class BoldInitialScraper(BaseInitialScraper):
    tienda = "bold"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("span.trimName")[0].text
      self.img_link = "https://bold.cl/" + soup.select("div.item > div > img")[0].attrs["data-src"]

      path = "div.item--price"
      precio_normal = soup.select(path)[0].text.strip()
      precio_oferta = "Oferta no disponible"

      if '-' in precio_normal:
        precio_oferta = precio_normal.split('-')[1].strip()
        precio_normal = precio_normal.split('-')[0].strip()
        #path_oferta = "div.price-with-discount"

      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_normal = string_to_number(precio_normal)

      self.path_normal = path + '/' + '0'
      self.path_oferta = path + '/' + '1'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class ContrapuntoInitialScraper(BaseInitialScraper):
    tienda = "contrapunto"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.nombreProducto = soup.select("h1")[0].text
        self.img_link = soup.select("div.print-image.hide > img")[0].attrs["src"]

        path_internet = "span.product-price"
        path_normal = "span.regular-price"

        precio_internet = soup.select(path_internet)[0].text
        precio_normal = soup.select(path_normal)[0].text

        self.p_oferta = string_to_number(precio_internet)
        self.p_normal = string_to_number(precio_normal)

        self.path_oferta = path_internet + '/' + '0'
        self.path_normal = path_normal + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        return paths

class ChevroletInitialScraper(BaseInitialScraper):
    tienda = "chevrolet"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.nombreProducto = soup.select("#nav_anchor > span.q-js-button-text.hide-for-large-down")[0].text
        try:
            img_link = "https://www.chevrolet.cl" + soup.select('div.q-responsive-image.q-responsive-image-container.stat-image-link[data-dtm="masthead"] > picture > source')[0].attrs["data-srcset"].split(',')[0][:-4] + '1500'
        except:
            img_link = "https://www.chevrolet.cl" + soup.select('div.q-responsive-image.q-responsive-image-container.stat-image-link[data-dtm="responsive image"] > picture > source')[0].attrs["data-srcset"].split(',')[0][:-4] + '1500'

        self.img_link = img_link
        self.precio = string_to_number(soup.select("span.q-descriptive1")[0].text)
        self.path = "span.q-descriptive1" + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.precio
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path
        return paths

class MercadoLibreScraper(BaseInitialScraper):
    tienda = "mercado libre"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text
      self.img_link = soup.select("figure > img")[0].attrs["data-zoom"]

      precio_oferta = "Oferta no disponible"
      path = "span.price-tag-fraction"
      cant_precios = len(soup.select(path)[:-1])

      precio_normal = soup.select(path)[0].text

      if cant_precios == 2:
        precio_oferta = soup.select(path)[1].text

      self.path = path
      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)

      self.path_normal = self.path + '/' + '0'
      self.path_oferta = self.path + '/' + '1'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta"] = self.path_oferta
        return paths

class SubaruInitialScraper(BaseInitialScraper):
    tienda = "subaru"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      path = "div.cont > p.price"
      self.nombreProducto = soup.select("h1")[0].text
      self.img_link = "https://www.subaru.cl" + soup.select("div#descubre_foto")[0].attrs["data-desktop"]
      self.precio = string_to_number(soup.select(path)[0].text)
      self.path = path + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.precio
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path
        return paths

class LinioInitialScraper(BaseInitialScraper):
    tienda = "linio"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text.strip()
      self.img_link = soup.select("img.image-modal")[0].attrs["data-lazy"]

      precio_oferta = "Oferta no disponible"
      precio_tarjeta = "Oferta no disponible"

      path_ofertas = "div.lowest-price > span"
      path_normal = "span.original-price"
      cant_precios = len(soup.select(path_ofertas))

      #por alguna razón, si un producto tiene 3 precios, cant_precios = 8, o bien si tiene 2 precios: Tarjeta/Normal
      if cant_precios == 8:
        try: #tres precios: Tarjeta/Oferta/Normal
          precio_normal = soup.select(path_normal)[0].text
          precio_oferta = soup.select(path_ofertas)[0].text.strip()
          precio_tarjeta = soup.select(path_ofertas)[1].text

        except: #dos precios: Tarjeta/Normal
          path_normal = path_ofertas
          precio_normal = soup.select(path_normal)[0].text.strip()
          precio_tarjeta = soup.select(path_ofertas)[1].text.strip()

      else:
        try: #dos precios: Oferta/Normal
          precio_normal = soup.select(path_normal)[0].text
          precio_oferta = soup.select(path_ofertas)[0].text.strip()

        except: #un único precio
          path_normal = path_ofertas
          precio_normal = soup.select(path_normal)[0].text.strip()

      self.path_normal = path_normal + '/' + '0'
      self.path_oferta = path_ofertas + '/' + '0'
      self.path_tarjeta = path_ofertas + '/' + '1'

      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_tarjeta = evaluar_precio(precio_tarjeta)

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        if self.p_tarjeta != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        if self.p_tarjeta != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_tarjeta
        return paths

class HomecenterSodimacInitialScraper(BaseInitialScraper):
    tienda = "homecenter sodimac"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text
      data = str(soup.select("script")[1]).replace('<script type="application/ld+json">','').replace('</script>','')
      bug_fix = data.index("description") - len('description') + 4
      data = json.loads(data[:bug_fix] + '}')
      self.img_link = data['image']

      clase = '.'
      identicador = soup.select("div.product-price-and-logo > div > div > div")[0].attrs["class"]
      for x in identicador:
        if x != identicador[-1]:
          clase += x + '.'
        else:
          clase += x

      path = "div" + clase
      precio_tarjeta = soup.select(path)[0].text
      precio_normal = soup.select(path)[1].text

      if precio_tarjeta == precio_normal:
        precio_tarjeta = "Oferta no disponible"

      self.path = path
      self.p_normal = string_to_number(precio_normal)
      self.p_tarjeta = evaluar_precio(precio_tarjeta)

      self.path_normal = path + '/' + '1'
      self.path_tarjeta = path + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_tarjeta != "Oferta no disponible":
          precios["precio_oferta_tarjeta"] = self.p_tarjeta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_tarjeta != "Oferta no disponible":
          paths["precio_oferta_tarjeta"] = self.path_tarjeta
        return paths

class PetHappyInitialScraper(BaseInitialScraper):
    tienda = "pet happy"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text
      self.img_link = soup.select("img")[1].attrs["src"]
      self.precio_size = False

      precio_normal = "Oferta no disponible"
      precio_oferta = "Oferta no disponible"
      precio_chico = "Oferta no disponible"
      precio_grande = "Oferta no disponible"

      try: #hay oferta
        path_oferta = "strong.desc > span"
        path_normal = "span#product-page-price-before"

        precio_oferta = soup.select(path_oferta)[0].text
        precio_normal = soup.select(path_normal)[0].text

        self.path_oferta = path_oferta + '/' + '0'
        self.path_normal = path_normal + '/' + '0'

      except: #no hay oferta, o bien, hay dos precios: Product Tamaño Chico/Grande
        cant_precios = len(soup.select('span[itemprop="price"]'))

        if cant_precios == 1: #no hay oferta
          path_normal = "h2 > span"
          self.path_normal = path_normal + '/' + '0'

          precio_oferta = "Oferta no disponible"
          precio_normal = soup.select(path_normal)[0].text

        else: #dos precios: Product Tamaño Chico/Grande
          self.precio_size = True
          path_size = 'span[itemprop="price"]'
          self.path_chico = path_size + '/' + '0'
          self.path_grande = path_size + '/' + '1'

          precio_chico = soup.select(path_size)[0].text
          precio_grande = soup.select(path_size)[1].text

      self.p_normal = evaluar_precio(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_chico = evaluar_precio(precio_chico)
      self.p_grande = evaluar_precio(precio_grande)

    def get_precios(self):
        precios = dict()
        if self.precio_size:
          precios["precio_chico"] = self.p_chico
          precios["precio_grande"] = self.p_grande
        else:
          precios["precio_normal"] = self.p_normal
          if self.p_oferta != "Oferta no disponible":
            precios["precio_oferta"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        if self.precio_size:
          paths["precio_chico"] = self.path_chico
          paths["precio_grande"] = self.path_grande
        else:
          paths["precio_normal"] = self.path_normal
          if self.p_oferta != "Oferta no disponible":
            paths["precio_oferta"] = self.path_oferta
        return paths

class LaCasaDelVeganInitialScraper(BaseInitialScraper):
    tienda = "la casa del vegan"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text

      try:
        self.img_link = soup.select("img#first-image")[0].attrs["src"]
      except:
        self.img_link = soup.select("img.img-fluid")[1].attrs["src"]


      precio_oferta = "Oferta no disponible"
      cant_precios = len(soup.select("div.form-price_desktop > span"))

      if cant_precios == 2:
        path_oferta = "span#product-form-price"
        path_normal = "span#product-form-discount"

        precio_oferta = soup.select(path_oferta)[0].text
        precio_normal = soup.select(path_normal)[0].text

      else:
        path_normal = "span#product-form-price"
        path_oferta = ''
        precio_normal = soup.select(path_normal)[0].text

      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)

      self.path_normal = path_normal + '/' + '0'
      self.path_oferta = path_oferta + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.path_oferta != '':
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class DecathlonInitialScaper(BaseInitialScraper):
    tienda = "decathlon"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text
      self.img_link = soup.select("div.product-cover > img")[0].attrs["src"]

      if soup.select("strike.strikprice") != []:
        precio_oferta = soup.select("span.price-tag")[0].text
        precio_normal = soup.select("strike.strikprice")[0].text.strip()

        path_oferta = "span.price-tag"
        path_normal = "strike.strikprice"

      else:
        precio_oferta = "Oferta no disponible"
        precio_normal = soup.select("span.price-tag")[0].text

        path_oferta = ''
        path_normal = "span.price-tag"

      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_normal = string_to_number(precio_normal)
      self.path_oferta = path_oferta + '/' + '0'
      self.path_normal = path_normal + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class CasaAmarillaInitialScraper(BaseInitialScraper):
    tienda = "casa amarilla"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text.split('div class="box-collateral box-related"')[0]
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select('h1[itemprop="name"]')[0].text.strip()
      self.img_link = soup.select("div.product-image > img")[0].attrs["src"]

      path = "span.price"
      cant_precios = len(soup.select(path))

      if cant_precios == 2:
        precio_oferta = soup.select(path)[0].text.strip()
        precio_normal = soup.select(path)[1].text.strip()

        self.path_oferta = path + '/' + '0'
        self.path_normal = path + '/' + '1'

      else:
        precio_oferta = "Oferta no disponible"
        precio_normal = soup.select(path)[0].text.strip()
        self.path_oferta = ''
        self.path_normal = path + '/' + '0'

      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_normal = string_to_number(precio_normal)


    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class CasaRoyalInitialScraper(BaseInitialScraper):
    tienda = "casa royal"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text.split('div class="box-collateral box-related"')[0]
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select('h1[itemprop="name"]')[0].text
      self.img_link = soup.select("div.product-image > img")[0].attrs["src"]

      path = "span.price"
      cant_precios = len(soup.select(path))

      if cant_precios == 2:
        precio_oferta = soup.select(path)[0].text.strip()
        precio_normal = soup.select(path)[1].text.strip()

        self.path_oferta = path + '/' + '0'
        self.path_normal = path + '/' + '1'

      else:
        precio_oferta = "Oferta no disponible"
        precio_normal = soup.select(path)[0].text.strip()
        self.path_oferta = ''
        self.path_normal = path + '/' + '0'

      self.p_oferta = evaluar_precio(precio_oferta)
      self.p_normal = string_to_number(precio_normal)

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class FeriaChilenaDelLibro(BaseInitialScraper):
    tienda = "feria chilena del libro"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text.split('section class="related products"')[0]
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text.strip()
      self.img_link = soup.select("div.woocommerce-product-gallery__image > a")[0].attrs["href"]

      path = "span.woocommerce-Price-amount.amount"
      cant_precios = len(soup.select(path))

      if cant_precios == 1:
        precio_normal = soup.select(path)[0].text.strip()
        precio_oferta = "Oferta no disponible"

      else:
        precio_normal = soup.select(path)[0].text
        precio_oferta = soup.select(path)[1].text

      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)
      self.path_normal = path + '/' + '0'
      self.path_oferta = path + '/' + '1'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class EstacionNaturalInitialScraper(BaseInitialScraper):
    tienda = "estacion natural"
    def __init__(self,link):
      self.link = link
      fuente = requests.get(link).text.split('<div class="related-products__title "> <h4 class="title center">Artículos relacionados</h4> <div class="feature_divider"></div></div>')[0]
      soup = BeautifulSoup(fuente,features="html.parser")

      self.nombreProducto = soup.select("h1")[0].text
      img = str(soup.select("div.image__container")[0])
      self.img_link = 'https://' + img[img.find('data-src')+12:img.find('data-srcset')-2]
      #self.img_link = "//" + str(soup.select("div.image__container")[0]).split('//')[-1].replace("/></div>",'').replace('"','')

      path = "span.money"
      precio_oferta = "Oferta no disponible"
      cant_precios = len(soup.select(path)[1:])

      #dos precios
      if cant_precios == 3:
        precio_oferta = soup.select(path)[1].text
        precio_normal = soup.select(path)[2].text

        self.path_oferta = path + '/' + '1'
        self.path_normal = path + '/' + '2'

      #un único precio
      else:
        precio_normal = soup.select(path)[1].text

        self.path_oferta = ''
        self.path_normal = path + '/' + '1'


      self.p_normal = string_to_number(precio_normal)
      self.p_oferta = evaluar_precio(precio_oferta)

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        if self.p_oferta != "Oferta no disponible":
          precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        if self.p_oferta != "Oferta no disponible":
          paths["precio_oferta_internet"] = self.path_oferta
        return paths

class OrtopediaOnlineInitialScraper(BaseInitialScraper):
    tienda = "ortopedia online"
    def __init__(self,link):
        self.link = link
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        fuente = requests.get(link,headers=headers).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.nombreProducto = soup.select("h1")[0].text.strip()
        self.img_link = soup.select("img.img-thumbnail")[0].attrs["src"]

        self.precio = string_to_number(soup.select("h2")[0].text)
        self.path = "h2" + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.precio
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path
        return paths

class SuzukiInitialScraper(BaseInitialScraper):
    tienda = "suzuki"
    def __init__(self,link):
        self.link = link
        fuente = requests.get(link).text
        soup = BeautifulSoup(fuente,features="html.parser")

        self.nombreProducto = soup.select("h1")[0].text
        self.img_link = soup.select("div.container.position-relative > img")[0].attrs["src"]

        self.p_normal = string_to_number(soup.select("span.full-price")[0].text)
        self.p_oferta = string_to_number(soup.select("span.discount-applied-price")[0].text)

        self.path_normal = "span.full-price" + '/' + '0'
        self.path_oferta = "span.discount-applied-price" + '/' + '0'

    def get_precios(self):
        precios = dict()
        precios["precio_normal"] = self.p_normal
        precios["precio_oferta_internet"] = self.p_oferta
        return precios

    def get_paths(self):
        paths = dict()
        paths["precio_normal"] = self.path_normal
        paths["precio_oferta_internet"] = self.path_oferta
        return paths
