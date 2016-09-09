# -*- coding: utf-8 -*-
from django.shortcuts import render
from inscripcion.forms import (inscripcionForm)
from inscripcion.models import (inscripcion)
from django.contrib import messages
# Create your views here.

def vista_concepto(request,pk=None):
	form_class = inscripcionForm
	obj = None
	if pk is not None:
		obj = inscripcion.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		messages.success(request,"Se ha Guardado la información con éxito")
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'inscripcion'
	}
	return parametros