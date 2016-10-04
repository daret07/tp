# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
crons=((u'0',u'Mensual'),(u'1',u'Recargos'))

class cron_auto(models.Model):
  definicion    = models.CharField(max_length=50)
  activo        = models.BooleanField(default=True)
  cron          = models.CharField(max_length=50,choices=crons)
