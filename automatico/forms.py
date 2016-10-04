# -*- coding: utf-8 -*-
from automatico.models import cron_auto
from django import forms
from base.forms import CustomForm,CustomModelForm
class cron_autoForm(CustomModelForm):
  class Meta:
    model   =cron_auto
    exclude =('definicion',)
