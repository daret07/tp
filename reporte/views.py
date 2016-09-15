# -*- coding: utf-8 -*-
from django.shortcuts import render
from reporte.forms import (movimientoForm)
from reporte.models import (movimiento)
from django.contrib import messages
import xlrd
from os.path import join, dirname, abspath
from catalogo.models import concepto
# Create your views here.

def vista_movimiento(request,pk=None):
  form_class = movimientoForm 
  obj = None

  if pk is not None: 
    obj = movimiento.objects.get(pk=pk)

  form = form_class(request.POST or None,instance=obj)

  if request.FILES:
    extension_valida = [
      ".xls",
      ".xlsx",
    ]
    file = request.FILES.get('archivo' or None)
    nombre_imagen = file.name

    imagen_valida = False
    for extension in extension_valida:
      if nombre_imagen.lower().endswith(extension):
        imagen_valida = True
        break
    
    if imagen_valida:
      obj = form.save(commit=False)
      obj.archivo = request.FILES.get('archivo' or None)
      obj.save()
      libro = xlrd.open_workbook(obj.archivo.path)
      hojas = libro.sheet_names()
      hoja  = libro.sheet_by_name(hojas[0])
      columnas = hoja.ncols

    if columnas == 10:
      for row_idx in range(0, hoja.ncols):
        label_numero = hoja.cell(0,row_idx).value

        if label_numero.lower() == 'referencia':
          obj.referencia = hoja.cell(1,row_idx).value

        if label_numero.lower() == 'importe':
          obj.monto = hoja.cell(1,row_idx).value

        if label_numero.lower().encode('utf8') == 'numero operación':
          obj.folio = hoja.cell(1,row_idx).value

        if label_numero.lower().encode('utf8') == 'fecha de operación':
          obj.fecha_registro = xlrd.xldate.xldate_as_datetime(hoja.cell(1,row_idx).value, libro.datemode)

    obj.concepto = concepto.objects.get(clave='abono')
    obj.save()
    messages.success(request,"Se ha Guardado la información con éxito")
    form = form_class(instance=obj)


  elif request.POST and form.is_valid():
    alumno = request.POST.get('alumno')
    referencia = request.POST.get('referencia')
    monto  = request.POST.get('monto')
    if monto != '' and referencia != '' and alumno != '':
      obj = form.save(commit=False)
      obj.save()
      messages.success(request,"Se ha Guardado la información con éxito")
      form = form_class(request.POST or None,instance=obj)
    else:
      messages.error(request,'Se debe de colocar almenos una de las dos opciones, ya se archivo o llenar todos los campos')

  parametros={
    'form'      : form,
    'custom'    : True,
    'obj'       : obj,  
    'modulo'    : 'movimiento',
  }
  return parametros