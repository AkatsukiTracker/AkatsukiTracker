from django.shortcuts import render
from django.contrib.auth.models import User
from apps.tracker.models import Tienda

def get_user(request):
    if request.user.username != "":
        user = User.objects.filter(username=request.user.username)[0]
    else:
        user = False
    return user

def home_view(request):
    user = get_user(request)
    args = {'tiendas':[], 'user':user}

    tiendas = Tienda.objects.all()
    for tienda in tiendas:
        args['tiendas'].append(tienda.nombre)

    return render(request, "home/index.html", args)

def about_view(request):
    user = get_user(request)
    args = {'user':user}
    return render(request, "home/about.html", args)

def contacto_view(request):
    user = get_user(request)
    args = {'user':user}
    return render(request, "home/contacto.html", args)

def error_400_view(request, exception):
    data = {}
    return render(request, "errors/400.html", data)

def error_403_view(request, exception):
    data = {}
    return render(request, "errors/403.html", data)

def error_404_view(request, exception):
    data = {}
    return render(request, 'errors/404.html', data)

def error_500_view(request):
    data = {}
    return render(request, "errors/500.html", data)

