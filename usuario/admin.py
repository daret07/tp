from django.contrib import admin
from base.utilidades import CustomModelAdmin

# Register your models here.
class usuarioAdmin(CustomModelAdmin):
  list_display = ('username','first_name','last_name','email','is_active',)
  list_filter = ('last_name',)

class perfilAdmin(CustomModelAdmin):
  list_display = ('name',)

