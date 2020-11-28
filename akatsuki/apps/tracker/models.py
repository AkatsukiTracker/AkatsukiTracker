from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from apps.users.models import Usuario

class Tienda(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    dominio = models.URLField(unique=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    img_link = models.URLField(null=True)

    def get_link(self):
        return self.link

class Historial(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.IntegerField()
    bs4path = models.CharField(max_length=200, null=True)

    class Disponibilidad(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')

    disponible = models.IntegerField( choices=Disponibilidad.choices )

class ProductoUsuario(models.Model):
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name='user',
        )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name='producto',
        )
