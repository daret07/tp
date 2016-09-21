# -*- coding: utf-8 -*-
from django.shortcuts import render
from reporte.forms import (movimientoForm,reporte_saldosForm,ficha_inscricionForm,estado_cuentaForm)
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
  form = ficha_inscricionForm()
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
    form = ficha_inscricionForm(request.POST)
  parametros={
    'ciclo'      : ciclo,
    'categoria'  : categ,
    'inscripcion': inscripcion_filtro,
    'form'       : form
  }
  return parametros

def vista_reporte_referencia(request,pk=None):
  refe = ref.objects.all()
  parametros={'referencias':refe}
  return parametros

def vista_reporte_saldos(request,pk=None):
  from datetime import datetime 
  from reporte.models import movimiento
  alumnos =''
  reporte =[]
  form = reporte_saldosForm
  total = 0
  fecha_inicio = datetime.strptime(str(datetime.now())[:10],"%Y-%m-%d").strftime("%d/%m/%Y")
  fecha_fin    = datetime.strptime(str(datetime.now())[:10],"%Y-%m-%d").strftime("%d/%m/%Y")
  

  if request.POST:
    f_i = request.POST.get('desde', datetime.now())
    f_f = request.POST.get('hasta', datetime.now())
    fecha_inicio = datetime.strptime(str(f_i),"%d/%m/%Y").strftime("%Y-%m-%d")
    fecha_fin    = datetime.strptime(str(f_f),"%d/%m/%Y").strftime("%Y-%m-%d")
    
    ciclo   = ciclo_escolar.objects.get(pk=request.POST.get('ciclo') or None)
    if ciclo == None:
      alumnos = alm.objects.filter(fecha_de_ingreso__range=(fecha_inicio,fecha_fin))
    else:  
      alumnos = alm.objects.filter(fecha_de_ingreso__range=(fecha_inicio,fecha_fin),ciclo_escolar=ciclo)
    for i in alumnos:
      movimientos=movimiento.objects.filter(alumno=i)  
      suma = 0
      for a in movimientos:
        if str(a.concepto.tipo) == 'ingreso':
          suma += a.monto
          total += a.monto
        elif str(a.concepto.tipo) == 'egreso':
          suma -= a.monto
          total -= a.monto
      reporte.append((i.matricula,i.nombre+' '+i.paterno+' '+i.materno, i.fecha_de_nacimiento,suma,i.estatus))
    form = reporte_saldosForm(request.POST or None)
  else:
    form = reporte_saldosForm(initial={'desde':fecha_inicio,'hasta':fecha_fin})
  parametros={'reporte':reporte,'form':form,'total':total}
  return parametros

def vista_deudores(request,pk=None):
  from reporte.models import movimiento
  from django.db.models import Count, Sum
  alumno = movimiento.objects.values('alumno').distinct()
  deudores_tmp=[]
  deudores =[]
  total = 0
  for i in alumno:
    tmp= i['alumno']
    movimientos=movimiento.objects.filter(alumno=tmp)
    suma = 0
    for a in movimientos:
      if str(a.concepto.tipo) == 'ingreso':
        suma += a.monto
        total += a.monto
      elif str(a.concepto.tipo) == 'egreso':
        suma -= a.monto
        total -= a.monto
    if suma < 0:
      deudores_tmp.append((i['alumno'],suma))
  for i in deudores_tmp:
    alumno_tmp=alm.objects.get(pk=i[0])
    deudores.append((alumno_tmp.matricula,alumno_tmp.nombre,alumno_tmp.fecha_de_nacimiento,float(i[1])))
  parametros={'saldo':deudores,'total':total}
  return parametros

def vista_estado_cuenta(request,pk=None):
  form = estado_cuentaForm
  if request.POST:
    print request.POST
  parametros={
  'form':form
  }
  return parametros