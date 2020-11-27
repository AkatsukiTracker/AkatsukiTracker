from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
#imports raros que veré si se ocupan

#views, modelos y demases
from django.views.generic import TemplateView
from .models import *
from .forms import *
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .scrapers import *

import json


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'tracker/profile.html')

def trending(request):
    return render(request, 'tracker/trending.html' )

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

@login_required(login_url='login')
@api_view(['POST','GET'])
def check_url(request):

    if request.method == 'GET':
        link = request.GET['url']
        try:
            tienda = link.split('/')[2]
        except:
            pass
        if len(link) != 0 and tiendaDisponible(tienda):
            if tienda == "www.falabella.com":
                scraper = FalabellaInitialScraper(link)
                #tienda
                tienda = "falabella"

            #precios
            precios = scraper.get_precios()
            #nombre
            nombre = scraper.get_nombre()
            #paths
            paths = scraper.get_paths()
            #link imagen
            img = scraper.get_img()

            return Response({"message": "OK", "data": {"tienda": tienda, "precios": precios, "paths": paths, "nombre": nombre, "link": link, "img": img}})
    return Response({"message": "NOT OK"})

@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        #usuario
        user = User.objects.filter(username=request.user.username)[0]
        #DATOS
        datos = request.POST
        datos = json.loads(datos['datos'])

        #producto
        nombre_producto = datos['nombre']
        link = datos['link']
        img = datos['img']

        #tienda
        tienda = Tienda.objects.filter(nombre=datos["tienda"])[0]    #[0]?

        #historiales
        precios = []
        tipo_precios = []
        paths = []
        for i in datos["precios"]:
            tipo_precios.append(i)
            precios.append(datos["precios"][i])
            paths.append(datos["paths"][i])

        #Crear Instancias de los Modelos

        #Producto
        producto = Producto(nombre = nombre_producto, link = link, tienda = tienda, img_link = img)
        producto.save()

        #Historiales
        for i in range(len(precios)):
            historial = Historial(producto = producto, tipo = tipo_precios[i], precio = int(precios[i]), bs4path = paths[i], disponible=1)
            historial.save()

        #ProductoUsuario
        productoUsuario = ProductoUsuario(producto = producto, user = user)
        productoUsuario.save()


        return HttpResponse("OK")
    if request.method == 'GET':
        return redirect('dashboard')
    return HttpResponse("NOT OK")
