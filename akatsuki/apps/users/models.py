from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Usuario(User):
    img_perfil = models.ImageField(upload_to= "static/imgs_perfil/", null=True)

    class Notificaciones(models.IntegerChoices): #Notificaciones de productos Trending Semanales
        NO = 0, _('No')
        Si = 1, _('Si')
    notificaciones = models.IntegerField( choices=Notificaciones.choices, default=1)

