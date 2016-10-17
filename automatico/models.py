# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from catalogo.models import concepto
# Create your models here.

class cron_auto(models.Model):
  definicion    = models.CharField(max_length=50)
  activo        = models.BooleanField(default=True)
  hermanos      = models.BooleanField()
  concepto      = models.ForeignKey('catalogo.concepto',blank=True,null=True,on_delete=models.SET_NULL)
  condiciones   = models.BooleanField()

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
  (u'10',u'10')
  )
class recargo_pago(models.Model):
  activo        = models.BooleanField()
  padre         = models.ForeignKey('automatico.cron_auto')
  cantidad_debe = models.CharField(max_length=2,choices=numero)
  concepto      = models.ForeignKey('catalogo.concepto')
  aplica        = models.ForeignKey('catalogo.concepto',related_name='aplica')
