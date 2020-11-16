from django.urls import path
from .views import TrackerView

urlpatterns = [
    path('tracker/', TrackerView.as_view()),
]