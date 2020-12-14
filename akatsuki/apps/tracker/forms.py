from django.forms import ModelForm
from .models import *
from django import forms
from apps.users.models import Usuario

class CheckUrlForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'

class ProductosForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'

class ImgPerfilForm(ModelForm):
	class Meta:
		model = Usuario
		fields = ("img_perfil", )
