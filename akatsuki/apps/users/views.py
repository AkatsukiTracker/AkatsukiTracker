from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                messages.success(request, 'La cuenta fue creada para ' + username)
                '''
                send_mail(
                    'Cuenta Creada en AkatsukiTracker', #Titulo  
                    'Tu cuenta fue creada exitosamente en AkatsukiTracker, desde ahora puedes disfrutar bla bla....', #Mensaje
                    'akatsuki_tracker@mail.com', #Emisor
                    form.cleaned_data.get('email'), #Destinatario
                )
                '''
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('dashboard')
        context = {'form':form}
        return render(request, 'users/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Nombre de usuario o contraseña incorrecto')

        context = {}
        return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home/index.html', context)
