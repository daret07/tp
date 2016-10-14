# -*- coding:UTF-8 -*-
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import helpers
from django.contrib.admin.views.main import ChangeList
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages
import csv

def export_as_csv_action(description="Exportar registros seleccionados a CSV",
                         fields=None, exclude=None, header=True):
    
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv

def eliminar_usuario(modeladmin,request,queryset):
    queryset.delete()

eliminar_usuario.short_description = 'Eliminar registros seleccionados'

custom_site = AdminSite()
custom_site.disable_action('delete_selected')
custom_site.add_action(eliminar_usuario)
custom_site.add_action(export_as_csv_action())

"""
Clase ChangeList modificada, con la finalidad de poder establecer la direccion
que aparecera en los listados, dado el proyecto generico que se realiza
"""
class CustomChangeList(ChangeList):
    
    # Metodo que permite generar la liga de retorno
    def url_for_result(self,result):
        name = self.model.__name__
        pk   = getattr(result,self.pk_attname)
        
        return reverse(
                'editar',
                args=[
                    self.opts.app_label,
                    self.opts.model_name,
                    pk
                ])

"""
Clase ModelAdmin personalizada con la finalidad de extender la funcionalidad
en especifico de ChangeList
"""
class CustomModelAdmin(ModelAdmin):
    
    new_queryset = None
    
    # Metodo que regresa la clase personalizada CustomChangeList
    def get_changelist(self,request,**kwargs):
        kwargs = request
        return CustomChangeList
    
    # Metodo que permite reemplazar el queryset.
    def set_queryset(self,queryset):
        self.new_queryset = queryset

    def get_queryset(self,request):
        qs = super(CustomModelAdmin,self).get_queryset(request)
        if self.new_queryset is None:
            return qs
        else:
            self.queryset = self.new_queryset
            return self.new_queryset

def obtener_listado(
  self,
  model,
  list_display=[],
  list_display_links=None,
  list_filter=[],
  date_hierarchy=None,
  search_fields=[],
  list_per_page=500,
  list_max_show_all=5000,
  queryset=None):
  
  my_admin = CustomModelAdmin
  my_admin                     = my_admin(model,AdminSite())
  my_admin.list_display        = list_display
  my_admin.list_display_links  = list_display_links
  my_admin.list_filter         = list_filter
  my_admin.date_hierarchy      = date_hierarchy
  my_admin.search_fields       = search_fields
  my_admin.list_select_related = ''
  my_admin.list_per_page       = list_per_page
  my_admin.list_max_show_all   = list_max_show_all
  my_admin.list_editable       = []
  my_admin.actions             = []
  my_admin.action_form         = helpers.ActionForm

  if queryset != None:
    nuevo_queryset = queryset
    my_admin.set_queryset(nuevo_queryset)

  ChangeList = my_admin.get_changelist(self)

  listado = ChangeList(
    self,
    model,
    my_admin.list_display,
    my_admin.list_display_links,
    my_admin.list_filter,
    my_admin.date_hierarchy,
    my_admin.search_fields,
    my_admin.list_select_related,
    my_admin.list_per_page,
    my_admin.list_max_show_all,
    my_admin.list_editable,
    my_admin)

  listado.formset = None

  return listado

def obtener_listado_admin(
  self,
  model,
  my_admin=CustomModelAdmin,
  queryset=None):
  
  #custom_site.register(model,model)

  my_admin = my_admin(model,custom_site)
  if queryset != None:
    nuevo_queryset = queryset
    my_admin.set_queryset(nuevo_queryset)
    
  list_display = ['action_checkbox'] + list(my_admin.list_display)
  
  my_admin.show_admin_actions = True
  my_admin.actions = my_admin.get_actions(self)
  action_form = my_admin.action_form(self.POST)
  action_form.fields['action'].choices = my_admin.get_action_choices(self)

  ChangeList = my_admin.get_changelist(self)

  listado = ChangeList(
    self,
    model,
    list_display,
    my_admin.get_list_display_links(self,my_admin.list_display),
    my_admin.list_filter,
    my_admin.date_hierarchy,
    my_admin.search_fields,
    my_admin.list_select_related,
    my_admin.list_per_page,
    my_admin.list_max_show_all,
    my_admin.list_editable,
    my_admin)
  
  selected = self.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

  if selected:
    response = my_admin.response_action(self,queryset=listado.get_queryset(self))
    if type(response) is HttpResponse:
      return response
  
  #if not selected and self.POST:
  #  messages.error(self, 'No selecciono ningun elemento. No se afecto ningún elemento')

  listado.formset = None

  parametros = {
    'cl'                        : listado,
    'action_form'               : action_form,
    'actions_selection_counter' : my_admin.actions_selection_counter
  }

  return parametros


