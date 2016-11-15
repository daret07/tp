from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.

class ciclo_escolarAdmin(CustomModelAdmin):
	list_display=('clave','descripcion')
	list_display_links=('clave',)
	list_filter=('clave',)
	search_fields=('clave','descripcion')


class conceptoAdmin(CustomModelAdmin):
	list_display=('clave','descripcion','monto')
	list_display_links=('clave',)
	list_filter=('clave',)
	search_fields=('clave','descripcion')

	def monto(self,obj):
    
    return '$ %s'%humanize.intcomma(obj.importe)

class categoriaAdmin(CustomModelAdmin):
	list_display=('nombre','descripcion','cupo_maximo','ciclo_escolar')
	list_display_links=('nombre',)
	list_filter=('nombre',)
	search_fields=('nombre','descripcion','cupo_maximo','ciclo_escolar')

class alumnoAdmin(CustomModelAdmin):
	list_display=('nombre','paterno','materno','Matricula','ciclo_escolar','padre','emergencia','estado')
	list_display_links=('nombre',)
	list_filter=('nombre',)
	search_fields=('nombre','paterno','materno')

	def estado(self,obj):
		if obj.estatus == True:
			return 'ALTA'
		elif  obj.estatus == False:
			return 'BAJA'
	def Matricula(self,obj):
		return obj.ant + obj.matricula

class personaAdmin(CustomModelAdmin):
	list_display=('nombre',)
	list_display_links=('nombre',)
	list_filter=('nombre',)
	search_fields=('nombre',)