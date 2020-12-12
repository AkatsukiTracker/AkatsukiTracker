from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
#imports raros que veré si se ocupan

#views, modelos y demases
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from apps.users.models import Usuario

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.tracker.models import *
from apps.tracker.forms import *
from apps.tracker.scrapers import *

import json
from django.core.serializers.json import DjangoJSONEncoder

from django.core.management.base import BaseCommand

class Command(BaseCommand):
  def handle(self, **options):
    tienda = Tienda.objects.filter(nombre='falabella')[0]

    producto = Producto(nombre = 'nombre', link = 'asdasd', tienda = tienda, img_link = 'none')
    producto.save()
