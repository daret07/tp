from django.contrib import admin
from base.utilidades import CustomModelAdmin

# Register your models here.
class usuarioAdmin(CustomModelAdmin):
  list_display = ('username','Superior','first_name','last_name','email','is_active',)
  list_filter = ('last_name',)
  
  def Superior(self,obj):
  	if obj.Superior == None:
  		return '-'

class perfilAdmin(CustomModelAdmin):
  list_display = ('name',)

