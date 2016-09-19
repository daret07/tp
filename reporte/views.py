# -*- coding: utf-8 -*-
from django.shortcuts import render
from reporte.forms import (movimientoForm)
from reporte.models import (movimiento)
from django.contrib import messages
import xlrd
from os.path import join, dirname, abspath
from catalogo.models import concepto,alumno as alm,referencias as ref, ciclo_escolar
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
          tmp            = int(hoja.cell(1,row_idx).value)
          ref_tmp        = ref.objects.get(referencia=tmp)
          alumno_tmp     = alm.objects.get(pk=ref_tmp.alumno.pk)
          obj.alumno     = alumno_tmp
          obj.ciclo      = alumno_tmp.ciclo_escolar

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
    if monto != '':
      obj = form.save(commit=False)
      obj.ciclo = ciclo_escolar.objects.get(alumno=alumno)
      obj.save()
      messages.success(request,"Se ha Guardado la información con éxito")
    else:
      messages.error(request,'Se debe de colocar almenos una de las dos opciones, ya se archivo o llenar todos los campos')
    form = form_class(request.POST or None,instance=obj)

  parametros={
    'form'      : form,
    'custom'    : True,
    'obj'       : obj,  
    'modulo'    : 'movimiento',
  }
  return parametros

def vista_ficha_inscripcion(request,pk=None):
  from catalogo.models import ciclo_escolar,categoria
  from inscripcion.models import inscripcion
  from django.db.models import Q
  ciclo = ciclo_escolar.objects.all()
  categ = categoria.objects.all()
  inscripcion_filtro = None
  tmp_ciclo =''
  tmp_categoria=''
  
  if request.POST:
    
    if request.POST.get('ciclo'):
      tmp_ciclo     = ciclo_escolar.objects.get(pk=request.POST.get('ciclo'))
    
    if request.POST.get('categoria'):
      tmp_categoria = categoria.objects.get(pk=request.POST.get('categoria'))

    if tmp_categoria != '' and tmp_ciclo != '':
      inscripcion_filtro   = inscripcion.objects.filter(ciclo=tmp_ciclo,categoria=tmp_categoria)
    elif tmp_categoria == '' and tmp_ciclo != '':
      inscripcion_filtro   = inscripcion.objects.filter(ciclo=tmp_ciclo)
    elif tmp_categoria != '' and tmp_ciclo == '':
      inscripcion_filtro   = inscripcion.objects.filter(categoria=tmp_categoria)

  parametros={
    'ciclo'      : ciclo,
    'categoria'  : categ,
    'inscripcion': inscripcion_filtro
  }
  return parametros

def vista_reporte_referencia(request,pk=None):
  refe = ref.objects.all()
  parametros={'referencias':refe}
  return parametros

def vista_reporte_saldos(request,pk=None):
  
  parametros={'saldo':'a'}
  return parametros

def vista_deudores(request,pk=None):
  from reporte.models import movimiento
  movimientos = list(movimiento.objects.all())
  parametros={'saldo':'a'}
  return parametros