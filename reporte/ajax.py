# -*- coding: utf-8 -*-

def validar(request):
  params ={'a':'a'}
  return params

def filtro_categoria(request):
  from catalogo.models import categoria,ciclo_escolar
  ciclo = ciclo_escolar.objects.get(pk=request.POST.get('cat'))
  cat   = categoria.objects.filter(ciclo_escolar=ciclo)
  cat_pk = []
  for i in cat:
    cat_pk.append(i.pk)
  parametros={
  'categorias': cat_pk
  }
  return parametros

def estado_cuenta(request):
  from reporte.models import movimiento
  from catalogo.models import alumno
  from django.db.models import Sum
  pks  = request.POST.get('cuenta')
  mes  = request.POST.get('mes')
  anio = request.POST.get('anio')
  alum = alumno.objects.get(pk=pks)

  ingreso = movimiento.objects.filter(concepto__tipo = 'I',alumno=alum)
  total_ingreso = ingreso.aggregate(total = Sum('monto'))['total'] 
  if not total_ingreso:
    total_ingreso = 0

  egreso = movimiento.objects.filter(concepto__tipo = 'E',alumno=alum)
  total_eso = egreso.aggregate(total = Sum('monto'))['total'] 
  if not total_eso:
    total_eso = 0
  debe = total_eso-total_ingreso


  movs_mes = movimiento.objects.filter(alumno=alum,fecha_registro__month=mes,fecha_registro__year=anio).prefetch_related('concepto')
  saldo_mensual = 0
  estado_cuentas = []
  

  if movs_mes:
    for i in movs_mes:
      estado_cuentas.append((i.fecha_registro,i.concepto.descripcion,i.concepto.tipo,i.monto),)

      if str(i.concepto.tipo) == 'E':
        saldo_mensual += i.monto
      if str(i.concepto.tipo) == 'I':
        saldo_mensual -= i.monto
  
  mes_ant = mes_anterior(mes,anio)
  movs_mes_ant = movimiento.objects.filter(alumno=alum,fecha_registro__month=mes_ant['mes'],fecha_registro__year=mes_ant['anio']).prefetch_related('concepto')
  saldo_mensual_ant = 0
  if movs_mes_ant:
    for i in movs_mes_ant:
      if str(i.concepto.tipo) == 'E':
        saldo_mensual_ant += i.monto
      if str(i.concepto.tipo) == 'I':
        saldo_mensual_ant -= i.monto


  parametros ={
  'total'          : saldo_mensual,
  'saldo_mensual'  : saldo_mensual,
  'mensualidad'    : estado_cuentas,
  'saldo_anterior' : float(saldo_mensual_ant) + float(0.0),
  'mensaje'        : '' if saldo_mensual > 0 else '( Mensualidad - Saldada )'
  }
  return parametros

def mes_anterior(mes,anio):
  anio_a = 0
  mes_a  = 0
  if int(mes) == 1:
    mes_a = 12
    anio_a = int(anio) - 1
  else:
    mes_a = int(mes) - 1
    anio_a=anio
  return {
  'mes' :mes_a,
  'anio':anio_a,
  }

def getvalue(request):
  from catalogo.models import concepto
  concept = concepto.objects.get(pk=request.POST.get('concep'))
  parametros={
  'importe':concept.importe,
  'tipo':concept.tipo,
  }
  return parametros