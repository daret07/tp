# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuario.models import usuario
from base.utilidades import CustomModelAdmin

# Register your models here.

class bitacoraAdmin(CustomModelAdmin):
	list_per_page = 50
	list_display=('id','proyecto','titulo','descripcion','start_line')
	list_display_links=('id',)
	list_filter=('titulo',)
	date_hierarchy='start_line'
	def get_queryset(self,request):
		queryset = super(bitacoraAdmin,self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		elif request.user.groups.filter(name='CabezaDpto'):
			queryset = queryset.filter(usuario = request.user)
		return queryset

class registroAdmin(CustomModelAdmin):
	list_per_page = 50
	list_display=('id','bitacora','fecha_d','actividad','resultado')
	list_display_links=('',)
	list_filter=('bitacora',)

	def get_queryset(self,request):
		queryset = super(registroAdmin,self).get_queryset(request)
		if request.user.is_superuser:
			return queryset
		
		elif request.user.groups.filter(name='CabezaDpto'):
			ids = usuario.objects.filter(Superior=request.user)
			arr_dis = []
			for i in ids:
				arr_dis.append(i.id)
			queryset = queryset.filter(usuario__in = arr_dis)
		
		elif request.user.groups.filter(name='Personal'):
			queryset = queryset.filter(usuario = request.user)
		return queryset

class fileregAdmin(CustomModelAdmin):
	list_per_page = 50
	list_display=('id','registro','descripcion')
	list_display_links=('id','registro')
	list_filter=('registro',)	