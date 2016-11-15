# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from catalogo.models import concepto
# Create your models here.

tip=(
  (u'1',u'Mensual'),
  (u'2',u'Recargos')
  )

class cron_auto(models.Model):
  definicion    = models.CharField(max_length=550)
  descripcion   = models.TextField(max_length=250,default='')
  activo        = models.BooleanField(default=True)
  tipo          = models.CharField(max_length=10,choices=tip,default='1')

numero=(
  (u'1',u'1'),
  (u'2',u'2'),
  (u'3',u'3'),
  (u'4',u'4'),
  (u'5',u'5'),
  (u'6',u'6'),
  (u'7',u'7'),
  (u'8',u'8'),
  (u'9',u'9'),
  (u'10',u'10'),
  (u'11',u'11'),
  (u'12',u'12'),
  (u'13',u'13'),
  (u'14',u'14'),
  (u'15',u'15'),
  (u'16',u'16'),
  (u'17',u'17'),
  (u'18',u'18'),
  (u'19',u'19'),
  (u'20',u'20'),
  (u'21',u'21'),
  (u'22',u'22'),
  (u'23',u'23'),
  (u'24',u'24'),
  (u'25',u'25'),
  (u'26',u'26'),
  (u'27',u'27'),
  (u'28',u'28'),
  (u'29',u'29'),
  (u'30',u'30'),
  )
class recargo_pago(models.Model):
  activo        = models.BooleanField()
  padre         = models.ForeignKey('automatico.cron_auto')
  cantidad_debe = models.CharField(max_length=2,choices=numero)
  concepto      = models.ForeignKey('catalogo.concepto',blank=True,null=True,on_delete=models.SET_NULL)
  aplica        = models.ForeignKey('catalogo.concepto',related_name='aplica',blank=True,null=True,on_delete=models.SET_NULL)
  diferencia    = models.IntegerField()


class pronto_pago(models.Model):
  activo        = models.BooleanField()
  padre         = models.ForeignKey('automatico.cron_auto')
  beca          = models.ForeignKey('catalogo.concepto',blank=True,null=True,on_delete=models.SET_NULL)