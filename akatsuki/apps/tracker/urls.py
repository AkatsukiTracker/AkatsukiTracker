from django.urls import path
from . import views
#from apps.users.views import  #add_product

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile")
    #path('add_product/',add_product, name="add_product" )
]
