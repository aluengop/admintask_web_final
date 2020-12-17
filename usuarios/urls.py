from django.contrib import admin
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('login2', views.inicio_sesion, name="login2"),
  
     
]

