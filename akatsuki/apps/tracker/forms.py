from django.forms import ModelForm
from .models import *
from django import forms

class CheckUrlForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'

class ProductosForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'