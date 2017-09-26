# -*- coding:UTF-8 -*-
from django import forms
from base.forms import CustomModelForm,CustomForm
from usuario.models import usuario
from proyecto.models import project,task,file,filetask
class projectForm(CustomModelForm):
	class Meta:
		model 	= project
		exclude = ('usuario','porcentaje')

taskFormset = forms.inlineformset_factory(
    project,
    task,
    fields='__all__',
    extra=0,
    min_num=1,
    widgets={
    'usuario':forms.Select(attrs={'class':'form-control'}),
    'estatus':forms.Select(attrs={'class':'form-control'}),
    'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
    'prioridad':forms.Select(attrs={'class':'form-control'}),
    'start_line':forms.DateInput(attrs={'class':'form-control date'}),
    'dead_line':forms.DateInput(attrs={'class':'form-control date'}),
    }
    )
fileFormset = forms.inlineformset_factory(
	project,
	file,
	fields='__all__',
	extra=0,
	min_num=1,
	widgets={
		'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
	}
	)

class projectSForm(CustomModelForm):
	class Meta:
		model = project
		exclude = ('usuario','porcentaje','estatus')
			
class taskForm(CustomModelForm):
	class Meta:
		model = task
		exclude = ('usuario','estatus','observacion','dead_line')

class taskCForm(CustomModelForm):
	class Meta:
		model = task
		fields = ('observacion',)

class filetaskForm(CustomModelForm):
	class Meta:
		model = filetask
		exclude = ('up_date',)

class filetaskMForm(CustomModelForm):
	class Meta:
		model = filetask
		exclude = ('up_date','proyecto')

