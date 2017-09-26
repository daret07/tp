# -*- coding:UTF-8 -*-
from django import forms
from base.forms import CustomModelForm,CustomForm
from usuario.models import usuario
from bitacora.models import bitacora,registro,observacion,participante,filereg
class bitacoraForm(CustomModelForm):
	class Meta:
		model 	= bitacora
		exclude = ('start_line','usuario')

participanteFormset = forms.inlineformset_factory(
	bitacora,
	participante,
	fields='__all__',
	extra=0,
	min_num=1,
	widgets={
		'usuario':forms.Select(attrs={'class':'form-control'}),
	}
	)

class registroForm(CustomModelForm):
	class Meta:
		model = registro
		exclude = ('usuario','hora_f','resultado','capturado')

class bitForm(CustomModelForm):
	class Meta:
		model = bitacora
		exclude = ('start_line','usuario')

class regForm(CustomModelForm):
	class Meta:
		model = registro
		exclude = ('usuario','resultado','hora_f')

class fileregForm(CustomModelForm):
	class Meta:
		model = filereg
		exclude = ('up_date','registro')

class conclusionForm(CustomModelForm):
	class Meta:
		model = registro
		fields = ('resultado',)