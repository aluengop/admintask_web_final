from django.shortcuts import render
from django.views import generic
from django.db import connection
import cx_Oracle
# Create your views here.

def iniciointerior(request):
    
    return render(request, "inicio-interior.html")


def crearUnidad(request):
    data = { 'lista_clientes':listar_clientes()}

    if request.method == 'POST':
        nombre_departamento = request.POST["nombre_departamento"]
        id_cliente = request.POST["id_cliente"]
        print(nombre_departamento,id_cliente)
        
        salida = agregar_unidad(nombre_departamento, id_cliente)
        
        if salida == 1 :
            data['mensaje'] = 'agregado correctamente'
        else:
            data['mensaje'] = 'no se ha podido guardar'        

    return render(request, "crearunidad.html", data)

def editarUnidades(request, id_unidad):
    
    unidad = [ u for u in listar_unidad() if u[0] == id_unidad ][0]

    data = {
        'unidad': unidad,
        'lista_clientes': listar_clientes() 
    }

    if request.method == 'POST':
        nombre_departamento = request.POST["nombre_departamento"]
        id_cliente = request.POST["id_cliente"]
        salida = editarUnidad(id_unidad, nombre_departamento, id_cliente)
        if salida == 1 :
            data['mensaje'] = 'Unidad %s editada correctamente'%id_unidad
        else:
            data['mensaje'] = 'No se ha podido Editar la unidad '+str(id_unidad)
        
    return render(request,'editarunidad.html',data)

def editarUnidad(id_unidad, nombre_departamento, id_cliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_MODIFICAR_UNIDAD", [id_unidad, nombre_departamento, id_cliente, salida])   
    return salida.getvalue()
    
def borrarUnidad(request, id_unidad):
    
    unidad = [ u for u in listar_unidad() if u[0] == id_unidad ][0]

    data = {
        'unidad': unidad,
    }
    if request.method == 'POST':
        salida = eliminarUnidad(id_unidad)
        if salida == 1 :
            data['mensaje'] = 'Unidad %s eliminada correctamente'%id_unidad
        else:
            data['mensaje'] = 'No se ha podido eliminar la unidad '+str(id_unidad)

    return render(request,'borrarunidad.html',data)


def eliminarUnidad(id_unidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ELIMINAR_UNIDAD", [id_unidad, salida])   
    return salida.getvalue()

def listarUnidades(request,  *args, **kwargs):
    data = {
        'lista_unidades':listar_unidad(),
        'lista_clientes':listar_clientes(), }

    return render(request, "listarunidades.html", data)

def listar_unidad():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_UNIDADES", [out_cur])
    lista_unidades = []

    for unidad in out_cur:
        lista_unidades.append(unidad)
    return lista_unidades
        
def listar_clientes():
	django_cursor = connection.cursor()
	cursor = django_cursor.connection.cursor()
	out_cur = django_cursor.connection.cursor()
	
	cursor.callproc("SP_LISTAR_CLIENTES", [out_cur])
	lista_clientes = []
	for cliente in out_cur:
		lista_clientes.append(cliente)
	return lista_clientes


def agregar_unidad(nombre_departamento, id_cliente):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_UNIDAD',[nombre_departamento, id_cliente, salida])
    return salida.getvalue()
