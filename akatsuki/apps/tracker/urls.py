from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile"),
    path('add_product/', views.add_product, name="add_product"),
    path("check_url/", views.check_url, name="check_url"),
    path("trending/", views.trending, name="trending")
]
