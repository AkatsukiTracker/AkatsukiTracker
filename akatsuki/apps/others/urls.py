from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view()),
    path('about/', AboutView.as_view()),
    path('contacto/', ContactoView.as_view()),
]
