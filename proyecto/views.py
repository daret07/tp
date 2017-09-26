# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from proyecto.forms import projectForm,taskFormset,fileFormset,taskForm
from proyecto.models import project,task
from django.contrib import messages
from bitacora.models import bitacora,registro
from usuario.models import usuario
from base.utilidades import enviar_email
# Create your views here.

def main_index(request):
	jefe = False

	if request.user.groups.filter(name='CabezaDpto'):
		jefe = True
		
	elif request.user.groups.filter(name='Gerente'):
		jefe = True
	

	# BITACORA
	if request.user.is_superuser:
		reg = registro.objects.filter(capturado=False)
	elif request.user.groups.filter(name='Gerente'):
		reg = registro.objects.filter(capturado=False)
	elif request.user.groups.filter(name='CabezaDpto'):
		ids = usuario.objects.filter(Superior=request.user)
		arr_dis = []
		for i in ids:
			arr_dis.append(i.id)
		reg = registro.objects.filter(usuario__id__in=arr_dis,capturado=False)
	else:
		reg = registro.objects.filter(usuario=request.user,capturado=False)
	
	# PROYECTOS
	if request.user.groups.filter(name='Personal'):
		taskP = task.objects.filter(usuario=request.user,estatus='1').order_by('proyecto')
	elif request.user.groups.filter(name='Gerente'):
		taskP = task.objects.filter(estatus='1')
	elif request.user.groups.filter(name='CabezaDpto'):
		ids = usuario.objects.filter(Superior=request.user)
		arr_id = []
		for i in ids:
			arr_id.append(i.id)
			taskP = task.objects.filter(usuario__in=arr_id,estatus='1').order_by('proyecto')


	parametros = {
	'task':taskP,
	'permiso':jefe,
	'regi':reg,
	}
	return parametros

def vista_project(request,pk=None):

	if pk is not None:
		obj = project.objects.get(pk=pk)
	else:
		obj = None

	form = projectForm(request.POST or None,instance=obj)
	task_form = taskFormset(request.POST or None,instance=obj)
	file_form = fileFormset(request.POST or None,request.FILES or None,instance=obj)

	if request.POST:
		operacion = request.POST['form_action']
		if form.is_valid():
			obj = form.save(commit = False)
			obj.usuario=(request.user)
			obj.save()
			
			arr_correo = []
			task_form = taskFormset(request.POST or None,instance=obj)
			if task_form.is_valid():
				obj_task = task_form.save()
				task_form = taskFormset(instance=obj)

				for item in obj_task:
					if item.usuario.email not in arr_correo:
						arr_correo.append(item.usuario.email)
			
			else:
				print task_form.errors
			
			file_form = fileFormset(request.POST or None,request.FILES or None,instance=obj)
			if file_form.is_valid():
				obj_file = file_form.save()

				file_form = fileFormset(instance=obj)
			
			#enviar_email('Asignacion de tarea','Se te asignaron Tareas nuevas en el proyecto '+str(obj.titulo),'daret07@gmail.com',arr_correo)
			messages.success(request,"Se ha Guardado la información con éxito")

		if operacion == 'SAVE_AND_OTHER':
			return redirect('crear',app='proyecto',modelo='project')
		elif operacion == 'SAVE':
			if form.is_valid():
				return redirect('listar',app='proyecto',modelo='project')
	perfil = request.user.groups.filter(name='Gerente')
	if not perfil:
		for item in task_form:
			item.fields["usuario"].queryset = usuario.objects.filter(Superior=request.user)


	parametros = {
	'form': form,
	'obj':obj,
	'form_task':task_form,
	'form_file':file_form,
	}
	return parametros

def listado_task(request):
	parametros = {}
	return parametros

def vista_task(request,pk=None):
	
	if pk is not None:
		obj = task.objects.get(pk=pk)
	else:
		obj = None

	form = taskForm(request.POST or None,instance=obj)

	if request.POST:
		operacion = request.POST['form_action']
		if form.is_valid():
			obj = form.save(commit = False)
			obj.usuario = request.user
			obj.estatus = '1'
			obj.save()
	perfil = request.user.groups.filter(name='Gerente')
	if not perfil:
		form.fields['proyecto'].queryset = project.objects.filter(usuario=request.user.Superior)
	parametros = {
	'form'	:form,
	'obj'		: obj,
	'custom': True
	}
	return parametros




