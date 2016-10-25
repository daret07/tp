# -*- coding: utf-8 -*-
from django.shortcuts import render
from catalogo.forms import (conceptoForm,categoriaForm,alumnoForm,ciclo_escolarForm,personaForm,referenciaFormset,descuentoFormset)
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
    operario = 0
    if len(obj.formula)>0:
      if len(obj.formula.split('*',2))>1:
        clave_tmp = obj.formula.split('*',2)
        operario  = 1
      elif len(obj.formula.split('+',2))>1:
        clave_tmp = obj.formula.split('+',2)
        operario  = 2
      elif len(obj.formula.split('-',2))>1:
        clave_tmp = obj.formula.split('-',2)
        operario  = 3
      elif len(obj.formula.split('/',2))>1:
        clave_tmp = obj.formula.split('/',2)
        operario  = 4

      clave_tmp[0] = clave_tmp[0].replace(' ','')
      concepto_tmp = concepto.objects.filter(clave__contains=clave_tmp[0])
      if concepto_tmp:
        if operario == 1:
          obj.importe=float(concepto_tmp[0].importe) * float(clave_tmp[1])
        elif operario == 2:
          obj.importe=float(concepto_tmp[0].importe) + float(clave_tmp[1])
        elif operario == 3:
          obj.importe=float(concepto_tmp[0].importe) - float(clave_tmp[1])
        elif operario == 4:
          obj.importe=float(concepto_tmp[0].importe) / float(clave_tmp[1])

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
  form.fields['ciclo_escolar'].queryset = ciclo_escolar.objects.filter(activo=True)
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
  cons_pks = []
  conceptos = None
  obj = None
  mat = True
  matricula = ''
  ref_p = False
  ref_u = False
  ant = str(time.strftime("%y"))
  if pk is not None:
    obj = alumno.objects.get(pk=pk)
    mat = False
    tmp_ref = referencias.objects.filter(alumno=obj)
    obj.matricula = obj.matricula.zfill(4)
    if tmp_ref:
      for i in tmp_ref:
        print i.descripcion
        if 'PRINCIPAL' in i.descripcion:
          ref_p = True
        if 'UNIFORME' in i.descripcion:
          ref_u = True


  form = form_class(request.POST or None,instance=obj)
  descuento_formset = descuentoFormset(request.POST or None,instance=obj)
  referencia_formset = referenciaFormset(request.POST or None,instance=obj)
  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.save()
    
    referencia_formset = referenciaFormset(request.POST or None,instance=obj)
    if referencia_formset.is_valid():
      referencia_formset.save()
      referencia_formset = referenciaFormset(instance=obj)
    
    descuento_formset = descuentoFormset(request.POST or None,instance=obj)
    if descuento_formset.is_valid():
      descuento_formset.save()
      descuento_formset = descuentoFormset(instance=obj)

    messages.success(request,"Se ha Guardado la información con éxito")

  if mat:
    last = alumno.objects.all().last()
    if last == None:
      tmp_last = 0
    else:
      tmp_last = int(last.pk)
    matricula = str(tmp_last+1).zfill(4)

  conceptos = concepto.objects.all()
  for i in conceptos:
    if 'E' in str(i.tipo):
      cons_pks.append(i.pk)
  descuento_formset.form.base_fields['concepto'].queryset = concepto.objects.filter(pk__in=cons_pks)

  form.fields['ciclo_escolar'].queryset = ciclo_escolar.objects.filter(activo=True)
  parametros={
    'ant'       : ant,
    'form'      : form,
    'form_req'  : referencia_formset,
    'form_desc' : descuento_formset,
    'custom'    : True,
    'obj'       : obj,
    'modulo'    : 'categoria',
    'matricula' : matricula,
    'principal' : ref_p,
    'uniforme'  : ref_u
  }
  return parametros