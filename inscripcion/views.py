# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from inscripcion.forms import (inscripcionForm)
from inscripcion.models import (inscripcion)
from catalogo.models import alumno,categoria,ciclo_escolar
from django.contrib import messages
# Create your views here.

def vista_inscripcion(request,pk=None):
  cat = categoria.objects.all()
  form_class = inscripcionForm
  obj = None
  maximo = 0
  cupo     = 0

  if pk is not None:
    obj = inscripcion.objects.get(pk=pk)
    cupo = obj.categoria.cupo_maximo
    alumnos   = inscripcion.objects.filter(categoria=obj.categoria)
    maximo  = len(alumnos)

  form = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.save()
    alumno.objects.filter(pk=obj.alumno.pk).update(ciclo_escolar=obj.ciclo)
    messages.success(request,"Se ha Guardado la información con éxito")

  catego   = categoria.objects.all()
  tmp_id_ins =[]
  for i in catego:
    tmp = inscripcion.objects.filter(categoria =i)
    if len(tmp) <= i.cupo_maximo:
      tmp_id_ins.append(i.pk)
    form.fields['categoria'].queryset = categoria.objects.filter(pk__in=tmp_id_ins)
  form.fields['ciclo'].queryset = ciclo_escolar.objects.filter(activo=True)

  operacion = request.POST.get('form_action',None)

  if operacion == 'SAVE_AND_OTHER':
    return redirect('crear',app='inscripcion',modelo='inscripcion')
  elif operacion == 'SAVE':
    if form.is_valid():
      return redirect('listar',app='inscripcion',modelo='inscripcion')

    
  parametros={
    'form'    : form,
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'inscripcion',
    'cupo'    : cupo,
    'maximo'  : maximo,
  }
  return parametros