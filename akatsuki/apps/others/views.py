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
    return render(request, "home/about.html")

def contacto_view(request):
    return render(request, "home/contacto.html")
   




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

