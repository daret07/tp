# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
from catalogo.models import alumno as alm,referencias
from reporte.models import movimiento
# Register your models here.
class movimientoAdmin(CustomModelAdmin):
  list_display=('fecha_registro','folio','matricula','alumno','referencia','descripcion','ciclo','concepto','monto')
  list_display_links=('alumno',)
  list_filter=('alumno',)
  search_fields=('alumno','pk',)

  def matricula(self,obj):
    alumno_tmp = obj.alumno
    alumno = alm.objects.get(pk=alumno_tmp.pk)
    return alumno.matricula
  def descripcion(self,obj):
    desc_tmp = obj.referencia
    descrip  = None
    if desc_tmp:
      tmp = referencias.objects.get(referencia=int(desc_tmp))
      descrip =  tmp.descripcion
    else:
      descrip ='Movimiento Manual'
      

    return descrip
