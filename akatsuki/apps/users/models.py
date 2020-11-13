from django.db import models


class User(models.Model):
    #id automatica
    email = models.EmailField(blank=True, unique=True)
    password = models.CharField(max_length=256)
    
