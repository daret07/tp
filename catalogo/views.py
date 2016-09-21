# -*- coding: utf-8 -*-
from django.shortcuts import render
from catalogo.forms import (conceptoForm,categoriaForm,alumnoForm,ciclo_escolarForm,personaForm,referenciaFormset)
from catalogo.models import (concepto,categoria,alumno,ciclo_escolar,persona,referencias)
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
    if len(obj.formula)>0:
      clave_tmp = obj.formula.split('*',2)
      clave_tmp[0] = clave_tmp[0].replace(' ','')
      concepto_tmp = concepto.objects.filter(clave__contains=clave_tmp[0])
      if concepto_tmp:
        obj.importe=float(concepto_tmp[0].importe) * float(clave_tmp[1])
        messages.success(request,"Se ha encontrado el concepto y se actualizo el importe")
      else:
        messages.error(request,"El concepto ingresado en la formula es incorrecto y/o no existe")    
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
  ref_p = False
  ref_u = False
  if pk is not None:
    obj = alumno.objects.get(pk=pk)
    mat = False
    tmp_ref = referencias.objects.filter(alumno=obj)
    if tmp_ref:
      for i in tmp_ref:
        if 'Principal' in i.descripcion:
          ref_p = True
        if 'Uniforme' in i.descripcion:
          ref_u = True


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
    matricula = str(time.strftime("%y"))+str(int(last.pk)+1).zfill(4)

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
    'matricula' : matricula,
    'principal' : ref_p,
    'uniforme'  : ref_u
  }
  return parametros