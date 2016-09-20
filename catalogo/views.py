# -*- coding: utf-8 -*-
from django.shortcuts import render
from catalogo.forms import (conceptoForm,categoriaForm,alumnoForm,ciclo_escolarForm,personaForm,referenciaFormset)
from catalogo.models import (concepto,categoria,alumno,ciclo_escolar,persona)
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
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'concepto'
  }
  return parametros


def vista_persona(request,pk=None):
  form_class = personaForm
  obj = None

  if pk is not None:
    obj = persona.objects.get(pk=pk)

  form = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.save()
    messages.success(request,"Se ha Guardado la información con éxito")

  parametros={
    'form'    : form,
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'concepto'
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
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'categoria'
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
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'categoria'
  }
  
  return parametros

def vista_alumno(request,pk=None):
  import time
  form_class = alumnoForm
  obj = None
  mat = True
  matricula = ''
  if pk is not None:
    obj = alumno.objects.get(pk=pk)
    mat = False

  form = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.save()
    referencia_formset = referenciaFormset(request.POST or None,instance=obj)
    if referencia_formset.is_valid():
      referencia_formset.save()
      messages.success(request,"Se ha Guardado la información con éxito")

  if mat:
    last = alumno.objects.all().last()
    matricula = str(time.strftime("%y"))+str(int(last.pk)+1).zfill(2)
    
  referencia_formset = referenciaFormset(request.POST or None,instance=obj)
  if pk is None:
    form.fields['padre'].queryset = persona.objects.none()
    form.fields['emergencia'].queryset = persona.objects.none()
  else:
    form.fields['padre'].queryset = persona.objects.filter(pk=int(obj.padre.pk))
    form.fields['emergencia'].queryset = persona.objects.filter(pk=int(obj.emergencia.pk))
  parametros={
    'form'      : form,
    'form_req'  : referencia_formset,
    'custom'    : True,
    'obj'       : obj,  
    'modulo'    : 'categoria',
    'matricula' : matricula
  }
  return parametros