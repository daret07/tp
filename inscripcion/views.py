# -*- coding: utf-8 -*-
from django.shortcuts import render
from inscripcion.forms import (inscripcionForm)
from inscripcion.models import (inscripcion)
from catalogo.models import alumno
from django.contrib import messages
# Create your views here.

def vista_inscripcion(request,pk=None):
	form_class = inscripcionForm
	obj = None
	if pk is not None:
		obj = inscripcion.objects.get(pk=pk)

	form = form_class(request.POST or None,instance=obj)

	if request.POST and form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		alumno.objects.filter(pk=obj.alumno.pk).update(ciclo_escolar=obj.ciclo)
		messages.success(request,"Se ha Guardado la información con éxito")

	if pk is None:
		inscripciones = inscripcion.objects.all()
		tmp_ids=[]
		for item in inscripciones:
			tmp_ids.append(item.alumno.pk)
		form.fields['alumno'].queryset = alumno.objects.exclude(pk__in=tmp_ids)
	else:
		form.fields['alumno'].queryset = alumno.objects.filter(pk=obj.alumno.pk)
	parametros={
		'form'    : form,
		'custom'	:	True,
		'obj'			: obj,	
		'modulo'	: 'inscripcion'
	}
	return parametros