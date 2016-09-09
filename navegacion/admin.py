from django.contrib import admin
from navegacion.models import menu

class menuAdmin(admin.ModelAdmin):
  list_display = ('nombre','app','modelo','padre','icono','permiso','nivel','listar','activo')

# Register your models here.
admin.site.register(menu,menuAdmin)
