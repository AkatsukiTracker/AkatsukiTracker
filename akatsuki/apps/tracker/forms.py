from django.forms import ModelForm
from .models import ProductoUsuario
from django import forms

class AddProductForm(ModelForm):
	class Meta:
		model = ProductoUsuario
		fields = '__all__'

