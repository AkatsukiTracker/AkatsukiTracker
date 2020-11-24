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
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'tracker/profile.html')

def check_url(request):
    tmpl_vars = {'form': CheckUrlForm()}
    return render(request, 'tracker/check_url.html', tmpl_vars)

@login_required(login_url='login')
@api_view(['GET','POST'])
def add_product(request, pk):
    if request.method == 'POST':
        pass

@api_view(['GET'])
def see_products(request, num=1):
    if request.method == 'GET':
        n = num * 10
        productos = Producto.objects.all()[n-10:n]
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

















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
