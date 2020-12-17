from django.contrib import admin
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('funcion', views.funcion, name="crear_funcion"),
    path('listarfuncion', views.listarFuncion, name="listar_funcion"),
    path('editarfuncion/<int:id_funcion>', views.editarfuncion, name="editar_funcion"),
    path('borrarfuncion/<int:id_funcion>', views.eliminarFunciones, name = "borrar_funcion")
     
]

