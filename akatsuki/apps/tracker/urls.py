from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile"),
    path('add_product/', views.add_product, name="add_product"),
    path("check_url/", views.check_url, name="check_url"),

    path("trending/", views.trending, name="trending"),
    path('trending/pagina=<int:num>', views.trending),
    path('trending/fecha=<str:fecha>', views.trending),
    path('trending/pagina=<int:num>_fecha=<str:fecha>', views.trending),

    path("check_product_info", views.check_info, name="check_info"),
    path("delete_product/", views.delete_product, name="delete_product"),

    path("profile_picture", views.profile_picture, name="profile_picture"),
    path("change_password", views.change_password, name="change_password"),
    path("change_email", views.change_email, name="change_email"),
    path("notif_trending", views.change_notif_trending, name="notif_trending"),
    path("notif_product_all", views.change_notif_prod_all, name="notif_product_all"),
    path("notif_product", views.change_notif_prod, name="notif_product"),

]
