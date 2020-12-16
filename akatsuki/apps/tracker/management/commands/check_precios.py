#views, modelos y demases
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from apps.users.models import Usuario

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

from apps.users.models import *

import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, **options):
    for user in Usuario.objects.all():
      prod_usuario = ProductoUsuario.objects.filter(user=user)
      productos = []
      for prod_user in prod_usuario:
        productos += prod_user.producto
      
      # x = media

      args = dict()   #Argumentos temporales para organizar
      productos_mail = {} #{producto: [(tipo, precio, baja/subida)]}    Productos destinados a mandar al correo
      for producto in productos:
        if ProductoUsuario.objects.filter(user=user, producto=producto)[0].notificaciones: #Checkeo si quiere notificaciones
         
          productos_mail[producto.nombre] = []
          args[producto.nombre] = {}
          historiales = Historial.objects.filter(producto=producto)
          medias = []   # ( tipo,  x )
          precios = {}

          for historial in historiales:
            
            if historial.tipo not in precios:
              precios[historial.tipo] = []           
             
            precios[historial.tipo] += historial.precio

          if condicion_tiempo:      #Falta hacer una condicion buena

            for i in precios:
            medias += (i, sum(precios[i])/len(precios[i])  )

            for historial in historiales_condicion: #aaaaaaaaaaa
                
              if ultimo_precio < x:

                productos_mail[producto.nombre] += (historial.tipo, historial.precio, "baja") 

              elif ultimo_precio > x:

                productos_mail[producto.nombre] += (historial.tipo, historial.precio, "subida") 


      mandar_mail (":)")

              
                

              

    