# -*- coding: utf-8 -*-

def validar(request):
  print request.POST
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
      estado_cuentas.append((i.fecha_registro,i.concepto.nombre,i.concepto.tipo,i.monto),)

      if str(i.concepto.tipo) == 'E':
        saldo_mensual += i.monto
      if str(i.concepto.tipo) == 'I':
        saldo_mensual -= i.monto


  parametros ={
  'total'          : debe,
  'saldo_mensual'  : saldo_mensual,
  'mensualidad'    : estado_cuentas,
  'saldo_anterior' : float(debe)-float(saldo_mensual),
  }
  return parametros


def getvalue(request):
  from catalogo.models import concepto
  concept = concepto.objects.get(pk=request.POST.get('concep'))
  parametros={
  'importe':concept.importe,
  'tipo':concept.tipo,
  }
  return parametros