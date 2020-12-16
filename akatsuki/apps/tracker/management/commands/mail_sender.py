from django.conf import settings 
from django.core.mail import send_mail 

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
    '''
    subject = 'MAIL TEST'
    message = f'Este es un msg de prueba'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = ['vicente.figueroa@usm.cl'] 
    send_mail( subject, message, email_from, recipient_list ) 
    '''
    historial1 = Historial.objects.all()[0]
    historial2 = Historial.objects.all()[::-1][0]

    print(historial1.fecha)
    print(historial2.fecha)
    