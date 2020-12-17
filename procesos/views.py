from django.shortcuts import render
from django.views import generic
from django.db import connection
import cx_Oracle
# Create your views here.

def listar_funcion():
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur = django_cursor.connection.cursor()
	
	cursor.callproc("SP_LISTAR_FUNCION", [out_cur])
	lista = []
	for fila in out_cur:
		lista.append(fila)
	return lista

def agregar_proceso(nombre,descripcion,dias_inter, tupla_fun_proc):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    '''cursor.callproc('SP_CREAR_PROCESO',[nombre, descripcion, dias_inter, T_NUMBER_ARRAY(tupla_fun_proc), salida])'''
    
    id_proceso = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_PROCESO2',[nombre, descripcion, dias_inter, id_proceso])
    
    for elemento in tupla_fun_proc:
        cursor.callproc('SP_INSERTAR_FUN_PROC2',[elemento, id_proceso, salida])
    return salida.getvalue()



def proceso(request):
    data = { 'listar_funcion':listar_funcion()}

    if request.method == 'POST':
        nombre_proceso = request.POST["nombre_proceso"]
        descripcion_proceso = request.POST["descripcion_proceso"]
        dias_inter = request.POST["dias_inter"]
        funcion_id_funcion = request.POST["funcion_id_funcion"]
        funcion_id_funcion2 = request.POST["funcion_id_funcion2"]
        '''print(nombre_proceso,descripcion_proceso)'''
        lista_fun_proc = [funcion_id_funcion, funcion_id_funcion2]
        tupla_fun_proc = (lista_fun_proc)
        
        print(tupla_fun_proc)

        if request.POST["funcion_id_funcion"] != request.POST["funcion_id_funcion2"] :
            salida = agregar_proceso(nombre_proceso, descripcion_proceso,dias_inter, tupla_fun_proc)
        else:
            salida = 2
        
        if salida == 1 :
            data['mensaje'] = 'Proceso agregado correctamente'
        elif salida == 2 :
            data['mensaje'] = 'Las funciones seleccionadas deben ser distintas'  
        else:
            data['mensaje'] = 'no se ha podido guardar'       

    return render(request, "crearproceso.html", data)

def listarProcesos(request,  *args, **kwargs):
    data = {
        'lista_procesos':listar_procesos(), }

    return render(request, "listarproceso.html", data)

    
def listar_procesos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LPROCESS", [out_cur])
    

    lista_procesos = []
    
    for proceso in out_cur:
        lista_procesos.append(proceso)
        
    return lista_procesos


def listar_fun_proc(id_proceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    
    cursor.callproc("SP_LP_FUNCION", [id_proceso, out_cur])
    
    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista


def listarFunProcesos(request, id_proceso):
    data = {
        'proceso': id_proceso,
        'lista': listar_fun_proc(id_proceso),
        'listar_funcion':listar_funcion()}

    if request.method == 'POST':
        funcion = request.POST.get('funcion',False)
        salida = agregarFuncion(id_proceso, funcion)

        
        if salida == 1 :
            data['mensaje'] = 'Funcion agregada correctamente al proceso %s '%id_proceso
        else:
            data['mensaje'] = 'No se ha podido agregar la funcion '+str(id_proceso)

    return render(request, "listarfuncionproceso.html", data)


def agregarFuncion(id_proceso, funcion):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_INSERTAR_FUN_PROC2", [funcion,id_proceso, salida])

    return salida.getvalue()



def editarProcesos(request, id_proceso):

    proceso = [ p for p in listar_procesos() if p[0] == id_proceso ][0]

    data = {
        'proceso': proceso,
        'lista_procesos': listar_procesos() 
    }

    if request.method == 'POST':
        nombre_proceso = request.POST["nombre_proceso"]
        descripcion_proceso = request.POST["descripcion_proceso"]
        dias_inter = request.POST["dias_inter"]
        
        salida = editarProceso(id_proceso, nombre_proceso, descripcion_proceso, dias_inter)
        if salida == 1 :
            data['mensaje'] = 'Proceso %s editado correctamente'%id_proceso
        else:
            data['mensaje'] = 'No se ha podido Editar el proceso '+str(id_proceso)
        
    return render(request,'editarproceso.html',data)

    
def editarProceso(id_proceso, nombre_proceso, descripcion_proceso, dias_inter):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_MODIFICAR_PROCESO", [id_proceso, nombre_proceso, descripcion_proceso, dias_inter, salida])   
    return salida.getvalue()


def eliminarProcesos(request, id_proceso):
    
    proceso = [ u for u in listar_procesos() if u[0] == id_proceso ][0]

    data = {
        'proceso': proceso,
    }
    if request.method == 'POST':
        salida = eliminarProceso(id_proceso)
        if salida == 1 :
            data['mensaje'] = 'Proceso %s eliminado correctamente'%id_proceso
        else:
            data['mensaje'] = 'No se ha podido eliminar el proceso '+str(id_proceso)

    return render(request,'borrarproceso.html',data)


def eliminarProceso(id_proceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ELIMINAR_PROCESO", [id_proceso, salida])
    cursor.callproc("SP_ELIMINAR_PROCESO2", [id_proceso, salida])     
    return salida.getvalue()



