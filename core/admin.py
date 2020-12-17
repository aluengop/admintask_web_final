from django.contrib import admin
from .models import Cliente, Estado, FunProc, Funcion, HistRep, HistTar, Proceso, Rol, Subtarea, Tarea, Unidad, UsuTar, Usuario
   
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Estado)
admin.site.register(FunProc)
admin.site.register(Funcion)
admin.site.register(HistRep)
admin.site.register(HistTar)
admin.site.register(Proceso)
admin.site.register(Rol)
admin.site.register(Subtarea)
admin.site.register(Tarea)
admin.site.register(Unidad)
admin.site.register(UsuTar)
admin.site.register(Usuario)
