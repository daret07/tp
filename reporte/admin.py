# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
from catalogo.models import alumno as alm,referencias,concepto as con
from reporte.models import movimiento
# Register your models here.
class movimientoAdmin(CustomModelAdmin):
  list_display=('fecha_registro','folio','matricula','alumno','referencia','detalles','ciclo','concepto','monto')
  list_display_links=('alumno','referencia',)
  list_filter=('alumno','referencia',)
  search_fields=('alumno','pk',)

  def matricula(self,obj):
    alumno_tmp = obj.alumno
    alumno_return = ''
    try:
      alumno = alm.objects.get(pk=alumno_tmp.pk)
      alumno_return = alumno.matricula
    except:
      alumno_return='No asociado'
    return alumno_return
  
  def detalles(self,obj):
    desc_tmp = obj.referencia
    descrip  = None
    if desc_tmp:
      tmp = referencias.objects.get(referencia=int(desc_tmp))
      descrip =  tmp.descripcion
    elif obj.descripcion:
      descrip = obj.descripcion
    else:
      descrip = 'Movimiento Manual'
    return descrip
  