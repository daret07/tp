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