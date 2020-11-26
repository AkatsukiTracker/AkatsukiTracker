from django.urls import path, re_path
#from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile"),
    path('add_product/', views.add_product, name="add_product"),
    path("check_url/", views.check_url, name="check_url"),
    #path('trending/', views.see_products, name='see_products'),
    #path('trending/page<int:num>', views.see_products, name='see_products'),
]

'''
patterns(
"views",
url(r"^api/$", "check_url"),

#api
url(r'^api/v1/productos/(?P<pk>[0-9]+)$', 'see_products'),
)
'''
