# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
from catalogo.models import alumno as alm,referencias,concepto as con
from reporte.models import movimiento
import humanize
from datetime import datetime
# Register your models here.
class movimientoAdmin(CustomModelAdmin):
  list_per_page = 20
  list_display=('campo_fecha_registro','folio','matricula','alumno','referencia','descripcion','ciclo','concepto','campo_monto')
  list_display_links=('alumno','referencia',)
  list_filter=('alumno','referencia',)
  date_hierarchy='fecha_registro'
  

  def matricula(self,obj):
    return obj.alumno.ant+obj.alumno.matricula
  
  def descripcion(self,obj):
    if obj.referencia.descripcion:
      return obj.referencia.descripcion
    else:
      return 'Movimiento Manual'
    

  def campo_monto(self,obj):
    
    return '$ %s'%humanize.intcomma(obj.monto)

  def campo_fecha_registro(self,obj):
    return '%s'%datetime.strftime(obj.fecha_registro,"%d/%m/%Y")