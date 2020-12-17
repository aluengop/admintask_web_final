
#from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_rol = models.FloatField(default=False)
    is_usuario = models.FloatField(default=False)

    def get_rol_profile(self):
        rol_profile = None
        if hasattr(self, 'rolprofile'):
            rol_profile = self.rolprofile
        return rol_profile

    def get_usuario_profile(self):
        usuario_profile = None
        if hasattr(self, 'usuarioprofile'):
            usuario_profile = self.usuarioprofile
        return usuario_profile

    class Meta:
        db_table = 'auth_user'


class Rol(models.Model):
    id_rol = models.FloatField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'

class Usuario(models.Model):
    id_usuario = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50, blank=True, null=True)
    rut = models.FloatField(blank=True, null=True)
    digv = models.CharField(max_length=1, blank=True, null=True)
    correo = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.FloatField(blank=True, null=True)
    activo = models.FloatField(blank=True, null=True)
    rol_id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='rol_id_rol')
    clave = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
