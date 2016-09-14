# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.
class movimientoAdmin(CustomModelAdmin):
	list_display=('alumno','ciclo','concepto')
	list_display_links=('alumno',)
	list_filter=('alumno',)
	search_fields=('alumno','pk',)