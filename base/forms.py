# -*- coding:UTF-8 -*-
from django import forms
from django.utils.safestring import mark_safe

"""
CustomsSelect es un widget al cual se le añade un boton que condiene en sus data el modelo y la app de donde pertenece, esto se hizo para que en
los foreignkey se puede añadir por medio de un modal
"""
class CustomSelect(forms.widgets.Select):

  def render(self,name,choices,attrs=None):
    from django.apps import  apps
    from importlib import import_module
    from os.path import exists

    model_name   = name
    app_name     = ""
    has_modal    = 'false'
    has_template = 'false'
    disabled     = ''

    ap = apps.all_models
    for value in ap:
      if ap.get(value).has_key(model_name):
        app_name=value
        break

    direccion_modal = "%s/templates/modales/%s.html" % (app_name,model_name)

    if exists(direccion_modal):
      has_modal = 'true'

    direccion_template = "%s/templates/%s.html" % (app_name,model_name)

    if exists(direccion_template):
      has_template= 'true'

    if has_modal == 'false' and has_template =='true':
      disabled = ''
    else:
      disabled = "disabled='disabled'"


    id_boton = "button_%s" % model_name

    salida = []
    salida.append(u''' <div class="input-group"> ''')
    salida.append(super(CustomSelect,self).render(name,choices,attrs))
    salida.append(u''' <span class='input-group-btn'>
                         <button id="%s" type='button' class='btn btn-secondary addForeignKey' data-modelo='%s' data-app='%s' data-has_modal='%s' %s>
                          <i class='fa fa-plus'></i>
                        </button></span>
                  ''' % (id_boton,model_name,app_name,has_modal,disabled))
    salida.append(u''' </div> ''')

    return mark_safe(u''.join(salida))

"""
Clase que tiene como finalidad definir los formularios a través de modelos
"""
class CustomModelForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(CustomModelForm,self).__init__(*args,**kwargs)
    for field_name, field in self.fields.items():
      if type(field) in [forms.fields.CharField,forms.fields.TypedChoiceField]:
        field.widget.attrs = {
          'class' : 'form-control',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.fields.FloatField]:
        field.widget.attrs = {
          'class' : 'form-control decimal',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.fields.EmailField]:
        field.widget.attrs = {
          'class' : 'form-control correo',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.fields.IntegerField]:
        field.widget.attrs = {
          'class'       : 'form-control entero',
          'maxlength'   : '8',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.fields.DateTimeField]:
        field.widget.attrs = {
          'class' : 'form-control datetime',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.fields.DateField]:
        field.widget.attrs = {
          'class' : 'form-control date',
          'placeholder' : field.help_text
        }
      elif type(field) in [forms.models.ModelChoiceField]:
        field.widget = forms.Select(choices=field.choices,attrs = {'class' : 'form-control'} )

"""
Clase que tiene como finalidad definir los formularios basicos
"""
class CustomForm(forms.Form):
  def __init__(self,*args,**kwargs):
    super(CustomForm,self).__init__(*args,**kwargs)
    for field_name, field in self.fields.items():
      if type(field) in [forms.fields.CharField,forms.models.ModelChoiceField,forms.fields.TypedChoiceField,forms.fields.FloatField,forms.fields.EmailField]:
        field.widget.attrs = {
          'class' : 'form-control'
        }
      elif type(field) in [forms.fields.DateTimeField]:
        field.widget.attrs = {
          'class' : 'form-control datetime'
        }
      elif type(field) in [forms.fields.DateField]:
        field.widget.attrs = {
          'class' : 'form-control date'
        }

"""
Formulario de inicio de sesion
"""
class LoginForm(CustomForm):
    usuario    = forms.CharField()
    contrasena = forms.CharField(widget=forms.PasswordInput())
