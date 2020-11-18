from django.shortcuts import render, redirect 
from django.http import HttpResponse
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


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'tracker/profile.html')

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
