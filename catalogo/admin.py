from django.contrib import admin
from base.utilidades import CustomModelAdmin
import humanize
# Register your models here.

class ciclo_escolarAdmin(CustomModelAdmin):
	list_display=('clave','descripcion')
	list_display_links=('clave',)
	list_filter=('clave',)
	search_fields=('clave','descripcion')


class conceptoAdmin(CustomModelAdmin):
	list_display=('clave','descripcion','custom_importe')
	list_display_links=('clave',)
	list_filter=('clave',)
	search_fields=('clave','descripcion')
	def custom_importe(self,obj):
    valor = '%0.2f' % obj.importe
    return "$ " + humanize.intcomma(valor)

	custom_importe.short_description = 'Importe'
	custom_importe.admin_order_field = 'importe'


class categoriaAdmin(CustomModelAdmin):
	list_display=('nombre','descripcion','cupo_maximo','ciclo_escolar')
	list_display_links=('nombre',)
	list_filter=('nombre',)
	search_fields=('nombre','descripcion','cupo_maximo','ciclo_escolar')

class alumnoAdmin(CustomModelAdmin):
	list_display=('nombre','paterno','materno','custom_matricula','ciclo_escolar','padre','emergencia','estado')
	list_display_links=('nombre',)
	list_filter=('ciclo_escolar',)
	search_fields=('nombre','paterno','materno','ciclo_escolar')

	def estado(self,obj):
		if obj.estatus == True:
			return 'ALTA'
		elif  obj.estatus == False:
			return 'BAJA'
	def custom_matricula(self,obj):
		return obj.ant + obj.matricula

	custom_matricula.short_description = 'Matricula'
	custom_matricula.admin_order_field = 'matricula'



class personaAdmin(CustomModelAdmin):
	list_display=('nombre',)
	list_display_links=('nombre',)
	list_filter=('nombre',)
	search_fields=('nombre',)