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
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .scrapers import *


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'tracker/profile.html')
'''
def check_url(request):
    tmpl_vars = {'form': CheckUrlForm()}
    return render(request, 'tracker/check_url.html', tmpl_vars)
'''

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

@login_required(login_url='login')
@api_view(['POST','GET','PUT'])
def check_url(request):

    if request.method == 'POST':
        base_url = reverse('add_product')
        context = {"xd":"owo"}
        urlcontext = urlencode({'context': context})
        url = "{}?{}".format(base_url, urlcontext)
        return redirect(url)
    if request.method == 'PUT':
        link = request.data
        tienda = link.split('/')[2]
        if tienda == "www.falabella.com":
            scraper = FalabellaInitialScraper(link)
            #precios
            precios = scraper.get_precios()
            #nombre
            nombre = scraper.get_nombre()
            #tienda
            tienda = "falabella"
            #paths
            paths = scraper.get_paths()
        #serializer = CheckUrlSerializer(data = {"tienda": tienda, "precios": precios, "paths": paths, "nombre": nombre, "link": link})
        #serializer.is_valid()
        return Response({"message": "Funcionó!", "data": {"tienda": tienda, "precios": precios, "paths": paths, "nombre": nombre, "link": link}})
    return Response({"message": "Introduce un link para continuar"})

@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        #usuario
        username = request.user.username
        pk = request.user.pk
        #producto
        return HttpResponse("xd")
    return HttpResponse(request.GET.get("xd"))

    
    
        


















# EN DESARROLLO
'''
@login_required(login_url='login')
def add_product(request):
    AddProductFormSet = inlineformset_factory(Producto, ProductoUsuario, fk_name='producto', fields=('',))
    user = Usuario.objects.get(id=request.user.id)
    try:
        producto = Producto.objects.get(id=ProductoUsuario.producto)
        formset = AddProductFormSet(queryset=producto.objects.none(), instance=user)
    except:
        producto = Producto.objects.none()
        formset = AddProductFormSet(queryset=producto, instance=user)
    
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = AddProductForm(request.POST)
        formset = OrderFormSet(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request, 'tracker/add_product.html', context) 
'''
