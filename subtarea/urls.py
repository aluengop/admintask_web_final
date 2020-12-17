from django.contrib import admin
from . import views
from django.urls import path, re_path, include, reverse_lazy



urlpatterns = [
    path('subtareas/', views.subtareas, name = "subtareas"),
    path('agregar_subtarea/<int:id_tarea>', views.agregarsubtarea, name = "agregar_subtarea"),
    path('editar_subtarea/<int:id_subtarea>', views.editarsubtarea, name = "editar_subtarea"),
    path('eliminarsubtarea/<int:id_subtarea>', views.eliminarsubtarea, name = "eliminarsubtarea"),
    path('subtareasfiltro/<int:id_tarea>', views.subtareasfiltro, name = "subtareasfiltro"),
]