# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
from catalogo.models import alumno as alm,referencias,concepto as con
from reporte.models import movimiento
import humanize
from datetime import datetime
# Register your models here.
class movimientoAdmin(CustomModelAdmin):
  list_display=('campo_fecha_registro','folio','matricula','alumno','referencia','descripcion','ciclo','concepto','campo_monto')
  list_display_links=('alumno','referencia',)
  list_filter=('alumno','referencia',)
  search_fields=('alumno','pk',)
  date_hierarchy='fecha_registro'
  

  def matricula(self,obj):
    alumno_tmp = obj.alumno
    alumno_return = ''
    try:
      alumno = alm.objects.get(pk=alumno_tmp.pk)
      alumno_return = alumno.matricula
    except:
      alumno_return='No asociado'
    return alumno_return
  
  def descripcion(self,obj):
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

  def campo_monto(self,obj):
    
    return '$ %s'%humanize.intcomma(obj.monto)

  def campo_fecha_registro(self,obj):
    return '%s'%datetime.strftime(obj.fecha_registro,"%d/%m/%Y")