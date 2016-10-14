# -*- coding: utf-8 -*-
from django import forms
from base.forms import CustomForm,CustomModelForm
from reporte.models import *
from catalogo.models import ciclo_escolar,categoria,alumno as alm


class movimientoForm(CustomModelForm):
  def __init__(self, *args,**kwargs):
    super(movimientoForm,self).__init__(*args,**kwargs)
    if self.fields['monto'].widget.attrs.has_key('class'):
      self.fields['monto'].widget.attrs['class']+='form-control decimal'
    else:
      self.fields['monto'].widget.attrs.update({'class' : 'form-control decimal'})
  class Meta:
    model=movimiento
    exclude=('descripcion','ciclo')

class movimiento_subirForm(CustomForm):
  subir_movimiento = forms.FileField()

class reporte_saldosForm(CustomForm):
  def __init__(self, *args,**kwargs):
    super(reporte_saldosForm,self).__init__(*args,**kwargs)
    self.fields['ciclo'].widget.attrs['class']='form-control'
  desde   = forms.DateField()
  hasta   = forms.DateField()
  ciclo   = forms.ModelChoiceField(queryset=ciclo_escolar.objects.all(),required=False)

class ficha_inscricionForm(CustomForm):
  def __init__(self, *args,**kwargs):
    super(ficha_inscricionForm,self).__init__(*args,**kwargs)
    self.fields['ciclo'].widget.attrs['class']='form-control'
    self.fields['categoria'].widget.attrs['class']='form-control'
  ciclo     = forms.ModelChoiceField(queryset=ciclo_escolar.objects.all(),required=False)
  categoria = forms.ModelChoiceField(queryset=categoria.objects.all(),required=False)

meses=(
  (u'1',u'ENERO'),
  (u'2',u'FEBRERO'),
  (u'3',u'MARZO'),
  (u'4',u'ABRIL'),
  (u'5',u'MAYO'),
  (u'6',u'JUNIO'),
  (u'7',u'JULIO'),
  (u'8',u'AGOSTO'),
  (u'9',u'SEPTIEMBRE'),
  (u'10',u'OCTUBRE'),
  (u'11',u'NOVIEMBRE'),
  (u'12',u'DICIEMBRE'),
)

class estado_cuentaForm(CustomForm):
  def __init__(self, *args,**kwargs):
    super(estado_cuentaForm,self).__init__(*args,**kwargs)
    self.fields['mes'].widget.attrs['class']='form-control'
    self.fields['anio'].widget.attrs['class']='form-control decimal-y'
    self.fields['alumno'].widget.attrs['class']='form-control'
  mes           = forms.ChoiceField(choices=meses,required=False)
  anio          = forms.IntegerField(required=False)
  alumno        = forms.ModelChoiceField(queryset=alm.objects.all(),required=True)