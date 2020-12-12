
#views, modelos y demases
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from apps.users.models import Usuario

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, **options):
    products = Producto.objects.all()
    for prod in products:
      historiales = Historial.objects.filter(producto = prod)
      tienda = prod.tienda.nombre
      link = prod.link
      for hist in historiales:
        scraper = seleccionar_scraper(tienda, link, hist.bs4path)
        status = scraper.check_status()
        if status == 0:  #Mismo path
          precio = scraper.get_precio()
          historial = Historial(producto = prod, tipo = hist.tipo, precio = precio, bs4path = hist.bs4path, disponible=1)
          historial.save()
        elif status == 1: #Distinto path
          precio = scraper.get_precio()
          path = scraper.get_path()
          historial = Historial(producto = prod, tipo = hist.tipo, precio = precio, bs4path = path, disponible=1)
        elif status == 2: # No Disponible?¿
          pass

