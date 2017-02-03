# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from inscripcion.forms import (inscripcionForm)
from inscripcion.models import (inscripcion)
from catalogo.models import alumno,categoria,ciclo_escolar
from django.contrib import messages
from usuario.models import usuario 
# Create your views here.

def vista_inscripcion(request,pk=None):
  cat = categoria.objects.all()
  form_class = inscripcionForm
  obj = None
  maximo = 0
  cupo     = 0
  perfil = get_perfil(request)
  if pk is not None:
    obj = inscripcion.objects.get(pk=pk)
    cupo = obj.categoria.cupo_maximo
    alumnos   = inscripcion.objects.filter(categoria=obj.categoria)
    maximo  = len(alumnos)

  form = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    pk_alumno          = request.POST.get('alumno')
    alumno_inscripcion = alumno.objects.get(pk=pk_alumno)
    inscripcion_tmp    = inscripcion.objects.filter(alumno=alumno_inscripcion)
    if not obj:
      if inscripcion.objects.filter(alumno=alumno_inscripcion):
        auto_inscripcion(request,alumno_inscripcion,True)
      else:
        auto_inscripcion(request,alumno_inscripcion,False)
      
    obj = form.save(commit=False)
    obj.save()
     
    if len(usuario.objects.filter(username=str(obj.alumno_matricula)))==0:
      users = usuario.objects.create(username=str(obj.alumno_matricula),first_name=str(obj.alumno_nombre)+' '+str(obj.alumno_paterno),email=str(obj.alumno_email))
      users.set_password(str(obj.alumno_paterno)+str(obj.alumno_matricula))
      grupo = get_perfil_user(request)
      users.groups.add(grupo['perfil'][0])
      users.save()
      messages.success(request,"Se ha Guardado la información con éxito y Se ha Creado un usuario: "+str(obj.alumno_matricula)+", Contraseña: "+str(obj.alumno_paterno)+str(obj.alumno_matricula))
    else:
      messages.success(request,"Se ha Guardado la información con éxito")
    
    alumno.objects.filter(pk=obj.alumno.pk).update(ciclo_escolar=obj.ciclo)
    

  catego   = categoria.objects.all()
  tmp_id_ins =[]
  for i in catego:
    tmp = inscripcion.objects.filter(categoria =i)
    if len(tmp) <= i.cupo_maximo:
      tmp_id_ins.append(i.pk)
    form.fields['categoria'].queryset = categoria.objects.filter(pk__in=tmp_id_ins)
  form.fields['ciclo'].queryset = ciclo_escolar.objects.filter(activo=True)

  operacion = request.POST.get('form_action',None)

  if operacion == 'SAVE_AND_OTHER':
    return redirect('crear',app='inscripcion',modelo='inscripcion')
  elif operacion == 'SAVE':
    if form.is_valid():
      return redirect('listar',app='inscripcion',modelo='inscripcion')

    
  parametros={
    'form'    : form,
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'inscripcion',
    'cupo'    : cupo,
    'maximo'  : maximo,
    'perfil'  : perfil,
  }
  return parametros

def get_perfil_user(request):
  from django.contrib.auth.models import Group
  perfil = []
  for i in Group.objects.filter(name='PADRE'):
    perfil.append(i.pk)
  parametros={
    'perfil'  : perfil
  }
  return parametros

def get_perfil(request):
  perfil = []
  for i in request.user.groups.all():
    perfil.append(i.name)
  parametros={
    'perfil'  : perfil
  }
  return parametros


def auto_inscripcion(request,alumno,tipo):
  from automatico.models import condicionantes,condicionante_tmp
  from catalogo.models import concepto
  from reporte.models import movimiento
  from django.utils import timezone
  from reporte.views import descuentos
  if tipo:
    concepto_tmp = concepto.objects.filter(clave='REINSCRIPCION')
    tmps = condicionantes.objects.filter(concepto=concepto_tmp,activo=True)
    for item in tmps:
      tmps_tmp = condicionante_tmp.objects.filter(padre=item)
      for item_tmp in tmps_tmp:
        movimiento.objects.create(
              fecha_registro=timezone.now(),
              ciclo=alumno.ciclo_escolar,
              alumno=alumno,
              concepto=item_tmp.concepto_tmp,
              monto=item_tmp.concepto_tmp.importe,
              descripcion='Movimiento De Reinscripcion')
        descuentos(alumno.pk,item_tmp.concepto_tmp.importe,item_tmp.concepto_tmp,alumno.ciclo_escolar)
  else:
    concepto_tmp = concepto.objects.filter(clave='INSCRIPCION')
    tmps = condicionantes.objects.filter(concepto=concepto_tmp,activo=True)
    for item in tmps:
      tmps_tmp = condicionante_tmp.objects.filter(padre=item)
      for item_tmp in tmps_tmp:
        movimiento.objects.create(
              fecha_registro=timezone.now(),
              ciclo=alumno.ciclo_escolar,
              alumno=alumno,
              concepto=item_tmp.concepto_tmp,
              monto=item_tmp.concepto_tmp.importe,
              descripcion='Movimiento De Inscripcion')
        descuentos(alumno.pk,item_tmp.concepto_tmp.importe,item_tmp.concepto_tmp,alumno.ciclo_escolar)