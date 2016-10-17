# -*- coding: utf-8 -*-
from automatico.models import cron_auto,recargo_pago
from django import forms
from base.forms import CustomForm,CustomModelForm
class cron_autoForm(CustomModelForm):
  class Meta:
    model   =cron_auto
    exclude =('definicion',)


recargo_pagoFormset = forms.inlineformset_factory(
    cron_auto,
    recargo_pago,
    fields='__all__',
    extra=0,
    min_num=1,
    widgets={
        'concepto': forms.Select(attrs={'class':'form-control'}),
        'cantidad_debe':forms.Select(attrs={'class':'form-control'}),
        'aplica':forms.Select(attrs={'class':'form-control'}),
        }
    )