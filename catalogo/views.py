# -*- coding: utf-8 -*-
from django.shortcuts import render
from catalogo.forms import (conceptoForm,categoriaForm,alumnoForm,ciclo_escolarForm)
from catalogo.models import (concepto,categoria,alumno,ciclo_escolar)
from django.contrib import messages
# Create your views here.

def vista_concepto(request,pk=None):
	form_class = conceptoForm
	obj = None
	if pk is not None:
		obj = concepto.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		messages.success(request,"Se ha Guardado la información con éxito")
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'concepto'
	}
	return parametros

def vista_ciclo_escolar(request,pk=None):
	form_class = ciclo_escolarForm
	obj = None
	if pk is not None:
		obj = ciclo_escolar.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		messages.success(request,"Se ha Guardado la información con éxito")
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'categoria'
	}
	return parametros

def vista_categoria(request,pk=None):
	form_class = categoriaForm
	obj = None
	if pk is not None:
		obj = categoria.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		messages.success(request,"Se ha Guardado la información con éxito")
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'categoria'
	}
	return parametros

def vista_alumno(request,pk=None):
	form_class = alumnoForm
	obj = None
	if pk is not None:
		obj = alumno.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		messages.success(request,"Se ha Guardado la información con éxito")
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'categoria'
	}
	return parametros