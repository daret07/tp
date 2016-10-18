# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.
class cron_autoAdmin(CustomModelAdmin):
  list_display=('id','campo_concepto','esta_activo','tiene_hermanos','condicion','definicion')
  list_display_links=('id',)
  list_filter=('id',)
  search_fields=('id',)
  
  def campo_concepto(self,obj):
    if obj.concepto:
      return obj.concepto
    else:
      return 'Recargos'

  def esta_activo(self,obj):
    if obj.activo:
      tmp = 'fa fa-check'
      return "<i class='fa fa-check-circle' aria-hidden='true' style='color:green;'></i>"
    else:
      return "<i class='fa fa-times-circle' aria-hidden='true' style='color:green;'></i>"
  esta_activo.allow_tags=True

  def tiene_hermanos(self,obj):
    if obj.hermanos:
      tmp = 'fa fa-check'
      return "<i class='fa fa-check-circle' aria-hidden='true' style='color:green;'></i>"
    else:
      return "<i class='fa fa-times-circle' aria-hidden='true' style='color:red;'></i>"
  tiene_hermanos.allow_tags=True

  def condicion(self,obj):
    if obj.condiciones:
      tmp = 'fa fa-check'
      return "<i class='fa fa-check-circle' aria-hidden='true' style='color:green;'></i>"
    else:
      return "<i class='fa fa-times-circle' aria-hidden='true' style='color:red;'></i>"
  condicion.allow_tags=True