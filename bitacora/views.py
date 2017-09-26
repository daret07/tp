# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from bitacora.forms import bitacoraForm,participanteFormset,registroForm
from bitacora.models import bitacora,participante
from proyecto.models import project
from usuario.models import usuario

# Create your views here.
def vista_bitacora(request,pk=None):
	
	if pk is not None:
		obj = bitacora.objects.get(pk=pk)
	else:
		obj = None

	form = bitacoraForm(request.POST or None,instance=obj)
	form_participante = participanteFormset(request.POST or None,instance=obj)

	if request.POST:
		operacion = request.POST['form_action']
		if form.is_valid():
			obj = form.save(commit = False)
			obj.usuario = request.user
			obj.save()

			form_participante = participanteFormset(request.POST or None,instance=obj)
			if form_participante.is_valid():
				form_participante.save()

			obj_p = participante.objects.filter(usuario=request.user,bitacora=obj)
			perfil = request.user.groups.filter(name='Gerente')
			if not perfil:
				if len(obj_p)==0:
					obj_participante = participante(usuario=request.user,bitacora=obj)
					obj_participante.save()

			if operacion == 'SAVE_AND_OTHER':
				return redirect('crear',app='bitacora',modelo='bitacora')
			elif operacion == 'SAVE':
				if form.is_valid():
					return redirect('listar',app='bitacora',modelo='bitacora')

	for item in form_participante:
		item.fields['usuario'].queryset = usuario.objects.filter(Superior = request.user)

	if request.user.groups.filter(name='CabezaDpto'):
		form.fields['proyecto'].queryset = project.objects.filter(usuario=request.user)

	parametros = {
	'form'	:form,
	'form_p': form_participante,
	'obj'		: obj,
	'custom': True
	}
	return parametros


def vista_registro(request,pk=None):

	if pk is not None:
		obj = bitacora.objects.get(pk=pk)
	else:
		obj = None

	form = registroForm(request.POST or None,instance=obj)
	if request.POST:
		operacion = request.POST['form_action']
		if form.is_valid():
			obj = form.save(commit = False)
			obj.usuario = request.user
			obj.save()

			if operacion == 'SAVE_AND_OTHER':
				return redirect('crear',app='bitacora',modelo='registro')
			elif operacion == 'SAVE':
				if form.is_valid():
					return redirect('listar',app='bitacora',modelo='registro')

	ids = participante.objects.filter(usuario=request.user)
	
	arr_ids = []

	for i in ids:
		arr_ids.append(i.bitacora.id)

	form.fields['bitacora'].queryset = bitacora.objects.filter(id__in = arr_ids)
	print obj
	parametros = {
	'form'	:form,
	'obj'		: obj,
	'custom': True
	}
	return parametros
