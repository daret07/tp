# -*- coding: utf-8 -*-
from django.shortcuts import render
from reporte.forms import (movimientoForm,movimiento_subirForm)
from reporte.models import (movimiento)
from django.contrib import messages
# Create your views here.

def vista_movimiento(request,pk=None):
  form_class = movimientoForm
  form_file = movimiento_subirForm
  obj = None

  if pk is not None: 
    obj = movimiento.objects.get(pk=pk)

  form = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.save()
    messages.success(request,"Se ha Guardado la información con éxito")
  elif request.FILES:
    file = request.FILES.get('subir_movimiento' or None)
    print file

  parametros={
    'form'      : form,
    'custom'    : True,
    'obj'       : obj,  
    'modulo'    : 'movimiento',
    'form_file' : form_file,
  }
  return parametros