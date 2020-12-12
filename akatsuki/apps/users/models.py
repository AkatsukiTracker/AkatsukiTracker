from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
    img_perfil = models.ImageField(upload_to= "static/imgs_perfil", null=True)

