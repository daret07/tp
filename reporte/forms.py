# -*- coding: utf-8 -*-
from django import forms
from base.forms import CustomForm,CustomModelForm
from reporte.models import *


class movimientoForm(CustomModelForm):
  def __init__(self, *args,**kwargs):
    super(movimientoForm,self).__init__(*args,**kwargs)
    if self.fields['monto'].widget.attrs.has_key('class'):
      self.fields['monto'].widget.attrs['class']+='form-control decimal'
    else:
      self.fields['monto'].widget.attrs.update({'class' : 'form-control decimal'})
  class Meta:
    model=movimiento
    fields='__all__'

class movimiento_subirForm(CustomForm):
  subir_movimiento = forms.FileField()