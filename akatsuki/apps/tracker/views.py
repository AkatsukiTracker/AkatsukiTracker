from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.forms import inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
#imports raros que veré si se ocupan

#views, modelos y demases
from django.views.generic import TemplateView
from .models import *
from .forms import *
from django.contrib.auth.models import User
from apps.users.models import Usuario

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .scrapers import *

import json
from django.core.serializers.json import DjangoJSONEncoder

import hashlib


@login_required(login_url='login')
def dashboard(request):
    if request.method == 'GET':
        user = User.objects.filter(username=request.user.username)[0]
        args = {
                "productos": [],
                "productos_json": {},
                "historiales": {},
                "links": [],
                "user": user
                }


        for p in ProductoUsuario.objects.filter(user=user):
            producto = p.producto
            historial = Historial.objects.filter(producto = producto)

            d_producto = {
                "id": producto.id,
                "nombre": producto.nombre,
                "tienda": (producto.tienda).nombre.capitalize(),
                "img": producto.img_link,
                "link": producto.link,
                "precio": historial[::-1][0].precio,
                "notificaciones": p.notificaciones
            }
            args["productos"].append(d_producto)
            args["productos_json"][producto.id] = d_producto
            args["historiales"][producto.id] = json.dumps(list(historial.values_list('tipo', 'fecha', 'precio' )), cls=DjangoJSONEncoder)
            args["links"].append(producto.link)


        return render(request, 'tracker/index.html', args)
    return render(request, 'tracker/index.html')

@login_required(login_url='login')
def profile(request):

    user = User.objects.filter(username=request.user.username)[0]
    username = user.username
    email = user.email

    usuario = Usuario.objects.filter(username=request.user.username)[0]
    if usuario and usuario.img_perfil:
        img = usuario.img_perfil.name[7:]
    else:
        img = "imgs_perfil/default.png"

    fecha = user.date_joined

    args = {"nombre": username, "email": email, "img": img, "fecha": fecha, "notificaciones": usuario.notificaciones_prod, "trending" : usuario.notificaciones}
    return render(request, 'tracker/profile.html', args)

def trending(request):
    if request.method == 'GET':
        if request.user.username != "":
          user = User.objects.filter(username=request.user.username)[0]
        else:
          user = False

        args = {
                "productos": [],
                "user": user
                }

        productos = Producto.objects.all()[::-1]

        for producto in productos:

            productosUsuarios = ProductoUsuario.objects.filter(producto = producto)

            tipos = []
            for historial in Historial.objects.filter(producto = producto):
                if historial.tipo not in tipos:
                    tipos.append(historial.tipo)

            historiales = []
            for i in range(len(tipos)):
                historiales.append(Historial.objects.filter(producto = producto, tipo = tipos[i])[::-1][0])

            precio = float("inf")
            for historial in historiales:
                if historial.precio < precio:
                    precio = historial.precio
                    ultimo_historial = historial

            d_producto = {
                "id": producto.id,
                "nombre": producto.nombre,
                "tienda": (producto.tienda).nombre.capitalize(),
                "img": producto.img_link,
                "link": producto.link,
                "precio": ultimo_historial.precio,
                "subscripciones": len(productosUsuarios),
                "agregado": False
            }
            if user:
                d_producto['agregado'] = ProductoUsuario.objects.filter(producto = producto, user = user).exists()


            args["productos"].append(d_producto)

        return render(request, 'tracker/trending.html', args)
    return render(request, 'tracker/trending.html' )

