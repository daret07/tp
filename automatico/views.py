# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from automatico.models import cron_auto,recargo_pago,pronto_pago,excendente
from automatico.forms import cron_autoForm,recargo_pagoFormset,pronto_pagoFormset,excendenteFormset
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
  pronto      = pronto_pagoFormset(request.POST or None,instance=obj)
  form_set    =  recargo_pagoFormset(request.POST or None,instance=obj)
  excendent   = excendenteFormset(request.POST or None, instance=obj)
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
    
    if str(obj.tipo) == '2':
      form_set    =  recargo_pagoFormset(request.POST or None,instance=obj)
      if form_set.is_valid():
        form_set.save()
    
    elif str(obj.tipo) == '1':
      pronto      = pronto_pagoFormset(request.POST or None,instance=obj)
      if pronto.is_valid():
        pronto.save()  
    
    elif str(obj.tipo) == '3':
      excedent      = excendenteFormset(request.POST or None,instance=obj)
      if excedent.is_valid():
        excedent.save() 

    messages.success(request,"Se ha Guardado la información con éxito")
  form_set =recargo_pagoFormset(instance=obj)
  pronto      = pronto_pagoFormset(instance=obj)
  excendent   = excendenteFormset(instance=obj)
  if obj:
    if obj.definicion:
      tmp = obj.definicion.split(' ')
      min_select = tmp[0]
      hor_select = tmp[1]
      dia_select = tmp[2]
      mes_select = tmp[3]

  operacion = request.POST.get('form_action',None)

  if operacion == 'SAVE_AND_OTHER':
    return redirect('crear',app='automatico',modelo='cron_auto')
  elif operacion == 'SAVE':
    return redirect('listar',app='automatico',modelo='cron_auto')
  parametros  ={
    'prontose': pronto,
    'formset' : form_set,
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
    'excendente':excendent,
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
