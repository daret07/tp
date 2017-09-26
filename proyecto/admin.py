# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from base.utilidades import CustomModelAdmin
from proyecto.models import project,task

admin.site.register(project)

class projectAdmin(CustomModelAdmin):
	list_display=('titulo','descripcion','usuario')#,'Agregar_Tareas')
	list_display_links=('titulo',)
	list_filter=('titulo','usuario')
	search_fields=('titulo__nombre',)
	def get_queryset(self,request):
		queryset = super(projectAdmin,self).get_queryset(request)
		perfil = request.user.groups.filter(name='Gerente')
		if perfil:
			return queryset
		elif request.user.is_superuser:
			return queryset
		else:
			queryset = queryset.filter(usuario = request.user)
			return queryset


class taskAdmin(CustomModelAdmin):
	list_per_page = 50
	list_display=('id','titulo','proyecto','usuario','estatus','descripcion','Acciones')
	list_display_links=('id',)
	list_filter=('usuario',)
	date_hierarchy='start_line'

	def get_queryset(self,request):
		queryset = super(taskAdmin,self).get_queryset(request)
		if request.user.groups.filter(name='Personal'):
			queryset = queryset.filter(usuario=request.user).order_by('proyecto')
		elif request.user.is_superuser:
			return queryset.order_by('proyecto')
		elif request.user.groups.filter(name='CabezaDpto'):
			queryset = queryset.filter(proyecto__usuario=request.user).order_by('proyecto')
		return queryset

	def Acciones(obj,self):
		if self.estatus == '1':
			return "<input type='button' class='btn btn-primary modals' data-id='{0}' value='Finalizar'>".format(self.id)
		else:
			return "<label class='label label-info'>Tarea Finalizada</label>"
	Acciones.allow_tags=True


class filetaskAdmin(CustomModelAdmin):
	list_per_page = 50
	list_display=('id','proyecto','descripcion')
	list_display_links=('id','proyecto')
	list_filter=('proyecto',)	



	