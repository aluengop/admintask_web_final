from django.shortcuts import render
from django.views import generic
from django.db import connection
from datetime import date, datetime, timedelta

#from django.http import JsonResponse
import cx_Oracle

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def subtareas(request, *args, **kwargs):
    list_tareas = [ u for u in listar_tareas() ]
    f = date.today()
    data = {
        'lista_elementos': listar_tareas(),
        "fecha_actual" : "%s/%s/%s"%(f.strftime("%d"),f.strftime("%m"),f.strftime("%Y"))
    }
    if request.method == "POST":
        print(dict(request.POST))


    return render(request,"subtareas.html", data)
    #return JsonResponse(data)

def listar_tareas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cur_salida = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_TAREA2", [out_cur])

    listatareas = []
    for fila in out_cur:
        listatareas.append(fila)

    listasubtareas = listar_sub_tareas()
    
    listaElementos = []

    f = date.today()

    now = datetime.now()
    print('now: ', now)

    fec_actual = "%s/%s/%s"%(f.strftime("%d"),f.strftime("%m"),f.strftime("%Y"))
    
    print(fec_actual)
    semaforo = []
    for tarea in listatareas:
        dic = {}
        dic["tarea"] = tarea
        subtareas = []
        suma = 0

        #Datetime - Fecha de la tarea
        dateString = tarea[3]
        dateFormatter = "%d/%m/%Y"
        fecha_termino = datetime.strptime(dateString, dateFormatter)
        print('fecha de termino: ', fecha_termino)

        #Datetime - Semana anterior
        semana_anterior = datetime.strptime(dateString, dateFormatter) - timedelta(days=7)    
        print('semana_anterior: ', semana_anterior)

        if fecha_termino < datetime.strptime(fec_actual, dateFormatter):
            semaforo = 3
        elif semana_anterior <= datetime.strptime(fec_actual, dateFormatter) <= fecha_termino:
            semaforo = 2
        else:
            semaforo = 1

        for sub in listasubtareas:
            if sub[3] == tarea[0]:
                subtareas.append(sub)

                suma += int(sub[2])

        dic["sub_tareas"] = subtareas
        try:
            porcentaje = round(suma*100/len(subtareas),0)
        except ZeroDivisionError:
            porcentaje = 0
        
        listaElementos.append(dic)
        dic["progreso"] = str(porcentaje)+"%"
        dic["semaforo"] = semaforo



    return listaElementos

def listar_sub_tareas():
    '''
    Obtener una lista de subtareas desde la base de datos
    '''
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LISTAR_SUBTAREA", [out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def agregarsubtarea(request, id_tarea):
    data = { }

    if request.method == 'POST':
        nombre_subtarea = request.POST["nombre_subtarea"]
        
        salida = agregar_tarea_bd(id_tarea, nombre_subtarea)
        
        if salida == 1 :
            data['mensaje'] = 'Agregado correctamente'
            messages.info(request, 'Operación Exitosa!')
        else:
            data['mensaje'] = 'No se ha podido guardar'
            messages.info(request, 'No se ha podido guardar!')

    return render(request,"agregarsubtarea.html", data)

def agregar_tarea_bd (id_tarea, nombre_subtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc("SP_CREAR_SUBTAREA", [id_tarea, nombre_subtarea, salida])   
    print(id_tarea, nombre_subtarea, salida)
    return salida.getvalue()
    
def editarsubtarea(request, id_subtarea):
    subtarea = [ u for u in listar_sub_tareas() if u[0] == id_subtarea ][0]
    
    data = {
        'subtarea': subtarea,
    }

    if request.method == 'POST':
        nombre_subtarea = request.POST["nombre_subtarea"]
        estado_subtarea = request.POST["estado_subtarea"]
        salida = editar_subtarea(id_subtarea, nombre_subtarea, estado_subtarea)

        if salida == 1 :
            data['mensaje'] = 'Subtarea %s editada correctamente'%id_subtarea
            messages.info(request, 'Operación Exitosa!')
        else:
            data['mensaje'] = 'No se ha podido Editar la sub tarea '+str(id_subtarea)
            messages.info(request, 'No se ha podido Editar la sub tarea!')
            
    return render(request,"editarsubtarea.html", data)

def editar_subtarea(id_subtarea, nombre_subtarea, estado_subtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_MODIFICAR_SUBTAREA", [id_subtarea, nombre_subtarea, estado_subtarea, salida])   
    return salida.getvalue()

def eliminarsubtarea(request, id_subtarea):
    subtarea = [ u for u in listar_sub_tareas() if u[0] == id_subtarea ][0]
    
    data = {
        'subtarea': subtarea,
    }

    if request.method == 'POST':

        salida = eliminar_subtarea_bd(id_subtarea)

        if salida == 1 :
            data['mensaje'] = 'Subtarea %s eliminada correctamente'%id_subtarea
            messages.info(request, 'Subtarea eliminada correctamente exitosamente!')
        else:
            data['mensaje'] = 'No se ha podido eliminar la subtarea '+str(id_subtarea)
            messages.info(request, 'No se ha podido eliminar la subtarea!')
            
    return render(request,"eliminarsubtarea.html", data)

def eliminar_subtarea_bd(id_subtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ELIMINAR_SUBTAREA", [id_subtarea, salida])   
    return salida.getvalue()

def subtareasfiltro(request, id_tarea):



    return render(request,"subtareasfiltro.html")
    #return JsonResponse(data)