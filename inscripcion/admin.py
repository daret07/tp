from django.contrib import admin
from base.utilidades import CustomModelAdmin

# Register your models here.
class inscripcionAdmin(CustomModelAdmin):
  list_display=('alumno_nombre','ciclo','categoria','alumno_curp')
  list_display_links=('alumno_nombre',)
  list_filter=('alumno_nombre',)
  search_fields=('alumno_nombre','ciclo',)