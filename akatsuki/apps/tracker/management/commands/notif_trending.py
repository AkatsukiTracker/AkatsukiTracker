from django.conf import settings 
from django.core.mail import send_mail 
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from apps.users.models import Usuario

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

from django.core.management.base import BaseCommand

#Algoritmo adaptado para la tupla (n,producto)
def first(n):
    return n[0]

class Command(BaseCommand):
    def handle(self, **options):

        producto_a_mandar = []
        # nombre : nombre, tienda, link, img, precio más bajo
        lista_productos = []  # (len(producto_usuario),producto )

        for producto in Producto.objects.all():
            lista_productos.append( (len(ProductoUsuario.objects.filter(producto=producto)), producto) )

        lista_productos.sort(key=first, reverse=True)

        if len(lista_productos) >= 5:
            lista_productos = lista_productos[:5]

        contador = 1
        for _, producto in lista_productos:
            nombre = producto.nombre
            tienda = producto.tienda.nombre
            link = producto.link
            img = producto.img_link
            tipo_precio = ""
            tipos = list()
            precio_bajo = float("inf")
            for hist in Historial.objects.filter(producto=producto):
                if hist.tipo not in tipos:
                    tipos.append(hist.tipo)
            historiales = []
            for tipo in tipos:
                historiales.append(Historial.objects.filter(producto = producto, tipo=tipo)[::-1][0])
            for hist in historiales:
                if hist.precio < precio_bajo and -1 < hist.precio:
                    precio_bajo = hist.precio
                    tipo_precio = hist.tipo

            producto_a_mandar.append((contador, {'nombre': nombre,
                                        'tienda': tienda,
                                        'link': link,
                                        'img': img,
                                        'precio': precio_bajo}))
            contador += 1

        for user in Usuario.objects.all():
            if user.notificaciones:
                
                msg_html = render_to_string('mails/trending.html', {'user': user.username, 
                                                                    'productos': producto_a_mandar})

                send_mail(
                '¡Estos son los productos más populares de esta semana!', #Titulo  
                "", #Mensaje
                settings.EMAIL_HOST_USER , #Emisor
                [user.email], #Destinatario
                html_message=msg_html, #Template
                )
