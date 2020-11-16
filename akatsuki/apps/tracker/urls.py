from django.urls import path
from .views import TrackerView, HomeView

urlpatterns = [
    path('tracker/', TrackerView.as_view()),
    path('home/', HomeView.as_view()),
]