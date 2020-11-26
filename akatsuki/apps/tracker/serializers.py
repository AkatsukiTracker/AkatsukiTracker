from rest_framework import serializers
from .models import *

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ('nombre')

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = ('precio', 'disponible')

class ProductoSerializer(serializers.ModelSerializer):

    tienda = serializers.CharField()

    precios = serializers.DictField(child=serializers.JSONField())
    paths = serializers.DictField(child=serializers.JSONField())

    class Meta:
        model = Producto
        fields = ('nombre', 'link')
        
class TodoSerializer(serializers.Serializer):

    tienda = TiendaSerializer()
    historial = HistorialSerializer()
    producto = ProductoSerializer

class CheckUrlSerializer(serializers.Serializer):

    link = serializers.URLField()

    tipo_precio = serializers.CharField()
    precio = serializers.CharField()
    
    nombre = serializers.CharField()

    tienda = serializers.CharField()

    tipo_precio_path = serializers.CharField()
    path = serializers.CharField()
