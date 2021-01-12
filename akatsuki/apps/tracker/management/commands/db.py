from django.contrib.auth.models import User
from apps.users.models import Usuario

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

import random

import datetime

from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, **options):

    prod = Producto.objects.filter(id = 53)[0]
    precio_anterior = 40000
    for dia in range(1,12):
      fecha = "2021-01-" + str(dia) +  " 17:41"
      fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")
      precio_nuevo = int(precio_anterior * (random.randint(90,110)/100))
      precio_oferta = int(precio_nuevo * (random.randint(80,90)/100))
      print(fecha, precio_nuevo)
      precio_anterior = precio_nuevo
      h = Historial(producto=prod, fecha=fecha, tipo="precio_normal", precio=precio_nuevo, bs4path="div.precioAntes/0", disponible=1)
      h.save()

      h = Historial(producto=prod, fecha=fecha, tipo="precio_oferta_internet", precio=precio_oferta, bs4path="div.precioAhoraFicha/0", disponible=1)
      h.save()

