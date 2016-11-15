# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.
class cron_autoAdmin(CustomModelAdmin):
  list_display=('esta_activo','descripcion')
  list_display_links=('descripcion',)
  list_filter=('descripcion',)

  


  def esta_activo(self,obj):
    if obj.activo:
      tmp = 'fa fa-check'
      return "<i class='fa fa-check-circle' aria-hidden='true' style='color:green;'></i>"
    else:
      return "<i class='fa fa-times-circle' aria-hidden='true' style='color:green;'></i>"
  esta_activo.allow_tags=True

