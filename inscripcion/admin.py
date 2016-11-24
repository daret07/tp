from django.contrib import admin
from base.utilidades import CustomModelAdmin

# Register your models here.
class inscripcionAdmin(CustomModelAdmin):
  list_display=('alumno','alumno_matricula','ciclo','categoria','alumno_curp')
  list_display_links=('alumno',)
  list_filter=('alumno','categoria',)
  search_fields=('alumno__nombre',)