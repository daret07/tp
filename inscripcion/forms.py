from django import forms
from base.forms import CustomForm,CustomModelForm
from inscripcion.models import *


class inscripcionForm(CustomModelForm):
  class Meta:
    model=inscripcion
    fields='__all__'