from django.db import models


class User(models.Model):
    #id automatica
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, unique=True)
    password = models.CharField(max_length=256)
    
