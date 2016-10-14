# -*- coding: utf-8 -*-
from django.shortcuts import render
from automatico.models import cron_auto
from automatico.forms import cron_autoForm
from django.contrib import messages

# Create your views here.
def vista_cron_auto(request,pk=None):
  form_class  = cron_autoForm
  obj         = None
  minuto      = range(1,59)
  hora        = range(1,24)
  dia         = range(1,31)
  mes         = messes()  
  min_select  = []
  hor_select  = []
  dia_select  = []
  mes_select  = []
  if pk is not None:
    obj       = cron_auto.objects.get(pk=pk)
    if obj.definicion:
      tmp = obj.definicion.split(' ')
      min_select = tmp[0]
      hor_select = tmp[1]
      dia_select = tmp[2]
      mes_select = tmp[3]

  form        = form_class(request.POST or None,instance=obj)

  if request.POST and form.is_valid():
    minuto_tmp    = request.POST.getlist('minuto')
    hora_tmp      = request.POST.getlist('hora')
    dia_tmp       = request.POST.getlist('dia')
    mes_tmp       = request.POST.getlist('mes')
    if len(hora_tmp) == 0 :
      hora_tmp = '*'
    if len(minuto_tmp) == 0 :
      minuto_tmp = '*'
    if len(dia_tmp) == 0 :
      dia_tmp = '*'
    if len(mes_tmp) == 0 :
      mes_tmp='*'
    obj           = form.save(commit=False)
    obj.definicion = str(','.join(map(str, minuto_tmp)))+' '+str(','.join(map(str, hora_tmp)))+' '+str(','.join(map(str, dia_tmp)))+' '+str(','.join(map(str, mes_tmp)))+' *'
    obj.save()
  
    messages.success(request,"Se ha Guardado la información con éxito")

  parametros  ={
    'form'    : form,
    'minuto'  : minuto,
    'hora'    : hora,
    'mes'     : mes,
    'dia'     : dia,
    'custom'  : True,
    'obj'     : obj,  
    'modulo'  : 'cron_auto',
    'min_s'  :min_select,
    'hor_s'  :hor_select,
    'dia_s'  :dia_select,
    'mes_s'  :mes_select,
  }
  
  return parametros

def messes():
  val = []
  val.append(('1','Enero'),)
  val.append(('2','Febrero'),)
  val.append(('3','Marzo'),)
  val.append(('4','Abril'),)
  val.append(('5','Mayo'),)
  val.append(('6','Junio'),)
  val.append(('7','Julio'),)
  val.append(('8','Agosto'),)
  val.append(('9','Septiembre'),)
  val.append(('10','Octubre'),)
  val.append(('11','Noviembre'),)
  val.append(('12','Diciembre'),)
  return val