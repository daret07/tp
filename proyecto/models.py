# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from usuario.models import usuario
import datetime



estado=(
	(u'1',u'Abierto'),
	(u'2',u'Suspendido'),
	(u'3',u'Cerrado'),
)

# Create your models here.
class project(models.Model):
	usuario     = models.ForeignKey(usuario, on_delete=models.CASCADE)
	titulo      = models.CharField(max_length = 50)
	estatus     = models.CharField(max_length = 50,choices=estado,verbose_name='Estado')
	descripcion = models.TextField()
	dead_line   = models.DateField(verbose_name='Fecha Fin',blank=True,null=True)
	porcentaje  = models.IntegerField(blank=True,null=True)
	start_line  = models.DateField(default = datetime.date.today,verbose_name='Fecha Inicio')

	def __str__(self):
		return str(self.titulo)
	
	class Meta:
		permissions = (
			('proyecto_menu','Can add proyecto_menu'),
			('bitacora_menu','Can add bitacora_menu'),
			)

prioridad_c=(
	(u'1',u'Baja'),
	(u'2',u'Media'),
	(u'3',u'Alta'),
	)
estado=(
	(u'1',u'Pendiente'),
	(u'2',u'Finalizada'),
)
class task(models.Model):
	proyecto    = models.ForeignKey('proyecto.project',on_delete=models.CASCADE)
	titulo      = models.CharField(max_length = 50)
	usuario     = models.ForeignKey(usuario,blank=True,null=True,on_delete=models.CASCADE)
	estatus     = models.CharField(max_length=50,blank=True,null=True,choices=estado)
	descripcion = models.TextField()
	prioridad  	= models.CharField(max_length=20,choices=prioridad_c,verbose_name='Prioridad',blank=True,null=True)
	observacion = models.TextField(verbose_name='Observaciones',blank=True,null=True)
	start_line  = models.DateField(blank=True,null=True,verbose_name='Fecha Inicio')
	dead_line   = models.DateField(blank=True,null=True,verbose_name='Fecha Fin')
	def __str__(self):
		return self.titulo

class file(models.Model):
	proyecto    = models.ForeignKey('proyecto.project',on_delete=models.CASCADE)
	descripcion = models.TextField(blank=True,null=True)
	up_date     = models.DateField(default = datetime.date.today,blank=True,null=True)
	file        = models.FileField(upload_to='files/project/')


class filetask(models.Model):
	proyecto    = models.ForeignKey('proyecto.task',on_delete=models.CASCADE,verbose_name="Tarea")
	descripcion = models.TextField(blank=True,null=True)
	up_date     = models.DateField(default = datetime.date.today,blank=True,null=True)
	file        = models.FileField(upload_to='files/subTask/')