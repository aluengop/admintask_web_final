# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cliente(models.Model):
    id_cliente = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.FloatField(blank=True, null=True)
    correo = models.CharField(max_length=50, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    area_actuacion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estado(models.Model):
    id_estado = models.FloatField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'


class FunProc(models.Model):
    id_fun_proc = models.FloatField(primary_key=True)
    funcion_id_funcion = models.ForeignKey('Funcion', models.DO_NOTHING, db_column='funcion_id_funcion')
    proceso_id_proceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='proceso_id_proceso')

    class Meta:
        managed = False
        db_table = 'fun_proc'


class Funcion(models.Model):
    id_funcion = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_termino = models.DateField(blank=True, null=True)
    unidad_id_unidad = models.ForeignKey('Unidad', models.DO_NOTHING, db_column='unidad_id_unidad')
    estado_id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')
    usuario_id_usuario = models.FloatField()

    class Meta:
        managed = False
        db_table = 'funcion'


class HistRep(models.Model):
    id_hist_rep = models.FloatField(primary_key=True)
    fecha_solicitud = models.DateField(blank=True, null=True)
    archivo = models.TextField(blank=True, null=True)  # This field type is a guess.
    cliente_id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_id_cliente')
    usuario_id_usuario = models.FloatField()

    class Meta:
        managed = False
        db_table = 'hist_rep'


class HistTar(models.Model):
    id_hist_tar = models.FloatField(primary_key=True)
    estado_inicial = models.CharField(max_length=50, blank=True, null=True)
    estado_final = models.CharField(max_length=50, blank=True, null=True)
    tarea_id_tarea = models.ForeignKey('Tarea', models.DO_NOTHING, db_column='tarea_id_tarea')
    nota = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hist_tar'


class Proceso(models.Model):
    id_proceso = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proceso'


class Rol(models.Model):
    id_rol = models.FloatField(primary_key=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class Subtarea(models.Model):
    id_subtarea = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    finalizado = models.CharField(max_length=1, blank=True, null=True)
    tarea_id_tarea = models.ForeignKey('Tarea', models.DO_NOTHING, db_column='tarea_id_tarea')

    class Meta:
        managed = False
        db_table = 'subtarea'


class Tarea(models.Model):
    id_tarea = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_termino = models.DateField(blank=True, null=True)
    estado_id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')
    funcion_id_funcion = models.ForeignKey(Funcion, models.DO_NOTHING, db_column='funcion_id_funcion')
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    encargado = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarea'


class Unidad(models.Model):
    id_unidad = models.FloatField(primary_key=True)
    nombre_departamento = models.CharField(max_length=50, blank=True, null=True)
    cliente_id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_id_cliente')

    class Meta:
        managed = False
        db_table = 'unidad'


class UsuTar(models.Model):
    id_usu_tar = models.FloatField(primary_key=True)
    tarea_id_tarea = models.ForeignKey(Tarea, models.DO_NOTHING, db_column='tarea_id_tarea', blank=True, null=True)
    usuario_id_usuario = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usu_tar'


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
