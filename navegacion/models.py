from __future__ import unicode_literals

from django.db import models

class menu(models.Model):
  nombre  = models.CharField(max_length=75)
  app     = models.CharField(max_length=75)
  modelo  = models.CharField(max_length=75)
  padre   = models.ForeignKey('menu',related_name='hijos',blank=True,null=True,  on_delete=models.SET_NULL)
  icono   = models.CharField(max_length=45,blank=True,null=True)
  permiso = models.CharField(max_length=75,blank=True,null=True)
  nivel   = models.IntegerField(default=0)
  listar  = models.BooleanField(default=True)
  activo  = models.BooleanField(default=True)

  def __unicode__(self):
    return '%s' % (self.nombre)