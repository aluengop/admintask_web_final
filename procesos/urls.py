from django.contrib import admin
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.urls import reverse_lazy


urlpatterns = [
    path('proceso', views.proceso, name="crear_procesos"),
    path('listarprocesos/', views.listarProcesos, name = "listar_procesos"),
    path('editarproceso/<int:id_proceso>', views.editarProcesos, name = "editar_proceso"),
    path('borrarproceso/<int:id_proceso>', views.eliminarProcesos, name = "borrar_proceso"),
    path('funproc/<int:id_proceso>', views.listarFunProcesos, name = "listar_funproc")
    
     
]