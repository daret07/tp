# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from proyecto.models import project
from usuario.models import usuario
import datetime

# Create your models here.

class bitacora(models.Model):
	proyecto    = models.ForeignKey(project, on_delete=models.CASCADE,blank=True,null=True,verbose_name='Bitacora de proyecto')
	titulo      = models.CharField(max_length = 50)
	usuario     = models.ForeignKey(usuario, on_delete=models.CASCADE)
	descripcion = models.TextField()
	start_line  = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.titulo
		

class registro(models.Model):
	bitacora    = models.ForeignKey(bitacora, on_delete=models.CASCADE)
	usuario     = models.ForeignKey(usuario, on_delete=models.CASCADE)
	fecha_d		  = models.DateTimeField(auto_now_add=True)
	actividad   = models.CharField(max_length=100)
	registro_o  = models.TextField(verbose_name="Detalles Extra")
	resultado		= models.TextField(verbose_name="Resultado",blank=True,null=True)
	capturado   = models.BooleanField(default=False)
	hora_f 			= models.DateTimeField(blank=True,null=True)

class observacion(models.Model):
	usuario 		= models.ForeignKey(usuario,on_delete=models.CASCADE)
	observacion = models.TextField()
	registro    = models.ForeignKey(registro, on_delete=models.CASCADE)
	fecha_obser = models.DateTimeField(auto_now_add=True)


class participante(models.Model):
	usuario		  = models.ForeignKey(usuario,on_delete=models.CASCADE)
	bitacora 		= models.ForeignKey(bitacora, on_delete=models.CASCADE)

class filereg(models.Model):
	registro    = models.ForeignKey('bitacora.registro',on_delete=models.CASCADE,verbose_name="Archivo")
	descripcion = models.TextField(blank=True,null=True)
	up_date     = models.DateField(default = datetime.date.today,blank=True,null=True)
	file        = models.FileField(upload_to='files/registro/')