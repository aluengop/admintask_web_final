from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout

from django.views import generic
from django.db import connection
from django.db.models import Q
import cx_Oracle
# Create your views here.

def listar_unidad():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_UNIDAD", [out_cur])
    listar = []
    for fila in out_cur:
        listar.append(fila)
    return listar


def listar_usuario():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_USUARIO", [out_cur])
    listar = []
    for fila in out_cur:
        listar.append(fila)
    return listar

def listar_estado():
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur = django_cursor.connection.cursor()
	
	cursor.callproc("SP_LISTAR_ESTADO", [out_cur])
	lista = []
	for fila in out_cur:
		lista.append(fila)
	return lista

def listar_funcion():
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur = django_cursor.connection.cursor()
	
	cursor.callproc("SP_LISTAR_FUNCION", [out_cur])
	lista = []
	for fila in out_cur:
		lista.append(fila)
	return lista


def listarFuncion( request, *args, **kwargs):
    data = { 'funcion': listar_funcion()}
    data['funcion']=listar_funcion()
    
    return render(request, 'listarfuncion.html', data)

def funcion(request):
    data = {
    'id_estado': listar_estado(),
    'id_unidad': listar_unidad(),
    'id_usuario': listar_usuario(),
     }

    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        unidad_id_unidad = request.POST.get('Unidad')
        estado_id_estado = request.POST.get('Estado')
        usuario_id_usuario = request.POST.get('Usuario')

        
        
        if request.POST["fecha_inicio"] < request.POST["fecha_termino"] :
            salida = agregar_funcion( nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario)
        else:
            salida = 2
        
        if salida == 1 :
            data['mensaje'] = 'agregado correctamente'
        elif salida == 2 :
            data['mensaje'] = 'Las fecha termino no puede ser antes que la fecha de inicio'
        else:
            data['mensaje'] = 'no se ha podido guardar'

    return render(request, 'agregarfuncion.html',data)


def agregar_funcion( nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_FUNCION',[ nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario, salida])
    return salida.getvalue()

def editarfuncion(request, id_funcion):

    funcion = [ u for u in listar_funcion() if u[0] == id_funcion ][0]
    fecha_inicio = funcion[2]
    fecha_inicio_str = "%s-%s-%s"%(fecha_inicio.strftime("%Y"),fecha_inicio.strftime("%m"),fecha_inicio.strftime("%d"))
    fecha_termino = funcion[3]
    fecha_termino_str = "%s-%s-%s"%(fecha_termino.strftime("%Y"),fecha_termino.strftime("%m"),fecha_termino.strftime("%d"))
    print(fecha_inicio_str)

    data = {
    'id_estado': listar_estado(),
    'id_unidad': listar_unidad(),
    'id_usuario': listar_usuario(),
    'funcion': funcion,
    'fecha_inicio_str': fecha_inicio_str,
    'fecha_termino_str': fecha_termino_str,
    }

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        unidad_id_unidad = request.POST.get('Unidad')
        estado_id_estado = request.POST.get('Estado')
        usuario_id_usuario = request.POST.get('Usuario')

        salida = editar_funcion(id_funcion,nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario)
        
        if salida == 1 :
            data['mensaje'] = 'funcion %s editado correctamente'%id_funcion
        else:
            data['mensaje'] = 'No se ha podido Editar el funcion '+str(id_funcion)

    return render(request, 'editarfuncion.html', data)


def editar_funcion(id_funcion, nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_MODIFICAR_FUNCION", [id_funcion, nombre, fecha_inicio, fecha_termino, unidad_id_unidad, estado_id_estado, usuario_id_usuario, salida])   
    return salida.getvalue()


def eliminarFunciones(request, id_funcion):
    
    funcion = [ u for u in listar_funcion() if u[0] == id_funcion ][0]

    data = {
        'funcion': funcion,
    }
    if request.method == 'POST':
        salida = eliminarFuncion(id_funcion)
        if salida == 1 :
            data['mensaje'] = 'Funcion %s eliminada correctamente'%id_funcion
        else:
            data['mensaje'] = 'No se ha podido eliminar la funcion'+str(id_funcion)

    return render(request,'borrarfuncion.html',data)


def eliminarFuncion(id_funcion):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ELIMINAR_FUNCION2", [id_funcion, salida])
    cursor.callproc("SP_ELIMINAR_FUNCION", [id_funcion, salida])

        
    return salida.getvalue()