from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from apps.users.models import Usuario

class Tienda(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    dominio = models.URLField(unique=True)

    def __str__(self):
        return "Tienda: " + self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    link = models.URLField(max_length=255, unique=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    img_link = models.URLField(null=True)

    def get_link(self):
        return self.link

    def __str__(self):
        return "Producto: " + self.nombre

class Historial(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.IntegerField()
    bs4path = models.CharField(max_length=300, null=True)

    class Disponibilidad(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')

    disponible = models.IntegerField( choices=Disponibilidad.choices )

    def __str__(self):
        return "Historial:   tipo: " + self.tipo + ", fecha: " + str(self.fecha) + ", producto: " + self.producto.nombre

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

    def __str__(self):
        return "Usuario: " + self.user.username + ", Producto: " + self.producto.nombre
