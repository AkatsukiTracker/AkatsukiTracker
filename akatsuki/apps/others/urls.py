from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('contacto/', contacto_view, name="contacto"),
    path('tiendas/', tiendas_view, name="tiendas"),
]
