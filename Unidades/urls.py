from django.contrib import admin
from . import views
from django.urls import path, re_path, include, reverse_lazy



urlpatterns = [
    path('listarunidades/', views.listarUnidades, name = "listar_unidades"),
    path('crearunidad/', views.crearUnidad, name = "crear_unidad"),
    path('editarunidad/<int:id_unidad>',views.editarUnidades, name= "editar_unidad"),
    path('borrarunidad/<int:id_unidad>',views.borrarUnidad, name= "borrar_unidad"),
    
    #Url inicial al logearse
    path('iniciointerior', views.iniciointerior, name = "iniciointerior"),

]
