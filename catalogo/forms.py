from django import forms
from base.forms import CustomForm,CustomModelForm
from catalogo.models import *

class conceptoForm(CustomModelForm):
  def __init__(self, *args,**kwargs):
    super(conceptoForm,self).__init__(*args,**kwargs)
    if self.fields['importe'].widget.attrs.has_key('class'):
      self.fields['importe'].widget.attrs['class']+='form-control decimal'
    else:
      self.fields['importe'].widget.attrs.update({'class' : 'form-control decimal'})

  class Meta:
    model = concepto
    fields='__all__'

class ciclo_escolarForm(CustomModelForm):
  class Meta:
    model=ciclo_escolar
    fields='__all__'

class categoriaForm(CustomModelForm):
  class Meta:
    model=categoria
    fields='__all__'

class alumnoForm(CustomModelForm):
  class Meta:
    model=alumno
    fields='__all__'