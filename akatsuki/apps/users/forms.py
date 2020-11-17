from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario#, ProductoUsuario
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = Usuario
		fields = ['username', 'email', 'password1', 'password2']
'''		
class AddProductForm(ModelForm):
	class Meta:
		model = ProductoUsuario
		fields = ['link']
'''
