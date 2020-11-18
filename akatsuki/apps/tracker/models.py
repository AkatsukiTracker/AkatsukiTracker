from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import Usuario

class Tienda(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    dominio = models.URLField(unique=True)

class TiendaPrecios(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    bs4_path = models.CharField(max_length=200)

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)

    def get_link(self):
        return self.link

class Historial(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.IntegerField()

    class Disponibilidad(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')

    disponible = models.IntegerField( choices=Disponibilidad.choices )

class ProductoUsuario(models.Model):
    user = models.ForeignKey(Usuario, 
        on_delete=models.CASCADE,
        related_name='usuario',
        )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name='producto',
        )
