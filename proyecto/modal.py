# -*- coding:UTF-8 -*-
from proyecto.forms import taskCForm,taskForm,projectSForm,filetaskMForm
from bitacora.forms import regForm,bitForm,fileregForm,conclusionForm
from bitacora.models import registro,participante,bitacora
from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from proyecto.models import task,project,filetask
import datetime
from base.utilidades import enviar_email
 
def task_modal(request,pk=None):
	realizado = False

	if request.POST['pk'] is not None:
		obj = task.objects.get(pk=request.POST['pk'])
	else:
		obj = None

	form = taskCForm(request.POST or None,instance = obj)
	
	observacion = request.POST.get('observacion' or None)
	
	if observacion:
		if form.is_valid():
			obj = form.save(commit=False)
			obj.dead_line = datetime.datetime.now()
			obj.estatus = '2'
			obj.save()
			
			#enviar_email('Finaliza Tarea','Se termino '+str(obj.titulo)+'. Obervaciones: '+str(obj.observacion),'daret07@gmail.com',[obj.usuario.Superior.email])
			realizado = True

	parametros={
		'form'    	: form,
		'obj'     	: obj,
		'custom'  	: True,
		'realizado'	: realizado,
	}
	return parametros
	

def project_modal(request):
	realizado = False
	form = projectSForm()
	if len(request.POST) > 3:
		form = projectSForm(request.POST or None)
		if form.is_valid:
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.estatus = '1'
			obj.save()
			realizado = True
	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		:realizado
	}
	return parametros

def tarea_modal(request):
	realizado = False
	form = taskForm()
	if len(request.POST) > 3:
		form = taskForm(request.POST or None)
		if form.is_valid:
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.estatus = '1'
			obj.save()
			realizado = True
	if not request.user.is_superuser:
		form.fields['proyecto'].queryset = project.objects.filter(usuario=request.user.Superior)
	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado
	}
	return parametros

def bitacora_modal(request):
	realizado = False
	form = bitForm()
	if len(request.POST) > 3:
		form = bitForm(request.POST or None)
		if form.is_valid:
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.save()

			obj_p = participante.objects.filter(usuario=request.user,bitacora=obj)
			
			if len(obj_p)==0:
				obj_participante = participante(usuario=request.user,bitacora=obj)
				obj_participante.save()

			realizado = True
	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado
	}
	return parametros

def registro_modal(request):
	realizado = False
	form = regForm()

	if len(request.POST) > 3:
		form = regForm(request.POST or None)

		if form.is_valid:
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.save()
			realizado = True

	part = participante.objects.filter(usuario=request.user)
	arr_bit = []
	for item in part:
		if not item.bitacora.id in arr_bit:
			arr_bit.append(item.bitacora.id)

	form.fields['bitacora'].queryset = bitacora.objects.filter(id__in=arr_bit)

	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado
	}
	return parametros



def file_modal(request):
	pk = request.POST['pk']
	realizado = False
	form = filetaskMForm()
	if len(request.POST) > 3:
		form = filetaskMForm(request.POST, request.FILES or None)
		if form.is_valid:
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.proyecto = task.objects.get(pk=pk)
			obj.save()
			realizado = True

	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado,
	'pk'					: pk
	}
	return parametros

def filereg_modal(request):

	pk = request.POST['pk']

	realizado = False
	form = fileregForm()
	if len(request.POST) > 3:
		form = fileregForm(request.POST, request.FILES or None)
		if form.is_valid:
			obj = form.save(commit=False)
			obj.registro = registro.objects.get(pk=pk)
			obj.save()
			realizado = True

	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado,
	'pk'					: pk
	}
	return parametros	


def conclusion_modal(request):

	pk = request.POST['pk']

	realizado = False
	form = conclusionForm()
	if len(request.POST) > 3:
		form = conclusionForm(request.POST or None, instance=registro.objects.get(pk=pk))
		if form.is_valid:
			obj = form.save(commit=False)
			obj.capturado = True
			obj.hora_f = datetime.datetime.now()
			obj.save()
			realizado = True


	parametros={
	'form'				: form,
	'custom'			: True,
	'realizado'		: realizado,
	'pk'					: pk
	}
	return parametros	
