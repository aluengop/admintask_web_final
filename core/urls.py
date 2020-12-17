from django.contrib import admin
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.home_view, name="home" ),
    path('index', views.index, name="index"),
    path('base', views.base, name="base"),
    path('inicio', views.inicio, name="inicio"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"), 
    path('informaciones', views.informaciones, name="informaciones"), 
    path('sobre', views.sobre, name="sobre"),
    path('mapa', views.mapa, name="mapa"),
]
