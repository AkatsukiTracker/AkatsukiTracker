from django.urls import path
from .views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view()),
    path('about/', AboutView.as_view()),
]
