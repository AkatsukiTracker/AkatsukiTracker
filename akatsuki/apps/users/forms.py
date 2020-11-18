from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = Usuario
		fields = ['username', 'email', 'password1', 'password2']
