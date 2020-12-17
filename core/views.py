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
import cx_Oracle

from .forms import ProcesoForm
from .models import Proceso
from .models import Tarea

from django.db import connections
import collections
import hashlib
# Create your views here.

def home_view( request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)

    return render(request, "paginainicial.html",{})

def index( request, *args, **kwargs):

    return render(request, "paginainicial.html",{})

   
def base( request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)

    return render(request, "base.html",{})

def inicio( request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)

    return render(request, "inicio.html",{})


def verificar_login(usuario, contrasena):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var (cx_Oracle.NUMBER)
    cursor.callproc('PK_USUARIO.SP_LOGIN', [usuario, contrasena, salida])

    return salida.getvalue()


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    data = {
                'mensaje' : ''
            }
    if request.method == "POST": 
        print(request.POST)
        #con = cx_Oracle.connect('admin', 'admintask' , 'admintaskv12.cwbq7zxlkbhk.us-east-1.rds.amazonaws.com:1521/ORCL')
        user = request.POST.get('username')
        passwd = request.POST.get('password')
        passwdEncriptada = hashlib.sha512(passwd.encode())

        cur = connections['default'].cursor()

        sql = "select rol_id_rol from usuario where rut = '{}' and clave = '{}'".format(user,passwdEncriptada.hexdigest())
        cur.execute(sql)
        res = cur.fetchall()
        rol = ''
        lista = []
        for dato in res:
            rol = dato[0]
            lista.append(rol)
        # Si el formulario es válido...

        if len(lista) > 0:
            if rol == 1: 
                username='admin'
                password='admin'
            elif rol == 2:
                username='diseñador de proceso'
                password='admin'
            else:
                username='funcionario'
                password='admin'
            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)
            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
               do_login(request, user)
                # Y le redireccionamos a la portada
            return redirect('iniciointerior')
        else:
            data['mensaje'] = 'Credenciales Erroneas'
    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'data': data})



def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('login')
    # Si queremos borramos los campos de ayuda
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form': form})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')


def informaciones( request, *args, **kwargs):

    return render(request, "informaciones.html",{})

def sobre( request, *args, **kwargs):

    return render(request, "sobre.html",{})

def mapa( request, *args, **kwargs):

    return render(request, "mapa.html",{})



