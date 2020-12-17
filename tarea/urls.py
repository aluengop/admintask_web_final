from django.contrib import admin
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('tarea', views.tarea, name="tarea"),
    path('listartarea', views.listar, name="listartarea"),
    path('buscartarea', views.listartareaporid, name="buscartarea"),
    path('uptarea/<int:id_tarea>', views.editartarea, name="uptarea"),
    path('borrartarea/<int:id_tarea>', views.borrartarea , name="borrartarea"),
    path('acciontarea/<int:id_tarea>', views.acciontarea , name="email"),
    path('notificar/<int:id_tarea>', views.notificar , name="notificar"),
    path('tareas_atrasadas', views.listartareasatrasadas, name="tareas_atrasadas"),
     
]


