from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from apps.users.models import Usuario

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, **options):
    for user in Usuario.objects.all():
      if user.notificaciones_prod:
        prod_usuario = ProductoUsuario.objects.filter(user=user)
        productos = []
        for prod_user in prod_usuario:
          productos.append(prod_user.producto)

        for producto in productos:
          if ProductoUsuario.objects.filter(user=user, producto=producto)[0].notificaciones:

            historiales = Historial.objects.filter(producto=producto)
            precios = {}
            for historial in historiales:

              if historial.tipo not in precios:
                precios[historial.tipo] = []

              precios[historial.tipo].append(historial.precio)

            ultimo_precio = float("inf")
            precio_anterior = float("inf") #Precio justo anterior

            mandar = False

            for i in precios:
              precio_anterior = precios[i][::-1][1]
              ultimo_precio = precios[i][::-1][0]
              media = sum(precios[i])/len(precios[i])

              if ultimo_precio < media:
                precio_bajo = ultimo_precio
                precio_alto = precio_anterior
                mandar = True

            if mandar:

              link_img = producto.img_link

              link_producto = producto.link


              msg_html = render_to_string('mails/offer.html', {'user': user.username,
                                                              'precio_bajo': precio_bajo,
                                                              'precio_alto': precio_alto,
                                                              'img': link_img,
                                                              'link': link_producto})

              send_mail(
                '¡Uno de tus productos bajó de precio!', #Titulo
                "", #Mensaje
                settings.EMAIL_HOST_USER , #Emisor
                [user.email], #Destinatario
                html_message=msg_html, #Template
              )



