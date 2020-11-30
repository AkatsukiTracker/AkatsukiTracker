from django.shortcuts import render
from django.contrib.auth.models import User

def home_view(request):
    if request.method == 'GET':
        if request.user.username != "":
          user = User.objects.filter(username=request.user.username)[0]
        else:
            user = False
        args = {"user": user}
        return render(request, "home/index.html", args)
    return render(request, "home/index.html")

def about_view(request):
    if request.method == 'GET':
        if request.user.username != "":
          user = User.objects.filter(username=request.user.username)[0]
        else:
            user = False
        args = {"user": user}
        return render(request, "about/index.html", args)
    return render(request, "about/index.html")

def contacto_view(request):
    if request.method == 'GET':
        if request.user.username != "":
          user = User.objects.filter(username=request.user.username)[0]
        else:
            user = False
        args = {"user": user}
        return render(request, "contacto/index.html", args)
    return render(request, "contacto/index.html")    
