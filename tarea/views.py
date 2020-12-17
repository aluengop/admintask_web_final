from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.shortcuts import render
from django.core.mail import send_mail

from django.views import generic
from django.db import connection
from django.db import models
import cx_Oracle

from django.db.models import Q
from core import models
from core.models import Tarea
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

def tarea(request):

    data = {
        'id_estado': listar_estado(),
        'id_funcion': listar_funcion(),
        'lista_encargado': listar_encargados(),
        'lista_usuarios': listar_usuarios(),
    }
        
    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        estado_id_estado = request.POST.get('Estado')
        funcion_id_funcion = request.POST.get('funcion_id_funcion')
        descripcion = request.POST.get('Descripcion')
        id_encargado = request.POST.get('id_encargado')
        id_usuario = request.POST.get('id_usuario')
        id_usuario2 = request.POST.get('id_usuario2')

        lista_usu_tar = [id_usuario, id_usuario2]
        tupla_usu_tar = (lista_usu_tar) 


        if request.POST["id_usuario"] == request.POST["id_usuario2"]:
            salida = agregar_tarea(nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, id_encargado, tupla_usu_tar)
        
        elif request.POST["id_encargado"] == request.POST["id_usuario"] != request.POST["id_usuario2"]:
	        salida = agregar_tarea(nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, id_encargado, tupla_usu_tar)
        
        elif request.POST["fecha_inicio"] < request.POST["fecha_termino"]:
	        salida = agregar_tarea(nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, id_encargado, tupla_usu_tar)
        else:
            salida = 2

        if salida == 1 :
            data['mensaje'] = 'Tarea agregada correctamente'
            messages.info(request, "Operación Exitosa!")
        elif salida == 2 :
            data['mensaje'] = 'Erro al completar los campos'
            messages.info(request, "Operación Fallida!")
	   
        else:
            data['mensaje'] = 'no se ha podido guardar la tarea'

        
    return render(request, "creartarea.html", data)

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

def listar_tarea():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TAREA", [out_cur])
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

def listar( request, *args, **kwargs):

    data = { 'tarea': listar_tarea()
    }
    data['tarea']=listar_tarea()

    return render(request, 'listartarea.html', data)

def listar_encargados():
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur = django_cursor.connection.cursor()
	
	cursor.callproc("SP_LISTAR_ENCARGADOS", [out_cur])
	lista_encargados = []
	for encargado in out_cur:
		lista_encargados.append(encargado)
	return lista_encargados

def listar_usuarios():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ENCARGADOS", [out_cur])
    lista_usuarios = []
    for usuario in out_cur:
        lista_usuarios.append(usuario)
    return lista_usuarios
 
def agregar_tarea(nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, encargado, tupla_usu_tar):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)    
    id_tarea = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('SP_CREAR_TAREA2',[nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, encargado, id_tarea])
    
    for elemento in tupla_usu_tar:
        cursor.callproc('SP_INSERTAR_USU_TAR2',[elemento, id_tarea, salida])
    return salida.getvalue()

