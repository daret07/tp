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

class descuentoForm(CustomModelForm):
  class Meta:
    model=descuento
    fields='__all__'

class alumnoForm(CustomModelForm):
  def __init__(self, *args,**kwargs):
    super(alumnoForm,self).__init__(*args,**kwargs)
    if self.fields['matricula'].widget.attrs.has_key('class'):
      self.fields['matricula'].widget.attrs.update({'class' : 'form-control decimal','readonly':'readonly'})
    if self.fields['fecha_de_ingreso'].widget.attrs.has_key('class'):
      self.fields['fecha_de_ingreso'].widget.attrs.update({'class' : 'form-control ','readonly':'readonly'})
  class Meta:
    model=alumno
    fields='__all__'

class personaForm(CustomModelForm):
  class Meta:
    model=persona
    exclude=('tipo',)

referenciaFormset = forms.inlineformset_factory(
    alumno,
    referencias,
    fields='__all__',
    extra=0,
    min_num=1,
    widgets={
        'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'1','readonly':'readonly'}),
        'referencia':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'})
    }
    )


descuentoFormset = forms.inlineformset_factory(
    alumno,
    descuento,
    fields='__all__',
    extra=0,
    min_num=1,
    widgets={
        'tipo_descuento':forms.Select(attrs={'class':'form-control'}),
        'monto':forms.TextInput(attrs={'class':'form-control decimal'}),
        'concepto': forms.Select(attrs={'class':'form-control concepto_auto'}),
        }
    )