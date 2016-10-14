# -*- coding:UTF-8 -*-
from django import forms
from base.forms import CustomModelForm,CustomForm
from usuario.models import usuario

class usuarioForm(CustomModelForm):
  clave              = forms.CharField(label='Password',widget=forms.PasswordInput(),required=False)
  clave_confirmacion = forms.CharField(label='Password (Confirmación)',widget=forms.PasswordInput(),required=False)

  class Meta:
    model  = usuario
    exclude = ('metodo_autenticacion','is_staff','user_permissions','password','last_login',)