def editartarea(request,id_tarea):
    tarea = [ u for u in listar_tarea() if u[0] == id_tarea ][0]
    fecha_inicio = tarea[2]
    fecha_inicio_str = "%s-%s-%s"%(fecha_inicio.strftime("%Y"),fecha_inicio.strftime("%m"),fecha_inicio.strftime("%d"))
    fecha_termino = tarea[3]
    fecha_termino_str = "%s-%s-%s"%(fecha_termino.strftime("%Y"),fecha_termino.strftime("%m"),fecha_termino.strftime("%d"))
    data = {
        'id_estado': listar_estado(),
        'id_funcion': listar_funcion(),
        'lista_encargado': listar_encargados(),
        'lista_usuarios': listar_usuarios(),
        'fecha_inicio_str': fecha_inicio_str,
        'fecha_termino_str': fecha_termino_str,
        'tarea': tarea,
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        estado_id_estado = request.POST.get('Estado')
        funcion_id_funcion = request.POST.get('funcion_id_funcion')
        descripcion = request.POST.get('Descripcion')
        id_encargado = request.POST.get('id_encargado')
       # id_usuario = request.POST.get('id_usuario')
       # id_usuario2 = request.POST.get('id_usuario2')

       # lista_usu_tar = [id_usuario, id_usuario2]
       # tupla_usu_tar = (lista_usu_tar) 

        print(id_tarea, nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, id_encargado )

        salida = actualizar_tarea(id_tarea, nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, id_encargado)
       
        if salida == 1 :
            data['mensaje'] = 'Tarea %s editada correctamente'%id_tarea
            messages.info(request, "Operación Exitosa!")
        else:
            data['mensaje'] = 'No se ha podido Editar la tarea '+str(id_tarea)
            messages.info(request, "Operación Fallida!")
    return render(request,'uptarea.html',data)

def actualizar_tarea (id_tarea, nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, encargado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    out_cur = django_cursor.connection.cursor()
    print(id_tarea, out_cur)
   # cursor.callproc('SP_BUSCAR_USUTAR', [id_tarea, out_cur])
    print(id_tarea, nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, encargado)
    cursor.callproc('SP_UPDATE_TAREA',[id_tarea, nombre, fecha_inicio, fecha_termino, estado_id_estado, funcion_id_funcion, descripcion, encargado, salida])
    
   # salida = 1
   # for elemento in out_cur:
   #     for usuario in tupla_usu_tar:
   #         print(elemento, usuario, id_tarea)
   #         cursor.callproc('SP_MODIFICAR_USU_TAR', [ elemento, usuario, id_tarea])
    return salida.getvalue()

def borrartarea(request, id_tarea):
    
    tarea = [ u for u in listar_tarea() if u[0] == id_tarea ][0]

    data = {
        'tarea': tarea,
    }
    if request.method == 'POST':
        salida = eliminartarea(id_tarea)
        if salida == 1 :
            data['mensaje'] = 'tarea %s eliminada correctamente'%id_tarea
            messages.info(request, "Operación Exitosa!")
        else:
            data['mensaje'] = 'No se ha podido eliminar la tarea '+str(id_tarea)
            messages.info(request, "Operación Fallida!")

    return render(request,'borrartarea.html',data)

def eliminartarea(id_tarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ELIMINAR_TAREA", [id_tarea, salida])
    cursor.callproc("SP_ELIMINAR_TAREA2", [id_tarea, salida])     
    return salida.getvalue()

def rescatarCorreo(id_tarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    
    cursor.callproc("SP_RESCATAR_CORREO", [id_tarea, salida])   
    return salida.getvalue()

def acciontarea(request, id_tarea):

    tarea = [ u for u in listar_tarea() if u[0] == id_tarea ][0]
    correo =  rescatarCorreo(tarea[0])

    data = {
        'tarea': tarea,
        'correo': correo,             
    }

    if request.method == "POST":
        message_asunto = request.POST['message_asunto']
        desc_mensaje = request.POST['desc_mensaje']
        message_email = request.POST['message_email']
        message = desc_mensaje

        idtarea = tarea[0]
        asunto = "ID: {} - Nombre: {} - {}".format(idtarea,tarea[1],message_asunto)

        message = '''Saludos desde Admintask, \n\n''' + tarea[1] + ' - ' + message_asunto + '\nDescripción: ' +  desc_mensaje + '''\n\nIngresa a Admintask para revisar ! 
        \nTambien puedes contactarte con nosotros en contacontacto@processsa.com
        \n\n\nAtentamente Admintask !!!'''

        send_mail(
            asunto,
            message,
            message_email,
            [correo],
            )
        messages.info(request, 'Mensaje enviado correctamente!')
        
            
        return render(request, 'acciontarea.html', data)
    else:
        
        return render(request, 'acciontarea.html',data)

def notificar(request, id_tarea):

    tarea = [ u for u in listar_tarea() if u[0] == id_tarea ][0]
    correo =  rescatarCorreo(tarea[0])

    data = {
        'tarea': tarea,
        'correo': correo,             
    }

    if request.method == "POST":
        message_asunto = request.POST['message_asunto']
        desc_mensaje = request.POST['desc_mensaje']
        message_email = request.POST['message_email']
        message = desc_mensaje
        

        idtarea = tarea[0]
        asunto = "ID: {} - Nombre: {} - {}".format(idtarea,tarea[1],message_asunto)

        message = '''Saludos desde Admintask, \n\n''' + tarea[1] + ' - ' + message_asunto + '\nDescripción: ' +  desc_mensaje + '''\n\nIngresa a Admintask para revisar ! 
        \nTambien puedes contactarte con nosotros en contacontacto@processsa.com
        \n\n\nAtentamente Admintask !!!'''

        send_mail(
            asunto,
            message,
            message_email,
            [correo],
            )
        messages.info(request, 'Mensaje enviado correctamente!')
            
        return render(request, 'notificar.html', data)
    else:
        
        return render(request, 'notificar.html',data)

def tareasatrasadas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_TAREA_VENCIDA", [out_cur])
    
    lista = []

    for fila in out_cur:
        lista.append(fila)
    return lista

def tareasxvencer():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_TAREA_X_EXPIRAR", [out_cur])
    
    lista = []

    for fila in out_cur:
        lista.append(fila)
    return lista

def cantatrasadas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc("SP_CANT_TAREA_VENCIDA", [salida])  
    return salida.getvalue()

def cantxvencer():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc("SP_CANT_POR_VENCER", [salida]) 
    return salida.getvalue()

def listartareasatrasadas(request):
    vencidas =  cantatrasadas()
    xvencer = cantxvencer()
    xvencer = myformat(xvencer)
    vencidas = myformat(vencidas)

    tamanoVencidas = len(tareasatrasadas())
    tamanoxVencer = len(tareasxvencer())
    
    data = {
        'list_vencidas':tareasatrasadas(),
        'list_xvencer':tareasxvencer(),
        'vencidas':vencidas,
        'xvencer':xvencer,
        'tamanoVencidas':tamanoVencidas,
        'tamanoxVencer':tamanoxVencer
        }
   
    return render(request, 'tareas_atrasadas.html', data)

def myformat(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')
    


def buscartarea(encargado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_TAREA_POR_ID", [encargado ,out_cur])
    
    buscar = []

    for fila in out_cur:
        buscar.append(fila)
    return buscar

def listartareaporid(request):
    encargado = request.GET.get('encargado')
    data = {
        
    }
    
    if request.method == "POST":
        
        encargado = request.POST['encargado']
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()
    
        cursor.callproc("SP_LISTAR_TAREA_POR_ID", [encargado ,out_cur])
    
        buscar = []

        for fila in out_cur:
            buscar.append(fila)

    return  render(request, 'buscarid.html', data )