@login_required(login_url='login')
@api_view(['GET'])
def check_url(request):

    if request.method == 'GET':
        link = request.GET['url']
        try:
            tienda = link.split('/')[2]
        except:
            return Response({"message": "NOT OK", "error": "Invalid method"})
        if len(link) != 0 and tiendaDisponible(tienda):
            tienda, scraper = seleccionar_scraper_initial(tienda, link)

            #precios
            precios = scraper.get_precios()
            #nombre
            nombre = scraper.get_nombre()
            #paths
            paths = scraper.get_paths()
            #link imagen
            img = scraper.get_img()

            return Response({"message": "OK", "data": {"tienda": tienda, "precios": precios, "paths": paths, "nombre": nombre, "link": link, "img": img}})
    return Response({"message": "NOT OK", "error": "Invalid method"})

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
            #hash del link
        result = hashlib.md5(link.encode())
        link_hash = result.hexdigest()

        img = datos['img']

        producto = Producto.objects.filter(link = link)

        if len(producto) == 1:
            producto = producto[0]
            if len(ProductoUsuario.objects.filter(producto=producto, user=user)) == 1:
                return HttpResponse("Este producto ya está entre sus subscripciones")
            else:
                productoUsuario = ProductoUsuario(producto = producto, user = user)
                productoUsuario.save()
        else:

            #tienda
            tienda = Tienda.objects.filter(nombre=datos["tienda"])[0]

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
            producto = Producto(nombre = nombre_producto, link = link, tienda = tienda, img_link = img, link_hash= link_hash)
            producto.save()

            #Historiales
            for i in range(len(precios)):
                historial = Historial(producto = producto, tipo = tipo_precios[i], precio = int(precios[i]), bs4path = paths[i], disponible=1)
                historial.save()

            #ProductoUsuario
            productoUsuario = ProductoUsuario(producto = producto, user = user, notificaciones= 1)
            productoUsuario.save()

        return redirect('dashboard')
    return redirect('dashboard')


@login_required(login_url='login')
def delete_product(request):
    if request.method == 'GET':
        user = User.objects.filter(username=request.user.username)[0]
        producto = Producto.objects.filter(id=json.loads(request.GET['id']))[0]
        producto_usuario = ProductoUsuario.objects.filter(producto = producto, user = user)[0]
        producto_usuario.delete()
        return redirect('dashboard')
    return redirect('dashboard')

@login_required(login_url='login')
@api_view(['GET'])
def check_info(request):
    if request.method == 'GET':

        args = {"historiales": {},}

        link = request.GET['url']
        producto = Producto.objects.filter(link = link)[0]

        args["producto"] = producto.nombre

        historiales = Historial.objects.filter(producto = producto)
        for i in historiales:
            nombre_historial = i.tipo
            precio = i.precio
            fecha = i.fecha
            disponibilidad = i.disponible

            if nombre_historial not in args["historiales"]:
                args["historiales"][nombre_historial] = []
            args["historiales"][nombre_historial].append( (precio, fecha, disponibilidad) )

        return Response( args )
    return redirect('dashboard')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente')
        else:
            messages.error(request, str(form.errors))
        return redirect('profile')
    else:
        return HttpResponse(status=404)

@login_required(login_url='login')
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Correo actualizado correctamente')
        else:
            messages.error(request, str(form.errors))
        return redirect('profile')
    else:
        return HttpResponse(status=404)

@login_required(login_url='login')
def profile_picture(request):
    if request.method == 'POST':
        form = ImgPerfilForm(request.POST, request.FILES)
        if form.is_valid():
           user = Usuario.objects.filter(username=request.user.username)[0]
           user.img_perfil = request.FILES['file']
           user.save()
           messages.success(request, 'Imagen actualizada correctamente')
        else:
            messages.error(request, str(form.errors))
        return redirect("profile")
    else:
        return HttpResponse(status=404)

@login_required(login_url='login')
@api_view(['POST'])
def change_notif_trending(request):
    if request.method == 'POST':
        user = Usuario.objects.filter(username=request.user.username)[0]
        if user.notificaciones:
            user.notificaciones = False
        else:
            user.notificaciones = True
        user.save()
        return Response('OK')
    return Response('NOT OK')

@login_required(login_url='login')
@api_view(['POST'])
def change_notif_prod_all(request):
    if request.method == 'POST':
        user = Usuario.objects.filter(username=request.user.username)[0]
        if user.notificaciones_prod:
            user.notificaciones_prod = False
        else:
            user.notificaciones_prod = True
        user.save()
        return Response('OK')
    return Response('NOT OK')

@login_required(login_url='login')
@api_view(['POST'])
def change_notif_prod(request):
    if request.method == 'POST':
        user = Usuario.objects.filter(username=request.user.username)[0]
        producto = Producto.objects.filter(id=request.POST['producto'])[0]
        prod_user = ProductoUsuario.objects.filter(user=user, producto=producto)[0]
        if prod_user.notificaciones:
            prod_user.notificaciones = False
        else:
            prod_user.notificaciones = True
        prod_user.save()
        return Response('OK')
    return Response('NOT OK')

